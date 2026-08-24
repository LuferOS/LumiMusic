import re

with open("app/src/main/java/com/example/ui/screens/LocalMusicScreen.kt", "r") as f:
    content = f.read()

target = """        LazyColumn(
            modifier = Modifier.fillMaxSize(),
            contentPadding = PaddingValues(bottom = 100.dp) // Space for MiniPlayer
        ) {
            // First item: Liked Songs
            var showingLiked by remember { mutableStateOf(false) }"""

replacement = """        var showingLiked by remember { mutableStateOf(false) }
        LazyColumn(
            modifier = Modifier.fillMaxSize(),
            contentPadding = PaddingValues(bottom = 100.dp) // Space for MiniPlayer
        ) {
            // First item: Liked Songs"""

content = content.replace(target, replacement)

with open("app/src/main/java/com/example/ui/screens/LocalMusicScreen.kt", "w") as f:
    f.write(content)
