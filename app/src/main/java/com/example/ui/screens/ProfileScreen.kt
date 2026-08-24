package com.example.ui.screens

import androidx.core.content.FileProvider
import java.io.File
import java.io.FileInputStream
import java.io.FileOutputStream
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch

import android.content.Intent
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.verticalScroll
import androidx.compose.foundation.horizontalScroll
import androidx.compose.foundation.rememberScrollState
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.rounded.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import com.example.viewmodel.ProfileViewModel
import com.example.ui.theme.neonGlow

@OptIn(ExperimentalMaterial3Api::class)
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

    Column(
        modifier = Modifier
            .fillMaxSize()
            .padding(24.dp)
            .verticalScroll(rememberScrollState()),
        horizontalAlignment = Alignment.CenterHorizontally
    ) {
        Spacer(modifier = Modifier.height(32.dp))
        
        // Avatar
        Box(
            modifier = Modifier
                .size(120.dp)
                .clip(CircleShape)
                .background(dominantColor ?: MaterialTheme.colorScheme.primaryContainer)
                .neonGlow(dominantColor ?: MaterialTheme.colorScheme.primaryContainer, 60.dp, 40f, applyNeon),
            contentAlignment = Alignment.Center
        ) {
            Icon(
                imageVector = Icons.Rounded.Person,
                contentDescription = "Profile",
                modifier = Modifier.size(64.dp),
                tint = MaterialTheme.colorScheme.onPrimaryContainer
            )
        }
        Spacer(modifier = Modifier.height(16.dp))
        
        Text(
            text = stats.userName,
            style = MaterialTheme.typography.headlineMedium,
            fontWeight = FontWeight.Bold
        )
        Text(
            text = "API: ${stats.apiPreference}",
            style = MaterialTheme.typography.bodyLarge,
            color = MaterialTheme.colorScheme.onSurfaceVariant
        )
        
        Spacer(modifier = Modifier.height(16.dp))
        // Top Action Row
        Row(horizontalArrangement = Arrangement.spacedBy(8.dp), modifier = Modifier.horizontalScroll(rememberScrollState())) {
            Button(
                onClick = { showEditDialog = true },
                colors = ButtonDefaults.buttonColors(containerColor = dominantColor ?: MaterialTheme.colorScheme.primary),
                modifier = Modifier.neonGlow(dominantColor ?: MaterialTheme.colorScheme.primary, 24.dp, 20f, applyNeon)
            ) {
                Icon(Icons.Rounded.Edit, contentDescription = null, modifier = Modifier.size(18.dp))
                Spacer(modifier = Modifier.width(8.dp))
                Text("Edit Profile")
            }

            Button(
                onClick = { showAppearanceDialog = true },
                colors = ButtonDefaults.buttonColors(containerColor = MaterialTheme.colorScheme.secondary),
                modifier = Modifier.neonGlow(MaterialTheme.colorScheme.secondary, 24.dp, 20f, applyNeon)
            ) {
                Icon(Icons.Rounded.Palette, contentDescription = null, modifier = Modifier.size(18.dp))
                Spacer(modifier = Modifier.width(8.dp))
                Text("Theme")
            }
        }
        
        Spacer(modifier = Modifier.height(8.dp))
        // Bottom Action Row
        Row(horizontalArrangement = Arrangement.spacedBy(8.dp), modifier = Modifier.horizontalScroll(rememberScrollState())) {
            Button(
                onClick = onOpenEqualizer,
                colors = ButtonDefaults.buttonColors(containerColor = MaterialTheme.colorScheme.tertiary),
                modifier = Modifier.neonGlow(MaterialTheme.colorScheme.tertiary, 24.dp, 20f, applyNeon)
            ) {
                Icon(Icons.Rounded.GraphicEq, contentDescription = null, modifier = Modifier.size(18.dp))
                Spacer(modifier = Modifier.width(8.dp))
                Text("Equalizer")
            }
            
            Button(
                onClick = {
                    shareApk(context)
                },
                colors = ButtonDefaults.buttonColors(containerColor = Color(0xFF4CAF50)),
                modifier = Modifier.neonGlow(Color(0xFF4CAF50), 24.dp, 20f, applyNeon)
            ) {
                Icon(Icons.Rounded.Share, contentDescription = null, modifier = Modifier.size(18.dp))
                Spacer(modifier = Modifier.width(8.dp))
                Text("Share App (.APK)")
            }
        }

        Spacer(modifier = Modifier.height(32.dp))

        // Stats Grid
        Row(
            modifier = Modifier.fillMaxWidth(),
            horizontalArrangement = Arrangement.spacedBy(16.dp)
        ) {
            StatCard(
                title = "Listening Time",
                value = formatListeningTime(stats.totalListeningSeconds),
                icon = Icons.Rounded.Headphones,
                color = dominantColor ?: MaterialTheme.colorScheme.primary,
                applyNeon = applyNeon,
                modifier = Modifier.weight(1f)
            )
            StatCard(
                title = "Day Streak",
                value = "${stats.currentStreak} Days",
                icon = Icons.Rounded.LocalFireDepartment,
                color = Color(0xFFFF9800), // Fire color
                applyNeon = applyNeon,
                modifier = Modifier.weight(1f)
            )
        }
        
        Spacer(modifier = Modifier.height(16.dp))
        Row(
            modifier = Modifier.fillMaxWidth(),
            horizontalArrangement = Arrangement.spacedBy(16.dp)
        ) {
            StatCard(
                title = "Downloads",
                value = "${stats.totalDownloads} Tracks",
                icon = Icons.Rounded.Download,
                color = MaterialTheme.colorScheme.tertiary,
                applyNeon = applyNeon,
                modifier = Modifier.weight(1f)
            )
            StatCard(
                title = "Level",
                value = calculateLevel(stats.totalListeningSeconds),
                icon = Icons.Rounded.Star,
                color = Color(0xFFFFD700), // Gold
                applyNeon = applyNeon,
                modifier = Modifier.weight(1f)
            )
        }
        
        Spacer(modifier = Modifier.height(80.dp)) // Padding for bottom bar
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
                        label = { Text("Name") },
                        singleLine = true,
                        modifier = Modifier.fillMaxWidth()
                    )
                    Spacer(modifier = Modifier.height(16.dp))
                    Text("Preferred Download API", style = MaterialTheme.typography.labelLarge)
                    val apiOptions = listOf("YouTube", "Spotify", "Both")
                    apiOptions.forEach { apiOption ->
                        Row(
                            verticalAlignment = Alignment.CenterVertically,
                            modifier = Modifier.fillMaxWidth()
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
                }) {
                    Text("Save")
                }
            },
            dismissButton = {
                TextButton(onClick = { showEditDialog = false }) {
                    Text("Cancel")
                }
            }
        )
    }

    if (showAppearanceDialog) {
        var selectedPrimary by remember { mutableStateOf(stats.primaryColorHex) }
        var selectedBg by remember { mutableStateOf(stats.bgColorHex) }
        var selectedFont by remember { mutableStateOf(stats.fontPreference) }
        var isNeon by remember { mutableStateOf(stats.neonBorders) }
        var isExtract by remember { mutableStateOf(stats.extractAlbumColor) }

        val neonColors = listOf(
            "#00FFFF" to "Cyan",
            "#FF00FF" to "Magenta",
            "#00FF00" to "Lime",
            "#FF9800" to "Orange",
            "#E040FB" to "Purple"
        )
        val bgColors = listOf(
            "#000000" to "AMOLED Black",
            "#121212" to "Dark Gray"
        )
        val fonts = listOf("Default", "Serif", "Monospace", "Cursive")

        AlertDialog(
            onDismissRequest = { showAppearanceDialog = false },
            title = { Text("Appearance (Neon Mode)") },
            text = {
                Column(modifier = Modifier.verticalScroll(rememberScrollState())) {
                    Text("Accent Color", style = MaterialTheme.typography.labelLarge)
                    neonColors.forEach { (hex, name) ->
                        Row(verticalAlignment = Alignment.CenterVertically) {
                            RadioButton(selected = selectedPrimary == hex, onClick = { selectedPrimary = hex })
                            Text(name)
                        }
                    }
                    HorizontalDivider(modifier = Modifier.padding(vertical = 8.dp))
                    Text("Background", style = MaterialTheme.typography.labelLarge)
                    bgColors.forEach { (hex, name) ->
                        Row(verticalAlignment = Alignment.CenterVertically) {
                            RadioButton(selected = selectedBg == hex, onClick = { selectedBg = hex })
                            Text(name)
                        }
                    }
                    HorizontalDivider(modifier = Modifier.padding(vertical = 8.dp))
                    Text("Typography", style = MaterialTheme.typography.labelLarge)
                    fonts.forEach { font ->
                        Row(verticalAlignment = Alignment.CenterVertically) {
                            RadioButton(selected = selectedFont == font, onClick = { selectedFont = font })
                            Text(font)
                        }
                    }
                    HorizontalDivider(modifier = Modifier.padding(vertical = 8.dp))
                    Row(verticalAlignment = Alignment.CenterVertically) {
                        Checkbox(checked = isNeon, onCheckedChange = { isNeon = it })
                        Text("Enable Neon Glowing Borders")
                    }
                    Row(verticalAlignment = Alignment.CenterVertically) {
                        Checkbox(checked = isExtract, onCheckedChange = { isExtract = it })
                        Text("Dynamic Color from Album Art")
                    }
                }
            },
            confirmButton = {
                TextButton(onClick = {
                    viewModel.updateAppearance(selectedPrimary, selectedBg, selectedFont, isNeon, isExtract)
                    showAppearanceDialog = false
                }) {
                    Text("Apply")
                }
            },
            dismissButton = {
                TextButton(onClick = { showAppearanceDialog = false }) {
                    Text("Cancel")
                }
            }
        )
    }
}

@Composable
fun StatCard(
    title: String,
    value: String,
    icon: androidx.compose.ui.graphics.vector.ImageVector,
    color: Color,
    applyNeon: Boolean,
    modifier: Modifier = Modifier
) {
    Card(
        modifier = modifier
            .aspectRatio(1f)
            .neonGlow(color, 24.dp, 25f, applyNeon),
        shape = RoundedCornerShape(24.dp),
        colors = CardDefaults.cardColors(
            containerColor = MaterialTheme.colorScheme.surfaceVariant.copy(alpha = 0.5f)
        )
    ) {
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(16.dp),
            verticalArrangement = Arrangement.Center,
            horizontalAlignment = Alignment.CenterHorizontally
        ) {
            Icon(
                imageVector = icon,
                contentDescription = null,
                tint = color,
                modifier = Modifier.size(40.dp)
            )
            Spacer(modifier = Modifier.height(12.dp))
            Text(
                text = value,
                style = MaterialTheme.typography.titleLarge,
                fontWeight = FontWeight.Bold,
                color = color
            )
            Spacer(modifier = Modifier.height(4.dp))
            Text(
                text = title,
                style = MaterialTheme.typography.bodyMedium,
                color = MaterialTheme.colorScheme.onSurfaceVariant
            )
        }
    }
}

fun formatListeningTime(seconds: Long): String {
    val hours = seconds / 3600
    val minutes = (seconds % 3600) / 60
    return if (hours > 0) {
        "${hours}h ${minutes}m"
    } else {
        "${minutes}m"
    }
}

fun calculateLevel(seconds: Long): String {
    val hours = seconds / 3600
    return when {
        hours < 1 -> "Novice"
        hours < 10 -> "Explorer"
        hours < 50 -> "Fanatic"
        hours < 100 -> "Audiophile"
        else -> "Legend"
    }
}

fun shareApk(context: android.content.Context) {
    CoroutineScope(Dispatchers.IO).launch {
        try {
            val appInfo = context.applicationInfo
            val srcFile = File(appInfo.sourceDir)
            
            val cachePath = File(context.cacheDir, "shared_apks")
            if (!cachePath.exists()) {
                cachePath.mkdirs()
            }
            
            val destFile = File(cachePath, "LumiMusic.apk")
            
            // Copy APK to cache directory
            FileInputStream(srcFile).use { input ->
                FileOutputStream(destFile).use { output ->
                    input.copyTo(output)
                }
            }
            
            // Get URI using FileProvider
            val apkUri = FileProvider.getUriForFile(
                context,
                "${context.packageName}.fileprovider",
                destFile
            )
            
            val intent = Intent(Intent.ACTION_SEND).apply {
                type = "application/vnd.android.package-archive"
                putExtra(Intent.EXTRA_STREAM, apkUri)
                addFlags(Intent.FLAG_GRANT_READ_URI_PERMISSION)
                addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
            }
            
            context.startActivity(Intent.createChooser(intent, "Share Application APK").apply {
                addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
            })
            
        } catch (e: Exception) {
            e.printStackTrace()
        }
    }
}
