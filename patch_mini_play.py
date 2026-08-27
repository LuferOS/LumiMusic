import re

with open("app/src/main/java/com/example/ui/components/MiniPlayer.kt", "r") as f:
    content = f.read()

target = """                        Icon(
                            imageVector = if (isPlaying) Icons.Rounded.Pause else Icons.Rounded.PlayArrow,
                            contentDescription = "Play/Pause",
                            tint = Color.White
                        )"""

replacement = """                        androidx.compose.animation.AnimatedContent(
                            targetState = isPlaying,
                            label = "play_pause_anim_mini"
                        ) { playing ->
                            Icon(
                                imageVector = if (playing) Icons.Rounded.Pause else Icons.Rounded.PlayArrow,
                                contentDescription = "Play/Pause",
                                tint = Color.White
                            )
                        }"""

content = content.replace(target, replacement)
with open("app/src/main/java/com/example/ui/components/MiniPlayer.kt", "w") as f:
    f.write(content)
