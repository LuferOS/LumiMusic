import re
with open("app/src/main/java/com/example/ui/components/FullScreenPlayer.kt", "r") as f:
    content = f.read()

# Add import
if "import com.example.ui.theme.neonGlow" not in content:
    content = content.replace("import com.example.viewmodel.MainViewModel", "import com.example.viewmodel.MainViewModel\nimport com.example.ui.theme.neonGlow")

target = """                    modifier = Modifier
                        .fillMaxWidth()
                        .aspectRatio(1f)
                        .sharedElement(
                            state = rememberSharedContentState(key = "album_art"),
                            animatedVisibilityScope = animatedVisibilityScope
                        )
                        .clip(RoundedCornerShape(8.dp))
                        .background(Color.White.copy(alpha = 0.1f)),"""

replacement = """                    modifier = Modifier
                        .fillMaxWidth()
                        .aspectRatio(1f)
                        .sharedElement(
                            state = rememberSharedContentState(key = "album_art"),
                            animatedVisibilityScope = animatedVisibilityScope
                        )
                        .neonGlow(color = dominantColor ?: Color.White, cornerRadius = 8.dp, enabled = userStats.neonBorders)
                        .clip(RoundedCornerShape(8.dp))
                        .background(Color.White.copy(alpha = 0.1f)),"""

content = content.replace(target, replacement)
with open("app/src/main/java/com/example/ui/components/FullScreenPlayer.kt", "w") as f:
    f.write(content)
