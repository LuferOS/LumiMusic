import re

with open("app/src/main/java/com/example/ui/screens/LocalMusicScreen.kt", "r") as f:
    content = f.read()

target = """fun LocalMusicScreen(
    viewModel: LocalMusicViewModel,
    controller: MediaController?,
    dominantColor: Color?
) {"""

replacement = """import com.example.viewmodel.MainViewModel

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun LocalMusicScreen(
    viewModel: LocalMusicViewModel,
    mainViewModel: MainViewModel,
    controller: MediaController?,
    dominantColor: Color?
) {"""

content = content.replace(target, replacement)
# Avoid duplicating imports and @OptIn
content = content.replace("import com.example.viewmodel.MainViewModel\n\n@OptIn(ExperimentalMaterial3Api::class)\n@OptIn(ExperimentalMaterial3Api::class)", "import com.example.viewmodel.MainViewModel\n\n@OptIn(ExperimentalMaterial3Api::class)")

with open("app/src/main/java/com/example/ui/screens/LocalMusicScreen.kt", "w") as f:
    f.write(content)
