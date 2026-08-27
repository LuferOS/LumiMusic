with open("app/src/main/java/com/example/MainActivity.kt", "r") as f:
    content = f.read()

target = """            MyApplicationTheme(
                primaryColorHex = userStats.primaryColorHex,
                fontPref = userStats.fontPreference,
                dynamicColor = false
            ) {"""

replacement = """            val updateInfo by mainViewModel.updateInfo.collectAsStateWithLifecycle()
            val context = androidx.compose.ui.platform.LocalContext.current

            MyApplicationTheme(
                primaryColorHex = userStats.primaryColorHex,
                fontPref = userStats.fontPreference,
                dynamicColor = false
            ) {
                if (updateInfo.isAvailable) {
                    AlertDialog(
                        onDismissRequest = { /* Force user to update or let them dismiss? Let them dismiss by changing state, but for simplicity let's use a local state to hide it */ },
                        title = { Text("Nueva versión detectada") },
                        text = { Text("Se ha detectado una nueva versión (${updateInfo.newVersion}) en GitHub.\\n\\n${updateInfo.releaseNotes}") },
                        confirmButton = {
                            Button(onClick = {
                                val intent = android.content.Intent(android.content.Intent.ACTION_VIEW, android.net.Uri.parse(updateInfo.updateUrl))
                                context.startActivity(intent)
                            }) {
                                Text("Actualizar")
                            }
                        },
                        dismissButton = {
                            var showDialog by remember { mutableStateOf(true) }
                            if (!showDialog) return@MyApplicationTheme // Quick hack to dismiss it? No, better to just have state.
                        }
                    )
                }"""

# Actually, to make it dismissible:
replacement = """            val updateInfo by mainViewModel.updateInfo.collectAsStateWithLifecycle()
            val context = androidx.compose.ui.platform.LocalContext.current
            var showUpdateDialog by remember { mutableStateOf(true) }

            MyApplicationTheme(
                primaryColorHex = userStats.primaryColorHex,
                fontPref = userStats.fontPreference,
                dynamicColor = false
            ) {
                if (updateInfo.isAvailable && showUpdateDialog) {
                    AlertDialog(
                        onDismissRequest = { showUpdateDialog = false },
                        title = { Text("Nueva versión detectada") },
                        text = { Text("Se ha detectado una nueva versión (${updateInfo.newVersion}) en GitHub.\\n\\n${updateInfo.releaseNotes}") },
                        confirmButton = {
                            Button(onClick = {
                                val intent = android.content.Intent(android.content.Intent.ACTION_VIEW, android.net.Uri.parse(updateInfo.updateUrl))
                                context.startActivity(intent)
                                showUpdateDialog = false
                            }) {
                                Text("Actualizar")
                            }
                        },
                        dismissButton = {
                            TextButton(onClick = { showUpdateDialog = false }) {
                                Text("Ignorar", color = MaterialTheme.colorScheme.onSurface.copy(alpha=0.7f))
                            }
                        },
                        containerColor = Color(0xFF1E1E1E),
                        titleContentColor = Color.White,
                        textContentColor = Color.White.copy(alpha=0.8f)
                    )
                }"""

content = content.replace(target, replacement)

with open("app/src/main/java/com/example/MainActivity.kt", "w") as f:
    f.write(content)
