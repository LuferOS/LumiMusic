import re

with open("app/src/main/java/com/example/MainActivity.kt", "r") as f:
    content = f.read()

# Fix imports
if "import com.example.ui.components.FullScreenPlayer" not in content:
    content = content.replace("import com.example.ui.components.MiniPlayer", "import com.example.ui.components.MiniPlayer\nimport com.example.ui.components.FullScreenPlayer")

# Modify state
old_state = "var showLyrics by remember { mutableStateOf(false) }"
new_state = """var showFullScreenPlayer by remember { mutableStateOf(false) }"""
content = content.replace(old_state, new_state)

# Replace LyricsBottomSheet usage
old_bottom_sheet = """                    if (showLyrics) {
                        LyricsBottomSheet(viewModel = viewModel) {
                            showLyrics = false
                        }
                    }"""

new_full_player = """                    if (showFullScreenPlayer) {
                        val lyricsState by viewModel.lyricsState.collectAsStateWithLifecycle()
                        FullScreenPlayer(
                            controller = mediaController,
                            dominantColor = activeColor,
                            lyrics = lyricsState ?: "Loading...",
                            onClose = { showFullScreenPlayer = false }
                        )
                    }"""

content = content.replace(old_bottom_sheet, new_full_player)

# Replace MiniPlayer call
old_mini_player = """                                MiniPlayer(
                                    controller = mediaController,
                                    dominantColor = activeColor,
                                    onShowLyrics = {
                                        val title = mediaController?.currentMediaItem?.mediaMetadata?.title?.toString()
                                        val artist = mediaController?.currentMediaItem?.mediaMetadata?.artist?.toString()
                                        if (!title.isNullOrBlank()) {
                                            viewModel.fetchLyrics(title, artist ?: "")
                                        }
                                        showLyrics = true
                                    }
                                )"""

new_mini_player = """                                MiniPlayer(
                                    controller = mediaController,
                                    dominantColor = activeColor,
                                    onExpand = {
                                        val title = mediaController?.currentMediaItem?.mediaMetadata?.title?.toString()
                                        val artist = mediaController?.currentMediaItem?.mediaMetadata?.artist?.toString()
                                        if (!title.isNullOrBlank()) {
                                            viewModel.fetchLyrics(title, artist ?: "")
                                        }
                                        showFullScreenPlayer = true
                                    }
                                )"""
content = content.replace(old_mini_player, new_mini_player)

with open("app/src/main/java/com/example/MainActivity.kt", "w") as f:
    f.write(content)
