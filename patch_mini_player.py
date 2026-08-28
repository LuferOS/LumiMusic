import re

with open('app/src/main/java/com/example/ui/components/MiniPlayer.kt', 'r') as f:
    content = f.read()

# 1. Update baseModifier to have padding outside
# Currently:
#         val baseModifier = Modifier
#             .fillMaxWidth()
#             .height(64.dp)
#             .padding(horizontal = 16.dp, vertical = 8.dp)
content = content.replace(
"""        val baseModifier = Modifier
            .fillMaxWidth()
            .height(64.dp)
            .padding(horizontal = 16.dp, vertical = 8.dp)""",
"""        val baseModifier = Modifier
            .fillMaxWidth()
            .padding(horizontal = 12.dp, vertical = 8.dp)
            .height(64.dp)"""
)

# 2. Add CircularProgressIndicator to Play/Pause button
play_btn_old = """                    IconButton(onClick = {
                        view.performHapticFeedback(HapticFeedbackConstants.CLOCK_TICK)
                        if (isPlaying) controller?.pause() else controller?.play()
                    }) {
                        if (isBatterySaverOn) {
                            Icon(
                                imageVector = if (isPlaying) Icons.Rounded.Pause else Icons.Rounded.PlayArrow,
                                contentDescription = "Play/Pause",
                                tint = Color.White,
                                modifier = Modifier.size(32.dp)
                            )
                        } else {
                            androidx.compose.animation.AnimatedContent(
                                targetState = isPlaying,
                                label = "play_pause_anim_mini"
                            ) { playing ->
                                Icon(
                                    imageVector = if (playing) Icons.Rounded.Pause else Icons.Rounded.PlayArrow,
                                    contentDescription = "Play/Pause",
                                    tint = Color.White,
                                    modifier = Modifier.size(32.dp)
                                )
                            }
                        }
                    }"""

play_btn_new = """                    Box(contentAlignment = Alignment.Center) {
                        CircularProgressIndicator(
                            progress = { progress },
                            modifier = Modifier.size(44.dp),
                            color = Color.White.copy(alpha = 0.5f),
                            trackColor = Color.White.copy(alpha = 0.1f),
                            strokeWidth = 2.dp,
                            strokeCap = androidx.compose.ui.graphics.StrokeCap.Round
                        )
                        IconButton(onClick = {
                            view.performHapticFeedback(HapticFeedbackConstants.CLOCK_TICK)
                            if (isPlaying) controller?.pause() else controller?.play()
                        }) {
                            if (isBatterySaverOn) {
                                Icon(
                                    imageVector = if (isPlaying) Icons.Rounded.Pause else Icons.Rounded.PlayArrow,
                                    contentDescription = "Play/Pause",
                                    tint = Color.White,
                                    modifier = Modifier.size(28.dp)
                                )
                            } else {
                                androidx.compose.animation.AnimatedContent(
                                    targetState = isPlaying,
                                    label = "play_pause_anim_mini"
                                ) { playing ->
                                    Icon(
                                        imageVector = if (playing) Icons.Rounded.Pause else Icons.Rounded.PlayArrow,
                                        contentDescription = "Play/Pause",
                                        tint = Color.White,
                                        modifier = Modifier.size(28.dp)
                                    )
                                }
                            }
                        }
                    }"""

content = content.replace(play_btn_old, play_btn_new)

# 3. Remove LinearProgressIndicator
linear_progress = """                LinearProgressIndicator(
                    progress = { progress },
                    modifier = Modifier
                        .fillMaxWidth()
                        .height(2.dp),
                    color = Color.White,
                    trackColor = Color.White.copy(alpha = 0.3f),
                )"""

content = content.replace(linear_progress, "")

with open('app/src/main/java/com/example/ui/components/MiniPlayer.kt', 'w') as f:
    f.write(content)
