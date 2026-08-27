import re

with open("app/src/main/java/com/example/ui/components/FullScreenPlayer.kt", "r") as f:
    content = f.read()

target = """                    Icon(
                        imageVector = if (isPlaying) Icons.Rounded.Pause else Icons.Rounded.PlayArrow,
                        contentDescription = "Play/Pause",
                        modifier = Modifier.size(36.dp),
                        tint = Color.Black
                    )"""

replacement = """                    androidx.compose.animation.AnimatedContent(
                        targetState = isPlaying,
                        label = "play_pause_anim"
                    ) { playing ->
                        Icon(
                            imageVector = if (playing) Icons.Rounded.Pause else Icons.Rounded.PlayArrow,
                            contentDescription = "Play/Pause",
                            modifier = Modifier.size(36.dp),
                            tint = Color.Black
                        )
                    }"""

content = content.replace(target, replacement)

with open("app/src/main/java/com/example/ui/components/FullScreenPlayer.kt", "w") as f:
    f.write(content)
