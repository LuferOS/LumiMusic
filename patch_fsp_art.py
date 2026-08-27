with open("app/src/main/java/com/example/ui/components/FullScreenPlayer.kt", "r") as f:
    content = f.read()

target = """                Box(
                    modifier = Modifier
                        .fillMaxWidth()
                        .aspectRatio(1f)
                        .clip(RoundedCornerShape(8.dp))
                        .background(Color.White.copy(alpha = 0.1f)),
                    contentAlignment = Alignment.Center
                ) {"""

replacement = """                Box(
                    modifier = Modifier
                        .fillMaxWidth()
                        .aspectRatio(1f)
                        .androidx.compose.ui.draw.shadow(
                            elevation = 24.dp,
                            shape = RoundedCornerShape(16.dp),
                            ambientColor = dominantColor ?: Color.Black,
                            spotColor = dominantColor ?: Color.Black
                        )
                        .clip(RoundedCornerShape(16.dp))
                        .background(Color.White.copy(alpha = 0.05f)),
                    contentAlignment = Alignment.Center
                ) {"""

if target in content:
    content = content.replace(target, replacement)
else:
    print("Could not find FullScreenPlayer art target")

with open("app/src/main/java/com/example/ui/components/FullScreenPlayer.kt", "w") as f:
    f.write(content)
