import re

with open("app/src/main/java/com/example/MainActivity.kt", "r") as f:
    content = f.read()

target_mini = """                                    MiniPlayer(viewModel = viewModel, 
                                        controller = mediaController,
                                        dominantColor = activeColor,
                                        onExpand = {"""
replacement_mini = """                                    MiniPlayer(viewModel = viewModel, 
                                        controller = mediaController,
                                        dominantColor = activeColor,
                                        sharedTransitionScope = this@SharedTransitionLayout,
                                        onExpand = {"""
content = content.replace(target_mini, replacement_mini)

target_full = """                            FullScreenPlayer(viewModel = viewModel, 
                                controller = mediaController,
                                dominantColor = activeColor,
                                onClose = { showFullScreenPlayer = false }
                            )"""
replacement_full = """                            FullScreenPlayer(viewModel = viewModel, 
                                controller = mediaController,
                                dominantColor = activeColor,
                                sharedTransitionScope = this@SharedTransitionLayout,
                                animatedVisibilityScope = this,
                                onClose = { showFullScreenPlayer = false }
                            )"""
content = content.replace(target_full, replacement_full)

with open("app/src/main/java/com/example/MainActivity.kt", "w") as f:
    f.write(content)
