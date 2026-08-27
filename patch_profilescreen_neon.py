with open("app/src/main/java/com/example/ui/screens/ProfileScreen.kt", "r") as f:
    content = f.read()

target = """fun SettingItem(
    icon: androidx.compose.ui.graphics.vector.ImageVector,
    title: String,
    subtitle: String,
    onClick: () -> Unit
) {
    Row(
        modifier = Modifier
            .fillMaxWidth()
            .padding(horizontal = 16.dp, vertical = 4.dp)
            .clip(RoundedCornerShape(16.dp))
            .clickable(onClick = onClick)
            .padding(horizontal = 16.dp, vertical = 16.dp),"""

replacement = """fun SettingItem(
    icon: androidx.compose.ui.graphics.vector.ImageVector,
    title: String,
    subtitle: String,
    applyNeon: Boolean = false,
    neonColor: Color = Color.Cyan,
    onClick: () -> Unit
) {
    Row(
        modifier = Modifier
            .fillMaxWidth()
            .padding(horizontal = 16.dp, vertical = 4.dp)
            .neonGlow(color = neonColor, cornerRadius = 16.dp, enabled = applyNeon)
            .clip(RoundedCornerShape(16.dp))
            .clickable(onClick = onClick)
            .padding(horizontal = 16.dp, vertical = 16.dp),"""
            
content = content.replace(target, replacement)

# Update calls to SettingItem to pass neon params
content = content.replace(
    """                SettingItem(
                    icon = Icons.Rounded.Person,
                    title = "Cuenta",
                    subtitle = "${stats.userName} • Nivel: ${calculateLevel(stats.totalListeningSeconds)}",
                    onClick = { showEditDialog = true }
                )""",
    """                SettingItem(
                    icon = Icons.Rounded.Person,
                    title = "Cuenta",
                    subtitle = "${stats.userName} • Nivel: ${calculateLevel(stats.totalListeningSeconds)}",
                    applyNeon = applyNeon,
                    neonColor = dominantColor ?: Color.Cyan,
                    onClick = { showEditDialog = true }
                )"""
)

content = content.replace(
    """                SettingItem(
                    icon = Icons.Rounded.Palette,
                    title = "Apariencia y Tema",
                    subtitle = "Personalizar el diseño de la aplicación",
                    onClick = { showAppearanceDialog = true }
                )""",
    """                SettingItem(
                    icon = Icons.Rounded.Palette,
                    title = "Apariencia y Tema",
                    subtitle = "Personalizar el diseño de la aplicación",
                    applyNeon = applyNeon,
                    neonColor = dominantColor ?: Color.Magenta,
                    onClick = { showAppearanceDialog = true }
                )"""
)

content = content.replace(
    """                SettingItem(
                    icon = Icons.Rounded.Equalizer,
                    title = "Reproducción",
                    subtitle = "Ajustes de audio, ecualizador",
                    onClick = onOpenEqualizer
                )""",
    """                SettingItem(
                    icon = Icons.Rounded.Equalizer,
                    title = "Reproducción",
                    subtitle = "Ajustes de audio, ecualizador",
                    applyNeon = applyNeon,
                    neonColor = dominantColor ?: Color.Green,
                    onClick = onOpenEqualizer
                )"""
)

content = content.replace(
    """                SettingItem(
                    icon = Icons.Rounded.SwapHoriz,
                    title = "Transiciones (Crossfade)",
                    subtitle = "${stats.transitionType} - ${stats.transitionDuration}s",
                    onClick = { showTransitionsDialog = true }
                )""",
    """                SettingItem(
                    icon = Icons.Rounded.SwapHoriz,
                    title = "Transiciones (Crossfade)",
                    subtitle = "${stats.transitionType} - ${stats.transitionDuration}s",
                    applyNeon = applyNeon,
                    neonColor = dominantColor ?: Color.Yellow,
                    onClick = { showTransitionsDialog = true }
                )"""
)

content = content.replace(
    """                SettingItem(
                    icon = Icons.Rounded.Download,
                    title = "Estadísticas de reproducción",
                    subtitle = "${stats.totalDownloads} descargas • ${formatListeningTime(stats.totalListeningSeconds)}",
                    onClick = { }
                )""",
    """                SettingItem(
                    icon = Icons.Rounded.Download,
                    title = "Estadísticas de reproducción",
                    subtitle = "${stats.totalDownloads} descargas • ${formatListeningTime(stats.totalListeningSeconds)}",
                    applyNeon = applyNeon,
                    neonColor = dominantColor ?: Color.Blue,
                    onClick = { }
                )"""
)

content = content.replace(
    """                SettingItem(
                    icon = Icons.Rounded.Share,
                    title = "Invitar a amigos",
                    subtitle = "Comparte la aplicación APK",
                    onClick = { shareApk(context) }
                )""",
    """                SettingItem(
                    icon = Icons.Rounded.Share,
                    title = "Invitar a amigos",
                    subtitle = "Comparte la aplicación APK",
                    applyNeon = applyNeon,
                    neonColor = dominantColor ?: Color.Red,
                    onClick = { shareApk(context) }
                )"""
)

content = content.replace(
    """                SettingItem(
                    icon = Icons.Rounded.Delete,
                    title = "Borrar caché y datos",
                    subtitle = "Liberar espacio en el dispositivo",
                    onClick = {
                        CoroutineScope(Dispatchers.IO).launch {
                            viewModel.clearAllData()
                        }
                    }
                )""",
    """                SettingItem(
                    icon = Icons.Rounded.Delete,
                    title = "Borrar caché y datos",
                    subtitle = "Liberar espacio en el dispositivo",
                    applyNeon = applyNeon,
                    neonColor = dominantColor ?: Color.Gray,
                    onClick = {
                        CoroutineScope(Dispatchers.IO).launch {
                            viewModel.clearAllData()
                        }
                    }
                )"""
)


with open("app/src/main/java/com/example/ui/screens/ProfileScreen.kt", "w") as f:
    f.write(content)
