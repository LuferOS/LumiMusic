import re

with open("app/src/main/java/com/example/MainActivity.kt", "r") as f:
    content = f.read()

target = """                        if (showFullScreenPlayer) {
                            val lyricsState by viewModel.lyricsState.collectAsStateWithLifecycle()
                            FullScreenPlayer(viewModel = viewModel, 
                                controller = mediaController,
                                dominantColor = activeColor,
                                lyrics = lyricsState ?: "Loading...",
                                onClose = { showFullScreenPlayer = false }
                            )
                        }"""

replacement = """                        androidx.compose.animation.AnimatedVisibility(
                            visible = showFullScreenPlayer,
                            enter = androidx.compose.animation.slideInVertically(
                                initialOffsetY = { it }
                            ),
                            exit = androidx.compose.animation.slideOutVertically(
                                targetOffsetY = { it }
                            )
                        ) {
                            val lyricsState by viewModel.lyricsState.collectAsStateWithLifecycle()
                            FullScreenPlayer(viewModel = viewModel, 
                                controller = mediaController,
                                dominantColor = activeColor,
                                lyrics = lyricsState ?: "Loading...",
                                onClose = { showFullScreenPlayer = false }
                            )
                        }"""
content = content.replace(target, replacement)

with open("app/src/main/java/com/example/MainActivity.kt", "w") as f:
    f.write(content)
