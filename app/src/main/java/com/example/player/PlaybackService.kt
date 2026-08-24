package com.example.player

import androidx.media3.common.AudioAttributes
import androidx.media3.common.C
import androidx.media3.exoplayer.ExoPlayer
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

class PlaybackService : MediaSessionService() {
    private var mediaSession: MediaSession? = null

    private val serviceScope = CoroutineScope(Dispatchers.Main + Job())
    private var fadeJob: Job? = null
    
    override fun onCreate() {
        super.onCreate()
        
        // Improve response times with aggressive LoadControl
        val loadControl = DefaultLoadControl.Builder()
            .setBufferDurationsMs(
                DefaultLoadControl.DEFAULT_MIN_BUFFER_MS / 2, // 25 seconds instead of 50
                DefaultLoadControl.DEFAULT_MAX_BUFFER_MS / 2, // 25 seconds instead of 50
                DefaultLoadControl.DEFAULT_BUFFER_FOR_PLAYBACK_MS / 2, // 1250ms instead of 2500ms
                DefaultLoadControl.DEFAULT_BUFFER_FOR_PLAYBACK_AFTER_REBUFFER_MS / 2
            )
            .build()
            
        val player = ExoPlayer.Builder(this)
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
        
        mediaSession = MediaSession.Builder(this, player).build()
        
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
            val stats = AppDatabase.getDatabase(this@PlaybackService).userStatsDao().getStatsDirect()
            val transitionType = stats?.transitionType ?: "Gapless"
            val durationSeconds = stats?.transitionDuration ?: 3
            
            fadeJob?.cancel()
            monitorJob?.cancel()
            
            if (transitionType == "Crossfade" || transitionType == "Fade") {
                // Fade-in
                fadeJob = launch {
                    player.volume = 0f
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
                    while (true) {
                        val playerDuration = player.duration
                        val currentPos = player.currentPosition
                        if (playerDuration > 0 && playerDuration - currentPos <= durationMs && player.isPlaying) {
                            // Start fade out
                            val steps = 20
                            val delayMs = durationMs / steps
                            for (i in steps downTo 1) {
                                player.volume = (i.toFloat() / steps)
                                delay(delayMs)
                            }
                            break // End monitoring for this track
                        }
                        delay(500)
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
