with open("app/src/main/java/com/example/ui/components/MiniPlayer.kt", "r") as f:
    content = f.read()

target = """                .padding(horizontal = 8.dp, vertical = 4.dp)
                .clickable { view.performHapticFeedback(HapticFeedbackConstants.VIRTUAL_KEY); onExpand() },"""

replacement = """                .padding(horizontal = 8.dp, vertical = 4.dp)
                .neonGlow(color = dominantColor ?: Color.White, enabled = userStats.neonBorders)
                .clickable { view.performHapticFeedback(HapticFeedbackConstants.VIRTUAL_KEY); onExpand() },"""

content = content.replace(target, replacement)

with open("app/src/main/java/com/example/ui/components/MiniPlayer.kt", "w") as f:
    f.write(content)
