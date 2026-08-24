import re

with open("app/src/main/java/com/example/ui/components/MiniPlayer.kt", "r") as f:
    content = f.read()

target = """                    IconButton(onClick = {
                        view.performHapticFeedback(HapticFeedbackConstants.VIRTUAL_KEY)
                        if (isPlaying) controller.pause() else controller.play()
                    }) {
                        Icon(
                            imageVector = if (isPlaying) Icons.Rounded.Pause else Icons.Rounded.PlayArrow,
                            contentDescription = "Play/Pause",
                            tint = Color.White
                        )
                    }
                }"""

replacement = """                    IconButton(onClick = {
                        view.performHapticFeedback(HapticFeedbackConstants.VIRTUAL_KEY)
                        if (isPlaying) controller.pause() else controller.play()
                    }) {
                        Icon(
                            imageVector = if (isPlaying) Icons.Rounded.Pause else Icons.Rounded.PlayArrow,
                            contentDescription = "Play/Pause",
                            tint = Color.White
                        )
                    }
                    IconButton(onClick = {
                        view.performHapticFeedback(HapticFeedbackConstants.VIRTUAL_KEY)
                        if ((controller.mediaItemCount ?: 0) <= 1) {
                            val isShuffle = controller.shuffleModeEnabled == true
                            val repeatMode = controller.repeatMode ?: Player.REPEAT_MODE_OFF
                            viewModel.playNextRemote(isShuffle, repeatMode)
                        } else {
                            controller.seekToNext()
                        }
                    }) {
                        Icon(
                            imageVector = Icons.Rounded.SkipNext,
                            contentDescription = "Next",
                            tint = Color.White
                        )
                    }
                }"""

content = content.replace(target, replacement)

with open("app/src/main/java/com/example/ui/components/MiniPlayer.kt", "w") as f:
    f.write(content)
