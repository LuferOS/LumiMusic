import re

with open("app/src/main/java/com/example/ui/components/MiniPlayer.kt", "r") as f:
    content = f.read()

imports = """import androidx.compose.ui.platform.LocalView
import android.view.HapticFeedbackConstants"""

if "LocalView" not in content:
    content = content.replace("import androidx.compose.ui.unit.dp", "import androidx.compose.ui.unit.dp\n" + imports)

target_start = """fun MiniPlayer(
    controller: MediaController?,
    dominantColor: Color?,
    viewModel: MainViewModel,
    onExpand: () -> Unit
) {
    if (controller == null) return"""

replacement_start = """fun MiniPlayer(
    controller: MediaController?,
    dominantColor: Color?,
    viewModel: MainViewModel,
    onExpand: () -> Unit
) {
    if (controller == null) return
    val view = LocalView.current"""

content = content.replace(target_start, replacement_start)

# Modify clickable
content = content.replace(".clickable { onExpand() }", ".clickable { view.performHapticFeedback(HapticFeedbackConstants.VIRTUAL_KEY); onExpand() }")

# Modify Like button
content = content.replace("""                    IconButton(onClick = {
                        viewModel.toggleLike(currentUri, currentTitle, currentArtist, artworkUri?.toString())
                    })""", """                    IconButton(onClick = {
                        view.performHapticFeedback(HapticFeedbackConstants.VIRTUAL_KEY)
                        viewModel.toggleLike(currentUri, currentTitle, currentArtist, artworkUri?.toString())
                    })""")

# Modify Play/Pause
content = content.replace("""                    IconButton(onClick = {
                        if (isPlaying) controller.pause() else controller.play()
                    })""", """                    IconButton(onClick = {
                        view.performHapticFeedback(HapticFeedbackConstants.VIRTUAL_KEY)
                        if (isPlaying) controller.pause() else controller.play()
                    })""")


with open("app/src/main/java/com/example/ui/components/MiniPlayer.kt", "w") as f:
    f.write(content)
