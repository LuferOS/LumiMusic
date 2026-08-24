import re

with open("app/src/main/java/com/example/player/PlaybackService.kt", "r") as f:
    content = f.read()

target = "mediaSession = MediaSession.Builder(this, player).build()"
replacement = """mediaSession = MediaSession.Builder(this, player).build()
        
        // Initialize AudioEffectManager when audio session ID is available
        player.addListener(object : Player.Listener {
            override fun onAudioSessionIdChanged(audioSessionId: Int) {
                super.onAudioSessionIdChanged(audioSessionId)
                AudioEffectManager.init(audioSessionId)
            }
        })"""

content = content.replace(target, replacement)

with open("app/src/main/java/com/example/player/PlaybackService.kt", "w") as f:
    f.write(content)
