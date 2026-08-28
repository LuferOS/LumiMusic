import re

with open('app/src/main/java/com/example/ui/components/PlayerArtwork.kt', 'r') as f:
    content = f.read()

# Make sure we add import for shadow
if 'import androidx.compose.ui.draw.shadow' not in content:
    content = content.replace('import androidx.compose.ui.draw.clip', 'import androidx.compose.ui.draw.clip\nimport androidx.compose.ui.draw.shadow')

# Add shadow when no neon border is present
# We replace:
#        val enhancedModifier = if (!isBatterySaverOn && neonBorders) {
#            baseModifier.neonGlow(color = dominantColor ?: Color.White, cornerRadius = 8.dp, enabled = true)
#        } else {
#            baseModifier
#        }
new_modifiers = """        val enhancedModifier = if (!isBatterySaverOn && neonBorders) {
            baseModifier.neonGlow(color = dominantColor ?: Color.White, cornerRadius = 24.dp, enabled = true)
        } else if (!isBatterySaverOn) {
            baseModifier.shadow(elevation = 24.dp, shape = RoundedCornerShape(24.dp), spotColor = dominantColor ?: Color.Black)
        } else {
            baseModifier
        }"""
        
content = re.sub(r'val enhancedModifier = if \(!isBatterySaverOn && neonBorders\) \{.*?(?=Box\()', new_modifiers + '\n\n        ', content, flags=re.DOTALL)

with open('app/src/main/java/com/example/ui/components/PlayerArtwork.kt', 'w') as f:
    f.write(content)
