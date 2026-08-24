import re

with open("app/src/main/java/com/example/ui/screens/ProfileScreen.kt", "r") as f:
    content = f.read()

# Replace the ProfileScreen function content
start_idx = content.find("@OptIn(ExperimentalMaterial3Api::class)")
end_idx = content.find("@Composable\nfun StatCard(")

new_profile_screen = """@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun ProfileScreen(
    viewModel: ProfileViewModel,
    dominantColor: Color?,
    onOpenEqualizer: () -> Unit
) {
    val stats by viewModel.userStats.collectAsStateWithLifecycle()
    var showEditDialog by remember { mutableStateOf(false) }
    var showAppearanceDialog by remember { mutableStateOf(false) }
    val context = LocalContext.current
    val applyNeon = stats.neonBorders

    BoxWithConstraints(modifier = Modifier.fillMaxSize()) {
        val isWideScreen = maxWidth >= 600.dp
        
        Column(
            modifier = Modifier
                .fillMaxSize()
                .background(MaterialTheme.colorScheme.background)
        ) {
            TopAppBar(
                title = { Text("Settings", fontWeight = FontWeight.Bold) },
                colors = TopAppBarDefaults.topAppBarColors(containerColor = Color.Transparent)
            )

            Column(
                modifier = Modifier
                    .fillMaxSize()
                    .widthIn(max = 800.dp)
                    .align(Alignment.CenterHorizontally)
                    .verticalScroll(rememberScrollState())
            ) {
                // Profile Section
                Row(
                    modifier = Modifier
                        .fillMaxWidth()
                        .padding(24.dp),
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    Box(
                        modifier = Modifier
                            .size(80.dp)
                            .clip(CircleShape)
                            .background(dominantColor ?: MaterialTheme.colorScheme.primaryContainer)
                            .neonGlow(dominantColor ?: MaterialTheme.colorScheme.primaryContainer, 20.dp, 20f, applyNeon)
                            .clickable { showEditDialog = true },
                        contentAlignment = Alignment.Center
                    ) {
                        Icon(
                            imageVector = Icons.Rounded.Person,
                            contentDescription = "Profile",
                            modifier = Modifier.size(40.dp),
                            tint = MaterialTheme.colorScheme.onPrimaryContainer
                        )
                    }
                    
                    Spacer(modifier = Modifier.width(24.dp))
                    
                    Column(modifier = Modifier.weight(1f)) {
                        Text(
                            text = stats.userName,
                            style = MaterialTheme.typography.headlineSmall,
                            fontWeight = FontWeight.Bold
                        )
                        Text(
                            text = "Level: ${calculateLevel(stats.listeningTime)}",
                            style = MaterialTheme.typography.bodyMedium,
                            color = MaterialTheme.colorScheme.onSurfaceVariant
                        )
                    }
                    
                    IconButton(onClick = { showEditDialog = true }) {
                        Icon(Icons.Rounded.Edit, contentDescription = "Edit Profile")
                    }
                }
                
                // Stats Grid
                Text(
                    text = "Statistics",
                    style = MaterialTheme.typography.titleMedium,
                    color = MaterialTheme.colorScheme.primary,
                    modifier = Modifier.padding(horizontal = 24.dp, vertical = 8.dp)
                )
                
                Row(
                    modifier = Modifier
                        .fillMaxWidth()
                        .padding(horizontal = 24.dp),
                    horizontalArrangement = Arrangement.spacedBy(16.dp)
                ) {
                    StatCard(
                        title = "Listening Time",
                        value = formatListeningTime(stats.listeningTime),
                        icon = Icons.Rounded.Headphones,
                        color = MaterialTheme.colorScheme.primary,
                        applyNeon = applyNeon,
                        modifier = Modifier.weight(1f)
                    )
                    StatCard(
                        title = "Songs Downloaded",
                        value = stats.songsDownloaded.toString(),
                        icon = Icons.Rounded.Download,
                        color = MaterialTheme.colorScheme.secondary,
                        applyNeon = applyNeon,
                        modifier = Modifier.weight(1f)
                    )
                }
                
                Spacer(modifier = Modifier.height(24.dp))
                HorizontalDivider(modifier = Modifier.padding(horizontal = 24.dp))
                Spacer(modifier = Modifier.height(16.dp))

                // Preferences
                Text(
                    text = "Preferences",
                    style = MaterialTheme.typography.titleMedium,
                    color = MaterialTheme.colorScheme.primary,
                    modifier = Modifier.padding(horizontal = 24.dp, vertical = 8.dp)
                )
                
                SettingItem(
                    icon = Icons.Rounded.Search,
                    title = "Preferred Download API",
                    subtitle = stats.apiPreference,
                    onClick = { showEditDialog = true }
                )
                
                SettingItem(
                    icon = Icons.Rounded.Palette,
                    title = "Appearance & Theme",
                    subtitle = "Customize colors, typography and neon borders",
                    onClick = { showAppearanceDialog = true }
                )
                
                SettingItem(
                    icon = Icons.Rounded.GraphicEq,
                    title = "Audio Equalizer",
                    subtitle = "Adjust frequencies and bass boost",
                    onClick = onOpenEqualizer
                )
                
                SettingItem(
                    icon = Icons.Rounded.Share,
                    title = "Share Application",
                    subtitle = "Send the APK to a friend",
                    onClick = { shareApk(context) }
                )
                
                Spacer(modifier = Modifier.height(120.dp)) // padding for bottom bar
            }
        }
    }

    if (showEditDialog) {
        var newName by remember { mutableStateOf(stats.userName) }
        var selectedApi by remember { mutableStateOf(stats.apiPreference) }
        
        AlertDialog(
            onDismissRequest = { showEditDialog = false },
            title = { Text("Edit Profile & Settings") },
            text = {
                Column {
                    OutlinedTextField(
                        value = newName,
                        onValueChange = { newName = it },
                        label = { Text("Display Name") },
                        modifier = Modifier.fillMaxWidth()
                    )
                    Spacer(modifier = Modifier.height(16.dp))
                    Text("Preferred Download API", style = MaterialTheme.typography.labelLarge)
                    val apiOptions = listOf("YouTube", "Spotify", "Both")
                    apiOptions.forEach { apiOption ->
                        Row(
                            verticalAlignment = Alignment.CenterVertically,
                            modifier = Modifier.fillMaxWidth().clickable { selectedApi = apiOption }
                        ) {
                            RadioButton(
                                selected = selectedApi == apiOption,
                                onClick = { selectedApi = apiOption }
                            )
                            Text(text = apiOption, modifier = Modifier.padding(start = 8.dp))
                        }
                    }
                }
            },
            confirmButton = {
                TextButton(onClick = {
                    viewModel.updateProfile(newName, selectedApi)
                    showEditDialog = false
                }) { Text("Save") }
            },
            dismissButton = {
                TextButton(onClick = { showEditDialog = false }) { Text("Cancel") }
            }
        )
    }

    if (showAppearanceDialog) {
        var selectedPrimary by remember { mutableStateOf(stats.primaryColorHex) }
        var selectedBg by remember { mutableStateOf(stats.bgColorHex) }
        var selectedFont by remember { mutableStateOf(stats.fontPreference) }
        var isNeon by remember { mutableStateOf(stats.neonBorders) }
        var isExtract by remember { mutableStateOf(stats.extractAlbumColor) }
        
        val neonColors = listOf("#00FFFF" to "Cyan", "#FF00FF" to "Magenta", "#00FF00" to "Lime", "#FF9800" to "Orange", "#E040FB" to "Purple")
        val bgColors = listOf("#000000" to "AMOLED Black", "#121212" to "Dark Gray")
        val fonts = listOf("Default", "Serif", "Monospace", "Cursive")
        
        AlertDialog(
            onDismissRequest = { showAppearanceDialog = false },
            title = { Text("Appearance (Neon Mode)") },
            text = {
                Column(modifier = Modifier.verticalScroll(rememberScrollState())) {
                    Text("Accent Color", style = MaterialTheme.typography.labelLarge)
                    neonColors.forEach { (hex, name) ->
                        Row(verticalAlignment = Alignment.CenterVertically, modifier = Modifier.fillMaxWidth().clickable { selectedPrimary = hex }) {
                            RadioButton(selected = selectedPrimary == hex, onClick = { selectedPrimary = hex })
                            Text(name)
                        }
                    }
                    HorizontalDivider(modifier = Modifier.padding(vertical = 8.dp))
                    Text("Background", style = MaterialTheme.typography.labelLarge)
                    bgColors.forEach { (hex, name) ->
                        Row(verticalAlignment = Alignment.CenterVertically, modifier = Modifier.fillMaxWidth().clickable { selectedBg = hex }) {
                            RadioButton(selected = selectedBg == hex, onClick = { selectedBg = hex })
                            Text(name)
                        }
                    }
                    HorizontalDivider(modifier = Modifier.padding(vertical = 8.dp))
                    Text("Typography", style = MaterialTheme.typography.labelLarge)
                    fonts.forEach { font ->
                        Row(verticalAlignment = Alignment.CenterVertically, modifier = Modifier.fillMaxWidth().clickable { selectedFont = font }) {
                            RadioButton(selected = selectedFont == font, onClick = { selectedFont = font })
                            Text(font)
                        }
                    }
                    HorizontalDivider(modifier = Modifier.padding(vertical = 8.dp))
                    Row(verticalAlignment = Alignment.CenterVertically, modifier = Modifier.fillMaxWidth().clickable { isNeon = !isNeon }) {
                        Checkbox(checked = isNeon, onCheckedChange = { isNeon = it })
                        Text("Enable Neon Glowing Borders")
                    }
                    Row(verticalAlignment = Alignment.CenterVertically, modifier = Modifier.fillMaxWidth().clickable { isExtract = !isExtract }) {
                        Checkbox(checked = isExtract, onCheckedChange = { isExtract = it })
                        Text("Dynamic Color from Album Art")
                    }
                }
            },
            confirmButton = {
                TextButton(onClick = {
                    viewModel.updateAppearance(selectedPrimary, selectedBg, selectedFont, isNeon, isExtract)
                    showAppearanceDialog = false
                }) { Text("Apply") }
            },
            dismissButton = {
                TextButton(onClick = { showAppearanceDialog = false }) { Text("Cancel") }
            }
        )
    }
}

@Composable
fun SettingItem(
    icon: androidx.compose.ui.graphics.vector.ImageVector,
    title: String,
    subtitle: String,
    onClick: () -> Unit
) {
    Row(
        modifier = Modifier
            .fillMaxWidth()
            .clickable(onClick = onClick)
            .padding(horizontal = 24.dp, vertical = 16.dp),
        verticalAlignment = Alignment.CenterVertically
    ) {
        Icon(
            imageVector = icon,
            contentDescription = null,
            tint = MaterialTheme.colorScheme.onSurfaceVariant,
            modifier = Modifier.size(24.dp)
        )
        Spacer(modifier = Modifier.width(16.dp))
        Column(modifier = Modifier.weight(1f)) {
            Text(text = title, style = MaterialTheme.typography.titleMedium)
            Text(text = subtitle, style = MaterialTheme.typography.bodyMedium, color = MaterialTheme.colorScheme.onSurfaceVariant)
        }
        Icon(
            imageVector = Icons.Rounded.ChevronRight,
            contentDescription = null,
            tint = MaterialTheme.colorScheme.onSurfaceVariant
        )
    }
}
"""

content = content[:start_idx] + new_profile_screen + content[end_idx:]

# Need to ensure import of BoxWithConstraints
if "import androidx.compose.foundation.layout.BoxWithConstraints" not in content:
    content = content.replace("import androidx.compose.foundation.layout.*", "import androidx.compose.foundation.layout.*\nimport androidx.compose.foundation.layout.BoxWithConstraints")

with open("app/src/main/java/com/example/ui/screens/ProfileScreen.kt", "w") as f:
    f.write(content)
