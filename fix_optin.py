import re

with open("app/src/main/java/com/example/MainActivity.kt", "r") as f:
    content = f.read()

content = content.replace("@OptIn(ExperimentalMaterial3Api::class)\n@Composable\nfun MainScreen(", "@OptIn(ExperimentalMaterial3Api::class, androidx.compose.animation.ExperimentalSharedTransitionApi::class)\n@Composable\nfun MainScreen(")

with open("app/src/main/java/com/example/MainActivity.kt", "w") as f:
    f.write(content)
