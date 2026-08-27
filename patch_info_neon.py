with open("app/src/main/java/com/example/ui/screens/ProfileScreen.kt", "r") as f:
    content = f.read()

target_info = """                SettingItem(
                    icon = Icons.Rounded.Info,
                    title = "Créditos e Información",
                    subtitle = "Versión, desarrolladores y API",
                    onClick = { showCreditsDialog = true }
                )"""
replacement_info = """                SettingItem(
                    icon = Icons.Rounded.Info,
                    title = "Créditos e Información",
                    subtitle = "Versión, desarrolladores y API",
                    applyNeon = applyNeon,
                    neonColor = dominantColor ?: Color.White,
                    onClick = { showCreditsDialog = true }
                )"""
content = content.replace(target_info, replacement_info)

with open("app/src/main/java/com/example/ui/screens/ProfileScreen.kt", "w") as f:
    f.write(content)
