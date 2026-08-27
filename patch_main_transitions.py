import re

with open("app/src/main/java/com/example/MainActivity.kt", "r") as f:
    content = f.read()

target = """                                        when (selectedTab) {
                                            0 -> MainScreen(
                                                viewModel = viewModel,
                                                profileViewModel = profileViewModel,
                                                controller = mediaController,
                                                onColorExtracted = { dominantColor = it },
                                                dominantColor = activeColor
                                            )
                                            1 -> com.example.ui.screens.LocalMusicScreen(
                                                viewModel = localMusicViewModel,
                                                mainViewModel = viewModel,
                                                controller = mediaController,
                                                dominantColor = activeColor
                                            )
                                            2 -> ProfileScreen(
                                                viewModel = profileViewModel,
                                                dominantColor = activeColor,
                                                onOpenEqualizer = { showEqualizer = true }
                                            )
                                        }"""

replacement = """                                        androidx.compose.animation.AnimatedContent(
                                            targetState = selectedTab,
                                            label = "tab_transition",
                                            transitionSpec = {
                                                androidx.compose.animation.fadeIn() togetherWith androidx.compose.animation.fadeOut()
                                            }
                                        ) { targetTab ->
                                            when (targetTab) {
                                                0 -> MainScreen(
                                                    viewModel = viewModel,
                                                    profileViewModel = profileViewModel,
                                                    controller = mediaController,
                                                    onColorExtracted = { dominantColor = it },
                                                    dominantColor = activeColor
                                                )
                                                1 -> com.example.ui.screens.LocalMusicScreen(
                                                    viewModel = localMusicViewModel,
                                                    mainViewModel = viewModel,
                                                    controller = mediaController,
                                                    dominantColor = activeColor
                                                )
                                                2 -> ProfileScreen(
                                                    viewModel = profileViewModel,
                                                    dominantColor = activeColor,
                                                    onOpenEqualizer = { showEqualizer = true }
                                                )
                                            }
                                        }"""

content = content.replace(target, replacement)
content = content.replace("import androidx.compose.animation.SharedTransitionLayout", "import androidx.compose.animation.SharedTransitionLayout\nimport androidx.compose.animation.togetherWith")
with open("app/src/main/java/com/example/MainActivity.kt", "w") as f:
    f.write(content)
