import re

with open("app/src/main/java/com/example/MainActivity.kt", "r") as f:
    content = f.read()

target = """                            val lyricsState by viewModel.lyricsState.collectAsStateWithLifecycle()
                            FullScreenPlayer(viewModel = viewModel, 
                                 controller = mediaController,
                                dominantColor = activeColor,
                                lyrics = lyricsState ?: "Loading...",
                                onClose = { showFullScreenPlayer = false }
                            )"""

replacement = """                            FullScreenPlayer(viewModel = viewModel, 
                                 controller = mediaController,
                                dominantColor = activeColor,
                                onClose = { showFullScreenPlayer = false }
                            )"""

content = content.replace(target, replacement)

with open("app/src/main/java/com/example/MainActivity.kt", "w") as f:
    f.write(content)
