import re

with open("app/src/main/java/com/example/ui/screens/ProfileScreen.kt", "r") as f:
    content = f.read()

new_content = """package com.example.ui.screens

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
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.BoxWithConstraints
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

    BoxWithConstraints(modifier = Modifier.fillMaxSize()) {
        Column(
            modifier = Modifier
                .fillMaxSize()
                .background(Color.Black)
        ) {
            // Header
            Row(
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(horizontal = 16.dp, vertical = 16.dp),
                verticalAlignment = Alignment.CenterVertically
            ) {
                IconButton(onClick = { /* Back */ }) {
                    Icon(Icons.Rounded.ArrowBack, contentDescription = "Back", tint = Color.White)
                }
                Text(
                    text = "Configuración",
                    style = MaterialTheme.typography.titleLarge,
                    fontWeight = FontWeight.Bold,
                    color = Color.White,
                    modifier = Modifier.weight(1f),
                    textAlign = androidx.compose.ui.text.style.TextAlign.Center
                )
                IconButton(onClick = { /* Search Settings */ }) {
                    Icon(Icons.Rounded.Search, contentDescription = "Search", tint = Color.White)
                }
            }

            Column(
                modifier = Modifier
                    .fillMaxSize()
                    .verticalScroll(rememberScrollState())
                    .padding(bottom = 100.dp)
            ) {
                SettingItem(
                    icon = Icons.Rounded.Person,
                    title = "Cuenta",
                    subtitle = "${stats.userName} • Nivel: ${calculateLevel(stats.totalListeningSeconds)}",
                    onClick = { showEditDialog = true }
                )
                SettingItem(
                    icon = Icons.Rounded.Palette,
                    title = "Apariencia y Tema",
                    subtitle = "Personalizar el diseño de la aplicación",
                    onClick = { showAppearanceDialog = true }
                )
                SettingItem(
                    icon = Icons.Rounded.Equalizer,
                    title = "Reproducción",
                    subtitle = "Ajustes de audio, ecualizador",
                    onClick = onOpenEqualizer
                )
                SettingItem(
                    icon = Icons.Rounded.Download,
                    title = "Estadísticas de reproducción",
                    subtitle = "${stats.totalDownloads} descargas • ${formatListeningTime(stats.totalListeningSeconds)}",
                    onClick = { }
                )
                SettingItem(
                    icon = Icons.Rounded.Share,
                    title = "Invitar a amigos",
                    subtitle = "Comparte la aplicación APK",
                    onClick = { shareApk(context) }
                )
            }
        }
    }

    if (showEditDialog) {
        var newName by remember { mutableStateOf(stats.userName) }
        var apiPref by remember { mutableStateOf(stats.apiPreference) }
        AlertDialog(
            onDismissRequest = { showEditDialog = false },
            title = { Text("Editar Perfil") },
            text = {
                Column {
                    OutlinedTextField(
                        value = newName,
                        onValueChange = { newName = it },
                        label = { Text("Nombre de usuario") },
                        modifier = Modifier.fillMaxWidth()
                    )
                    Spacer(modifier = Modifier.height(16.dp))
                    Text("API Preferida", style = MaterialTheme.typography.labelLarge)
                    Row(verticalAlignment = Alignment.CenterVertically) {
                        RadioButton(selected = apiPref == "itunes", onClick = { apiPref = "itunes" })
                        Text("iTunes (Rápido, 30s preview)")
                    }
                    Row(verticalAlignment = Alignment.CenterVertically) {
                        RadioButton(selected = apiPref == "youtube", onClick = { apiPref = "youtube" })
                        Text("YouTube (Audio completo)")
                    }
                }
            },
            confirmButton = {
                TextButton(onClick = {
                    viewModel.updateProfile(newName, apiPref)
                    showEditDialog = false
                }) { Text("Guardar") }
            },
            dismissButton = {
                TextButton(onClick = { showEditDialog = false }) { Text("Cancelar") }
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
            title = { Text("Apariencia") },
            text = {
                Column(modifier = Modifier.verticalScroll(rememberScrollState())) {
                    Text("Color de Acento", style = MaterialTheme.typography.labelLarge)
                    neonColors.forEach { (hex, name) ->
                        Row(verticalAlignment = Alignment.CenterVertically, modifier = Modifier.fillMaxWidth().clickable { selectedPrimary = hex }) {
                            RadioButton(selected = selectedPrimary == hex, onClick = { selectedPrimary = hex })
                            Text(name)
                        }
                    }
                    HorizontalDivider(modifier = Modifier.padding(vertical = 8.dp))
                    Row(verticalAlignment = Alignment.CenterVertically, modifier = Modifier.fillMaxWidth().clickable { isNeon = !isNeon }) {
                        Checkbox(checked = isNeon, onCheckedChange = { isNeon = it })
                        Text("Bordes de Neón")
                    }
                    Row(verticalAlignment = Alignment.CenterVertically, modifier = Modifier.fillMaxWidth().clickable { isExtract = !isExtract }) {
                        Checkbox(checked = isExtract, onCheckedChange = { isExtract = it })
                        Text("Color dinámico (Carátula)")
                    }
                }
            },
            confirmButton = {
                TextButton(onClick = {
                    viewModel.updateAppearance(selectedPrimary, selectedBg, selectedFont, isNeon, isExtract)
                    showAppearanceDialog = false
                }) { Text("Aplicar") }
            },
            dismissButton = {
                TextButton(onClick = { showAppearanceDialog = false }) { Text("Cancelar") }
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
            tint = Color.White,
            modifier = Modifier.size(24.dp)
        )
        Spacer(modifier = Modifier.width(16.dp))
        Column(modifier = Modifier.weight(1f)) {
            Text(text = title, style = MaterialTheme.typography.titleMedium, color = Color.White)
            Text(text = subtitle, style = MaterialTheme.typography.bodyMedium, color = Color.White.copy(alpha = 0.6f))
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
        hours < 1 -> "Novato"
        hours < 10 -> "Explorador"
        hours < 50 -> "Fanático"
        hours < 100 -> "Audiófilo"
        else -> "Leyenda"
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
            
            FileInputStream(srcFile).use { input ->
                FileOutputStream(destFile).use { output ->
                    input.copyTo(output)
                }
            }
            
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
            
            context.startActivity(Intent.createChooser(intent, "Compartir APK").apply {
                addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
            })
            
        } catch (e: Exception) {
            e.printStackTrace()
        }
    }
}
"""

with open("app/src/main/java/com/example/ui/screens/ProfileScreen.kt", "w") as f:
    f.write(new_content)
