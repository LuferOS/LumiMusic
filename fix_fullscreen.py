import re

with open("app/src/main/java/com/example/ui/components/FullScreenPlayer.kt", "r") as f:
    content = f.read()

# Fix OptIn
content = content.replace("@OptIn(ExperimentalMaterial3Api::class)\n@OptIn(androidx.compose.animation.ExperimentalSharedTransitionApi::class)", "@OptIn(ExperimentalMaterial3Api::class, androidx.compose.animation.ExperimentalSharedTransitionApi::class)")

with open("app/src/main/java/com/example/ui/components/FullScreenPlayer.kt", "w") as f:
    f.write(content)
