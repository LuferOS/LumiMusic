with open("app/src/main/java/com/example/ui/components/FullScreenPlayer.kt", "r") as f:
    content = f.read()

target = """            Spacer(modifier = Modifier.weight(0.3f))

            // Title & Artist Row"""

replacement = """            Spacer(modifier = Modifier.weight(0.15f))
            
            VisualizerView(
                isPlaying = isPlaying,
                visualizerType = userStats.visualizerType,
                primaryColor = if (userStats.visualizerColor == "Dinámico") (dominantColor ?: Color.White) else {
                    try { Color(android.graphics.Color.parseColor(userStats.visualizerColor)) } catch(e: Exception) { Color.White }
                },
                modifier = Modifier.padding(horizontal = 32.dp)
            )

            Spacer(modifier = Modifier.weight(0.15f))

            // Title & Artist Row"""
            
if "VisualizerView(" not in content:
    content = content.replace(target, replacement)
    with open("app/src/main/java/com/example/ui/components/FullScreenPlayer.kt", "w") as f:
        f.write(content)
