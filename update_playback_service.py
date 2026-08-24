import re

with open("app/src/main/java/com/example/player/PlaybackService.kt", "r") as f:
    content = f.read()

target = """    private fun applyTransitionEffects(player: ExoPlayer) {
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

replacement = """    private var monitorJob: Job? = null
    
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
    }"""

content = content.replace(target, replacement)

with open("app/src/main/java/com/example/player/PlaybackService.kt", "w") as f:
    f.write(content)
