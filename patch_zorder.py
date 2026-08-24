import re

with open("app/src/main/java/com/example/MainActivity.kt", "r") as f:
    content = f.read()

bad_surface = """                Surface(
                    modifier = Modifier.fillMaxSize(),
                    color = MaterialTheme.colorScheme.background
                ) {
                    var selectedTab by remember { mutableStateOf(0) }
                    var showEqualizer by remember { mutableStateOf(false) }

                    if (showFullScreenPlayer) {
                        val lyricsState by viewModel.lyricsState.collectAsStateWithLifecycle()
                        FullScreenPlayer(
                            controller = mediaController,
                            dominantColor = activeColor,
                            lyrics = lyricsState ?: "Loading...",
                            onClose = { showFullScreenPlayer = false }
                        )
                    }

                    if (showEqualizer) {
                        AudioSettingsBottomSheet(controller = mediaController) {
                            showEqualizer = false
                        }
                    }

                    Scaffold("""

fixed_surface = """                Surface(
                    modifier = Modifier.fillMaxSize(),
                    color = MaterialTheme.colorScheme.background
                ) {
                    var selectedTab by remember { mutableStateOf(0) }
                    var showEqualizer by remember { mutableStateOf(false) }

                    Box(modifier = Modifier.fillMaxSize()) {
                        Scaffold("""

content = content.replace(bad_surface, fixed_surface)

scaffold_end = """                        }
                    }
                }
            }
        }
    }
}

@Composable"""

fixed_end = """                        }
                    }
                    
                    if (showFullScreenPlayer) {
                        val lyricsState by viewModel.lyricsState.collectAsStateWithLifecycle()
                        FullScreenPlayer(
                            controller = mediaController,
                            dominantColor = activeColor,
                            lyrics = lyricsState ?: "Loading...",
                            onClose = { showFullScreenPlayer = false }
                        )
                    }

                    if (showEqualizer) {
                        AudioSettingsBottomSheet(controller = mediaController) {
                            showEqualizer = false
                        }
                    }
                }
            }
        }
    }
}

@Composable"""

content = content.replace(scaffold_end, fixed_end)

with open("app/src/main/java/com/example/MainActivity.kt", "w") as f:
    f.write(content)
