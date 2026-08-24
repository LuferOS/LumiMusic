import re

with open("app/src/main/java/com/example/player/PlaybackService.kt", "r") as f:
    content = f.read()

imports = """import androidx.media3.exoplayer.DefaultLoadControl
import androidx.media3.common.Player
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.Job
import kotlinx.coroutines.delay
import kotlinx.coroutines.launch
import kotlinx.coroutines.flow.firstOrNull
import com.example.data.local.AppDatabase"""

if "import androidx.media3.exoplayer.DefaultLoadControl" not in content:
    content = content.replace("import androidx.media3.session.MediaSessionService", "import androidx.media3.session.MediaSessionService\n" + imports)

# We need to modify onCreate to use DefaultLoadControl and listen for transitions
target_create = """    override fun onCreate() {
        super.onCreate()
        val player = ExoPlayer.Builder(this)
            .setAudioAttributes(
                AudioAttributes.Builder()
                    .setContentType(C.AUDIO_CONTENT_TYPE_MUSIC)
                    .setUsage(C.USAGE_MEDIA)
                    .build(),
                true
            )
            .build()
        
        mediaSession = MediaSession.Builder(this, player).build()
    }"""

replacement_create = """    private val serviceScope = CoroutineScope(Dispatchers.Main + Job())
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
        
        player.addListener(object : Player.Listener {
            override fun onMediaItemTransition(mediaItem: androidx.media3.common.MediaItem?, reason: Int) {
                super.onMediaItemTransition(mediaItem, reason)
                if (reason == Player.MEDIA_ITEM_TRANSITION_REASON_AUTO || reason == Player.MEDIA_ITEM_TRANSITION_REASON_SEEK) {
                    applyTransitionEffects(player)
                }
            }
        })
    }
    
    private fun applyTransitionEffects(player: ExoPlayer) {
        serviceScope.launch {
            val stats = AppDatabase.getDatabase(this@PlaybackService).userStatsDao().getStatsDirect()
            val transitionType = stats?.transitionType ?: "Gapless"
            val duration = stats?.transitionDuration ?: 3
            
            if (transitionType == "Crossfade") {
                // Perform a Fade-in
                fadeJob?.cancel()
                fadeJob = launch {
                    player.volume = 0f
                    val steps = 20
                    val delayMs = (duration * 1000L) / steps
                    for (i in 1..steps) {
                        if (!player.isPlaying && player.playbackState != Player.STATE_READY) break
                        player.volume = (i.toFloat() / steps)
                        delay(delayMs)
                    }
                    player.volume = 1f
                }
            } else {
                player.volume = 1f
            }
        }
    }"""

content = content.replace(target_create, replacement_create)

with open("app/src/main/java/com/example/player/PlaybackService.kt", "w") as f:
    f.write(content)
