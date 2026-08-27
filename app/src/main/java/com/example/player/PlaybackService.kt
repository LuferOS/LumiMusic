package com.example.player

import androidx.media3.common.AudioAttributes
import androidx.media3.common.C
import androidx.media3.exoplayer.ExoPlayer
import androidx.media3.exoplayer.DefaultRenderersFactory
import androidx.media3.exoplayer.audio.DefaultAudioSink
import androidx.media3.exoplayer.audio.TeeAudioProcessor
import androidx.media3.session.MediaSession
import androidx.media3.session.MediaSessionService
import androidx.media3.exoplayer.DefaultLoadControl
import androidx.media3.common.Player
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.Job
import kotlinx.coroutines.delay
import kotlinx.coroutines.launch
import kotlinx.coroutines.flow.firstOrNull
import com.example.data.local.AppDatabase
import android.content.Intent

import androidx.media3.datasource.cache.SimpleCache
import androidx.media3.datasource.cache.LeastRecentlyUsedCacheEvictor
import androidx.media3.database.StandaloneDatabaseProvider
import androidx.media3.datasource.cache.CacheDataSource
import androidx.media3.datasource.DefaultHttpDataSource
import androidx.media3.exoplayer.source.DefaultMediaSourceFactory
import java.io.File


class PlaybackService : MediaSessionService() {

    companion object {
        private var downloadCache: SimpleCache? = null
        
        @androidx.annotation.OptIn(androidx.media3.common.util.UnstableApi::class)
        fun getCache(context: android.content.Context): SimpleCache {
            if (downloadCache == null) {
                val cacheDir = File(context.cacheDir, "media_cache")
                val evictor = LeastRecentlyUsedCacheEvictor(200 * 1024 * 1024) // 200MB LRU Cache
                downloadCache = SimpleCache(cacheDir, evictor, StandaloneDatabaseProvider(context))
            }
            return downloadCache!!
        }
    }

    private var mediaSession: MediaSession? = null

    private val serviceScope = CoroutineScope(Dispatchers.Main + Job())
    private var fadeJob: Job? = null
    
        private var currentTransitionType = "Gapless"
    private var currentTransitionDuration = 3
    
    override fun onCreate() {
        super.onCreate()
        // Cargar configuración de transiciones una vez (y escuchar cambios en background)
        serviceScope.launch {
            AppDatabase.getDatabase(this@PlaybackService).userStatsDao().getStats().collect { stats ->
                currentTransitionType = stats?.transitionType ?: "Gapless"
                currentTransitionDuration = stats?.transitionDuration ?: 3
            }
        }
        super.onCreate()
        
        // Improve response times with aggressive LoadControl
        // Optimización de entradas y caché: Buffering agresivo para la siguiente canción
        // Aseguramos que empiece a descargar la siguiente pista mucho antes (al menos 20s - 50s)
        val loadControl = DefaultLoadControl.Builder()
            .setBufferDurationsMs(
                50000, // min buffer 50s
                100000, // max buffer 100s
                1500, // buffer for playback 1.5s
                2500  // buffer for playback after rebuffer 2.5s
            )
            .build()
            
        @androidx.annotation.OptIn(androidx.media3.common.util.UnstableApi::class)
        val httpDataSourceFactory = DefaultHttpDataSource.Factory().setAllowCrossProtocolRedirects(true)
        
        @androidx.annotation.OptIn(androidx.media3.common.util.UnstableApi::class)
        val cacheDataSourceFactory = CacheDataSource.Factory()
            .setCache(getCache(this))
            .setUpstreamDataSourceFactory(httpDataSourceFactory)
            .setFlags(CacheDataSource.FLAG_IGNORE_CACHE_ON_ERROR)
            
        @androidx.annotation.OptIn(androidx.media3.common.util.UnstableApi::class)
        val mediaSourceFactory = DefaultMediaSourceFactory(this)
            .setDataSourceFactory(cacheDataSourceFactory)

        val teeProcessor = TeeAudioProcessor(AudioAmplituder)
        val renderersFactory = object : DefaultRenderersFactory(this) {
            override fun buildAudioSink(context: android.content.Context, enableFloatOutput: Boolean, enableAudioTrackPlaybackParams: Boolean): androidx.media3.exoplayer.audio.AudioSink {
                return DefaultAudioSink.Builder(context)
                    .setAudioProcessors(arrayOf(teeProcessor))
                    .build()
            }
        }

        val player = ExoPlayer.Builder(this, renderersFactory)
            .setMediaSourceFactory(mediaSourceFactory)
            .setAudioAttributes(
                AudioAttributes.Builder()
                    .setContentType(C.AUDIO_CONTENT_TYPE_MUSIC)
                    .setUsage(C.USAGE_MEDIA)
                    .build(),
                true // handleAudioFocus
            )
            .setLoadControl(loadControl)
            .setHandleAudioBecomingNoisy(true)
            .build()
            
        // Enable Gapless playback by ignoring silence and keeping decoders active
        player.skipSilenceEnabled = true
        
        val intent = android.content.Intent(this, com.example.MainActivity::class.java)
        val pendingIntent = android.app.PendingIntent.getActivity(
            this,
            0,
            intent,
            android.app.PendingIntent.FLAG_IMMUTABLE or android.app.PendingIntent.FLAG_UPDATE_CURRENT
        )
        mediaSession = MediaSession.Builder(this, player)
            .setSessionActivity(pendingIntent)
            .build()
        
        // Initialize AudioEffectManager when audio session ID is available
        player.addListener(object : Player.Listener {
            override fun onAudioSessionIdChanged(audioSessionId: Int) {
                super.onAudioSessionIdChanged(audioSessionId)
                AudioEffectManager.init(audioSessionId)
            }
        })
        
        player.addListener(object : Player.Listener {
            override fun onMediaItemTransition(mediaItem: androidx.media3.common.MediaItem?, reason: Int) {
                super.onMediaItemTransition(mediaItem, reason)
                if (reason == Player.MEDIA_ITEM_TRANSITION_REASON_AUTO || reason == Player.MEDIA_ITEM_TRANSITION_REASON_SEEK) {
                    applyTransitionEffects(player)
                }
            }
        })
    }
    
    private var monitorJob: Job? = null
    
    private fun applyTransitionEffects(player: ExoPlayer) {
        serviceScope.launch {
            val transitionType = currentTransitionType
            val durationSeconds = currentTransitionDuration
            
            fadeJob?.cancel()
            monitorJob?.cancel()
            
            if (transitionType == "Crossfade" || transitionType == "Fade") {
                // Aseguramos que inicie en 0 para un crossfade/V-fade limpio
                player.volume = 0f
                
                // Fade-in
                fadeJob = launch {
                    val steps = 20
                    val delayMs = (durationSeconds * 1000L) / steps
                    for (i in 1..steps) {
                        player.volume = (i.toFloat() / steps)
                        delay(delayMs)
                    }
                    player.volume = 1f
                }
                
                // Monitor for Fade-out
                monitorJob = launch {
                    val durationMs = durationSeconds * 1000L
                    var fadeOutStarted = false
                    while (!fadeOutStarted) {
                        val playerDuration = player.duration
                        val currentPos = player.currentPosition
                        
                        // Fix crossfade logic: trigger slightly earlier to ensure smooth fade
                        if (playerDuration > 0 && playerDuration - currentPos <= durationMs + 200 && player.isPlaying) {
                            fadeOutStarted = true
                            // Start fade out
                            val steps = 20
                            val delayMs = durationMs / steps
                            for (i in steps downTo 1) {
                                player.volume = (i.toFloat() / steps)
                                delay(delayMs)
                            }
                            player.volume = 0f
                        }
                        if (!fadeOutStarted) delay(250) // poll faster for better accuracy
                    }
                }
            } else {
                player.volume = 1f
            }
        }
    }

    override fun onGetSession(controllerInfo: MediaSession.ControllerInfo): MediaSession? {
        return mediaSession
    }

    override fun onTaskRemoved(rootIntent: Intent?) {
        val player = mediaSession?.player
        if (player != null && !player.playWhenReady) {
            stopSelf()
        }
    }

    override fun onDestroy() {
        AudioEffectManager.release()
        mediaSession?.run {
            player.release()
            release()
            mediaSession = null
        }
        super.onDestroy()
    }
}
