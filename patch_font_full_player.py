with open("app/src/main/java/com/example/ui/components/FullScreenPlayer.kt", "r") as f:
    content = f.read()

target = """    val topColor = dominantColor ?: Color.DarkGray
    val bottomColor = Color(0xFF121212)
    
    Box("""

replacement = """    val topColor = dominantColor ?: Color.DarkGray
    val bottomColor = Color(0xFF121212)
    
    val customTypography = when (userStats.playerFont) {
        "Serif" -> androidx.compose.material3.Typography(
            displayLarge = androidx.compose.material3.MaterialTheme.typography.displayLarge.copy(fontFamily = androidx.compose.ui.text.font.FontFamily.Serif),
            titleLarge = androidx.compose.material3.MaterialTheme.typography.titleLarge.copy(fontFamily = androidx.compose.ui.text.font.FontFamily.Serif),
            bodyLarge = androidx.compose.material3.MaterialTheme.typography.bodyLarge.copy(fontFamily = androidx.compose.ui.text.font.FontFamily.Serif),
            bodyMedium = androidx.compose.material3.MaterialTheme.typography.bodyMedium.copy(fontFamily = androidx.compose.ui.text.font.FontFamily.Serif)
        )
        "Monospace" -> androidx.compose.material3.Typography(
            displayLarge = androidx.compose.material3.MaterialTheme.typography.displayLarge.copy(fontFamily = androidx.compose.ui.text.font.FontFamily.Monospace),
            titleLarge = androidx.compose.material3.MaterialTheme.typography.titleLarge.copy(fontFamily = androidx.compose.ui.text.font.FontFamily.Monospace),
            bodyLarge = androidx.compose.material3.MaterialTheme.typography.bodyLarge.copy(fontFamily = androidx.compose.ui.text.font.FontFamily.Monospace),
            bodyMedium = androidx.compose.material3.MaterialTheme.typography.bodyMedium.copy(fontFamily = androidx.compose.ui.text.font.FontFamily.Monospace)
        )
        "Cursive" -> androidx.compose.material3.Typography(
            displayLarge = androidx.compose.material3.MaterialTheme.typography.displayLarge.copy(fontFamily = androidx.compose.ui.text.font.FontFamily.Cursive),
            titleLarge = androidx.compose.material3.MaterialTheme.typography.titleLarge.copy(fontFamily = androidx.compose.ui.text.font.FontFamily.Cursive),
            bodyLarge = androidx.compose.material3.MaterialTheme.typography.bodyLarge.copy(fontFamily = androidx.compose.ui.text.font.FontFamily.Cursive),
            bodyMedium = androidx.compose.material3.MaterialTheme.typography.bodyMedium.copy(fontFamily = androidx.compose.ui.text.font.FontFamily.Cursive)
        )
        else -> androidx.compose.material3.MaterialTheme.typography
    }
    
    androidx.compose.material3.MaterialTheme(typography = customTypography) {
    Box("""

if "val customTypography" not in content:
    content = content.replace(target, replacement)
    
    # We also need to add a closing brace at the very end of the function!
    # Let's just do it string manipulation style:
    content = content + "\n    }\n"
    
    with open("app/src/main/java/com/example/ui/components/FullScreenPlayer.kt", "w") as f:
        f.write(content)
