import re

with open("app/src/main/java/com/example/ui/screens/ProfileScreen.kt", "r") as f:
    content = f.read()

# Add state
if "var showCreditsDialog by remember" not in content:
    content = content.replace(
        "var showTransitionsDialog by remember { mutableStateOf(false) }",
        "var showTransitionsDialog by remember { mutableStateOf(false) }\n    var showCreditsDialog by remember { mutableStateOf(false) }"
    )

# Replace the text block
target_text_block = """                Column(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalAlignment = Alignment.CenterHorizontally
                ) {
                    Text(
                        text = "LumiMusic v1.0",
                        style = MaterialTheme.typography.bodyMedium,
                        color = Color.White.copy(alpha = 0.5f)
                    )
                    Text(
                        text = "IMPULSADO POR ALYA CORE API GRACIAS ANDER POR TU API❤️‍🩹",
                        style = MaterialTheme.typography.labelSmall,
                        color = Color.White.copy(alpha = 0.7f),
                        textAlign = androidx.compose.ui.text.style.TextAlign.Center,
                        modifier = Modifier.padding(vertical = 4.dp, horizontal = 16.dp)
                    )
                    Text(
                        text = "Creado por LuferOS",
                        style = MaterialTheme.typography.bodySmall,
                        color = Color.White.copy(alpha = 0.4f)
                    )
                    Text(
                        text = "Luis Fernando Guzmán Niño",
                        style = MaterialTheme.typography.bodySmall,
                        color = Color.White.copy(alpha = 0.4f)
                    )
                }"""

replacement_item = """                SettingItem(
                    icon = Icons.Rounded.Info,
                    title = "Créditos e Información",
                    subtitle = "Versión, desarrolladores y API",
                    onClick = { showCreditsDialog = true }
                )
                Spacer(modifier = Modifier.height(32.dp))"""

content = content.replace(target_text_block, replacement_item)

# Add the dialog at the end
dialog_code = """
    if (showCreditsDialog) {
        val uriHandler = androidx.compose.ui.platform.LocalUriHandler.current
        AlertDialog(
            onDismissRequest = { showCreditsDialog = false },
            title = { Text("Créditos e Información") },
            text = {
                Column(
                    horizontalAlignment = Alignment.CenterHorizontally,
                    modifier = Modifier.fillMaxWidth()
                ) {
                    Icon(
                        imageVector = Icons.Rounded.MusicNote,
                        contentDescription = null,
                        modifier = Modifier.size(48.dp),
                        tint = MaterialTheme.colorScheme.primary
                    )
                    Spacer(modifier = Modifier.height(16.dp))
                    Text(
                        text = "LumiMusic v1.0",
                        style = MaterialTheme.typography.titleLarge,
                        fontWeight = FontWeight.Bold,
                        color = MaterialTheme.colorScheme.onSurface
                    )
                    Spacer(modifier = Modifier.height(16.dp))
                    Text(
                        text = "Creado por LuferOS",
                        style = MaterialTheme.typography.bodyLarge,
                        color = MaterialTheme.colorScheme.onSurface
                    )
                    Text(
                        text = "Luis Fernando Guzmán Niño",
                        style = MaterialTheme.typography.bodyMedium,
                        color = MaterialTheme.colorScheme.onSurface.copy(alpha = 0.7f)
                    )
                    Spacer(modifier = Modifier.height(24.dp))
                    HorizontalDivider()
                    Spacer(modifier = Modifier.height(16.dp))
                    Text(
                        text = "IMPULSADO POR ALYA CORE API\\nGRACIAS ANDER POR TU API ❤️\\u200D\\uD83E\\uDE79",
                        style = MaterialTheme.typography.labelMedium,
                        color = MaterialTheme.colorScheme.onSurface.copy(alpha = 0.8f),
                        textAlign = androidx.compose.ui.text.style.TextAlign.Center
                    )
                    Spacer(modifier = Modifier.height(8.dp))
                    TextButton(onClick = { uriHandler.openUri("https://api.alyacore.xyz") }) {
                        Text("api.alyacore.xyz", color = MaterialTheme.colorScheme.primary)
                    }
                }
            },
            confirmButton = {
                TextButton(onClick = { showCreditsDialog = false }) { Text("Cerrar") }
            }
        )
    }
}""" # Replace closing bracket of ProfileScreen

content = content.replace("}\n\n@Composable\nfun SettingItem", dialog_code + "\n\n@Composable\nfun SettingItem")
if "import androidx.compose.material.icons.rounded.Info" not in content:
    content = content.replace("import androidx.compose.material.icons.rounded.Delete", "import androidx.compose.material.icons.rounded.Delete\nimport androidx.compose.material.icons.rounded.Info\nimport androidx.compose.material.icons.rounded.MusicNote")

with open("app/src/main/java/com/example/ui/screens/ProfileScreen.kt", "w") as f:
    f.write(content)
