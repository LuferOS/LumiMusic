import re

with open("app/src/main/java/com/example/ui/screens/ProfileScreen.kt", "r") as f:
    content = f.read()

# Add showTransitionsDialog to the states at the top of ProfileScreen
state_target = """    var showEditDialog by remember { mutableStateOf(false) }
    var showAppearanceDialog by remember { mutableStateOf(false) }"""
state_replace = """    var showEditDialog by remember { mutableStateOf(false) }
    var showAppearanceDialog by remember { mutableStateOf(false) }
    var showTransitionsDialog by remember { mutableStateOf(false) }"""
content = content.replace(state_target, state_replace)

# Add SettingItem for Transitions
item_target = """                SettingItem(
                    icon = Icons.Rounded.Equalizer,
                    title = "Reproducción",
                    subtitle = "Ajustes de audio, ecualizador",
                    onClick = onOpenEqualizer
                )"""
item_replace = """                SettingItem(
                    icon = Icons.Rounded.Equalizer,
                    title = "Reproducción",
                    subtitle = "Ajustes de audio, ecualizador",
                    onClick = onOpenEqualizer
                )
                SettingItem(
                    icon = Icons.Rounded.SwapHoriz,
                    title = "Transiciones (Crossfade)",
                    subtitle = "${stats.transitionType} - ${stats.transitionDuration}s",
                    onClick = { showTransitionsDialog = true }
                )"""
content = content.replace(item_target, item_replace)

# Add Transitions Dialog
dialog_target = """    if (showAppearanceDialog) {"""
dialog_replace = """    if (showTransitionsDialog) {
        var selectedType by remember { mutableStateOf(stats.transitionType) }
        var selectedDuration by remember { mutableStateOf(stats.transitionDuration.toFloat()) }
        
        AlertDialog(
            onDismissRequest = { showTransitionsDialog = false },
            title = { Text("Transiciones de Audio") },
            text = {
                Column {
                    Text("Tipo de Transición", style = MaterialTheme.typography.labelLarge)
                    Row(verticalAlignment = Alignment.CenterVertically, modifier = Modifier.fillMaxWidth().clickable { selectedType = "None" }) {
                        RadioButton(selected = selectedType == "None", onClick = { selectedType = "None" })
                        Text("Ninguna (Pausa breve)")
                    }
                    Row(verticalAlignment = Alignment.CenterVertically, modifier = Modifier.fillMaxWidth().clickable { selectedType = "Gapless" }) {
                        RadioButton(selected = selectedType == "Gapless", onClick = { selectedType = "Gapless" })
                        Text("Gapless (Sin pausas)")
                    }
                    Row(verticalAlignment = Alignment.CenterVertically, modifier = Modifier.fillMaxWidth().clickable { selectedType = "Crossfade" }) {
                        RadioButton(selected = selectedType == "Crossfade", onClick = { selectedType = "Crossfade" })
                        Text("Crossfade (Fade In/Out)")
                    }
                    
                    if (selectedType == "Crossfade") {
                        Spacer(modifier = Modifier.height(16.dp))
                        Text("Duración: ${selectedDuration.toInt()} segundos", style = MaterialTheme.typography.labelLarge)
                        Slider(
                            value = selectedDuration,
                            onValueChange = { selectedDuration = it },
                            valueRange = 1f..10f,
                            steps = 8
                        )
                    }
                }
            },
            confirmButton = {
                TextButton(onClick = {
                    viewModel.updateTransitions(selectedType, selectedDuration.toInt())
                    showTransitionsDialog = false
                }) { Text("Guardar") }
            },
            dismissButton = {
                TextButton(onClick = { showTransitionsDialog = false }) { Text("Cancelar") }
            }
        )
    }

    if (showAppearanceDialog) {"""
content = content.replace(dialog_target, dialog_replace)

# Import SwapHoriz if not present
if "Icons.Rounded.SwapHoriz" in content and "SwapHoriz" not in content[:content.find("fun ProfileScreen")]:
    content = content.replace("import androidx.compose.material.icons.rounded.Share", "import androidx.compose.material.icons.rounded.Share\nimport androidx.compose.material.icons.rounded.SwapHoriz")


with open("app/src/main/java/com/example/ui/screens/ProfileScreen.kt", "w") as f:
    f.write(content)
