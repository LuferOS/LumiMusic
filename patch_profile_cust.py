import re

with open("app/src/main/java/com/example/ui/screens/ProfileScreen.kt", "r") as f:
    content = f.read()

if "var showCustomizationDialog by remember" not in content:
    content = content.replace(
        "var showCreditsDialog by remember { mutableStateOf(false) }",
        "var showCreditsDialog by remember { mutableStateOf(false) }\n    var showCustomizationDialog by remember { mutableStateOf(false) }"
    )

target_item = """                SettingItem(
                    icon = Icons.Rounded.Equalizer,
                    title = "Efectos de Audio",
                    subtitle = "Ajusta graves y ecualizador",
                    onClick = onOpenEqualizer
                )"""

replacement_item = """                SettingItem(
                    icon = Icons.Rounded.Equalizer,
                    title = "Efectos de Audio",
                    subtitle = "Ajusta graves y ecualizador",
                    onClick = onOpenEqualizer
                )
                SettingItem(
                    icon = Icons.Rounded.DashboardCustomize,
                    title = "Personalización Visual",
                    subtitle = "Visualizador, Fuentes, Inicio",
                    onClick = { showCustomizationDialog = true }
                )"""

content = content.replace(target_item, replacement_item)

dialog_code = """
    if (showCustomizationDialog) {
        com.example.ui.components.CustomizationDialog(
            userStats = userStats,
            onDismiss = { showCustomizationDialog = false },
            onSave = { tab, order, font, vType, vColor ->
                viewModel.updateCustomization(tab, order, font, vType, vColor)
            }
        )
    }"""

content = content.replace("    if (showCreditsDialog) {", dialog_code + "\n    if (showCreditsDialog) {")

if "import androidx.compose.material.icons.rounded.DashboardCustomize" not in content:
    content = content.replace("import androidx.compose.material.icons.rounded.Delete", "import androidx.compose.material.icons.rounded.Delete\nimport androidx.compose.material.icons.rounded.DashboardCustomize")

with open("app/src/main/java/com/example/ui/screens/ProfileScreen.kt", "w") as f:
    f.write(content)
