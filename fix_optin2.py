import re

with open("app/src/main/java/com/example/MainActivity.kt", "r") as f:
    content = f.read()

content = content.replace("class MainActivity : ComponentActivity() {", "@OptIn(androidx.compose.animation.ExperimentalSharedTransitionApi::class)\nclass MainActivity : ComponentActivity() {")

with open("app/src/main/java/com/example/MainActivity.kt", "w") as f:
    f.write(content)
