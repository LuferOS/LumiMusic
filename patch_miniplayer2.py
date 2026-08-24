import re

with open("app/src/main/java/com/example/ui/components/MiniPlayer.kt", "r") as f:
    content = f.read()

old_buttons = """                IconButton(onClick = {
                    if (isPlaying) controller.pause() else controller.play()
                }) {
                    Icon(
                        imageVector = if (isPlaying) Icons.Rounded.Pause else Icons.Rounded.PlayArrow,
                        contentDescription = "Play/Pause"
                    )
                }"""

new_buttons = """                IconButton(onClick = { controller.seekToPrevious() }) {
                    Icon(imageVector = Icons.Rounded.SkipPrevious, contentDescription = "Previous")
                }
                IconButton(onClick = {
                    if (isPlaying) controller.pause() else controller.play()
                }) {
                    Icon(
                        imageVector = if (isPlaying) Icons.Rounded.Pause else Icons.Rounded.PlayArrow,
                        contentDescription = "Play/Pause"
                    )
                }
                IconButton(onClick = { controller.seekToNext() }) {
                    Icon(imageVector = Icons.Rounded.SkipNext, contentDescription = "Next")
                }"""

content = content.replace(old_buttons, new_buttons)

with open("app/src/main/java/com/example/ui/components/MiniPlayer.kt", "w") as f:
    f.write(content)
