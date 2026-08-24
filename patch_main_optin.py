import re

with open("app/src/main/java/com/example/MainActivity.kt", "r") as f:
    content = f.read()

target = "@androidx.media3.common.util.UnstableApi"
replacement = "@androidx.media3.common.util.UnstableApi\n@OptIn(androidx.compose.animation.ExperimentalSharedTransitionApi::class)"
if "@OptIn(androidx.compose.animation.ExperimentalSharedTransitionApi::class)" not in content:
    content = content.replace(target, replacement)

with open("app/src/main/java/com/example/MainActivity.kt", "w") as f:
    f.write(content)
