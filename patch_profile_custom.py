with open("app/src/main/java/com/example/ui/screens/ProfileScreen.kt", "r") as f:
    content = f.read()

# Add Customization SettingItem
target_setting = """                SettingItem(
                    icon = Icons.Rounded.Palette,
                    title = "Apariencia y Tema",
                    subtitle = "Personalizar el diseño de la aplicación",
                    applyNeon = applyNeon,
                    neonColor = dominantColor ?: Color.Magenta,
                    onClick = { showAppearanceDialog = true }
                )"""

replacement_setting = """                SettingItem(
                    icon = Icons.Rounded.Palette,
                    title = "Apariencia y Tema",
                    subtitle = "Colores y bordes neón",
                    applyNeon = applyNeon,
                    neonColor = dominantColor ?: Color.Magenta,
                    onClick = { showAppearanceDialog = true }
                )
                SettingItem(
                    icon = Icons.Rounded.DashboardCustomize,
                    title = "Personalización Avanzada",
                    subtitle = "Pantalla de inicio, navegación y fuentes",
                    applyNeon = applyNeon,
                    neonColor = dominantColor ?: Color.Cyan,
                    onClick = { showCustomizationDialog = true }
                )"""

content = content.replace(target_setting, replacement_setting)

# Expand colors
target_colors = """val neonColors = listOf("#00FFFF" to "Cyan", "#FF00FF" to "Magenta", "#00FF00" to "Lime", "#FF9800" to "Orange", "#E040FB" to "Purple")"""
replacement_colors = """val neonColors = listOf(
            "#00FFFF" to "Cyan", "#FF00FF" to "Magenta", "#00FF00" to "Lime", 
            "#FF9800" to "Naranja", "#E040FB" to "Púrpura", "#F44336" to "Rojo", 
            "#2196F3" to "Azul", "#FFEB3B" to "Amarillo", "#E91E63" to "Rosa"
        )"""
content = content.replace(target_colors, replacement_colors)

with open("app/src/main/java/com/example/ui/screens/ProfileScreen.kt", "w") as f:
    f.write(content)
