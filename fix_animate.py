import re

with open("app/src/main/java/com/example/ui/components/FullScreenPlayer.kt", "r") as f:
    content = f.read()

content = content.replace("modifier = Modifier.animateContentSize()", "modifier = Modifier")

# Now add animateContentSize ONLY to the main Column
target_col = """        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(horizontal = 24.dp)
                .statusBarsPadding()
                .navigationBarsPadding(),
        ) {"""

replacement_col = """        Column(
            modifier = Modifier
                .fillMaxSize()
                .animateContentSize()
                .padding(horizontal = 24.dp)
                .statusBarsPadding()
                .navigationBarsPadding(),
        ) {"""

content = content.replace(target_col, replacement_col)

# Also need to import animateContentSize if it's missing
if "import androidx.compose.animation.animateContentSize" not in content:
    content = content.replace("import androidx.compose.animation.AnimatedVisibility", "import androidx.compose.animation.AnimatedVisibility\nimport androidx.compose.animation.animateContentSize")
if "import androidx.compose.animation.animateContentSize" not in content:
    # If AnimatedVisibility is missing
    content = content.replace("import androidx.compose.foundation.background", "import androidx.compose.animation.animateContentSize\nimport androidx.compose.foundation.background")

with open("app/src/main/java/com/example/ui/components/FullScreenPlayer.kt", "w") as f:
    f.write(content)
