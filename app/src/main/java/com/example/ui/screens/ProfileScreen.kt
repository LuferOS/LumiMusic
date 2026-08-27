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
import com.example.utils.bouncyClick

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
    var showTransitionsDialog by remember { mutableStateOf(false) }
    var showCreditsDialog by remember { mutableStateOf(false) }
    var showCustomizationDialog by remember { mutableStateOf(false) }
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

                Text(
                    text = "Configuración",
                    style = MaterialTheme.typography.titleLarge,
                    fontWeight = FontWeight.Bold,
                    color = Color.White,
                    modifier = Modifier.weight(1f),
                    textAlign = androidx.compose.ui.text.style.TextAlign.Center
                )

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
                    applyNeon = applyNeon,
                    neonColor = dominantColor ?: Color.Cyan,
                    onClick = { showEditDialog = true }
                )
                SettingItem(
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
                )
                SettingItem(
                    icon = Icons.Rounded.Equalizer,
                    title = "Reproducción",
                    subtitle = "Ajustes de audio, ecualizador",
                    applyNeon = applyNeon,
                    neonColor = dominantColor ?: Color.Green,
                    onClick = onOpenEqualizer
                )
                SettingItem(
                    icon = Icons.Rounded.SwapHoriz,
                    title = "Transiciones (Crossfade)",
                    subtitle = "${stats.transitionType} - ${stats.transitionDuration}s",
                    applyNeon = applyNeon,
                    neonColor = dominantColor ?: Color.Yellow,
                    onClick = { showTransitionsDialog = true }
                )
                SettingItem(
                    icon = Icons.Rounded.Download,
                    title = "Estadísticas de reproducción",
                    subtitle = "${stats.totalDownloads} descargas • ${formatListeningTime(stats.totalListeningSeconds)}",
                    applyNeon = applyNeon,
                    neonColor = dominantColor ?: Color.Blue,
                    onClick = { }
                )
                SettingItem(
                    icon = Icons.Rounded.Share,
                    title = "Invitar a amigos",
                    subtitle = "Comparte la aplicación APK",
                    applyNeon = applyNeon,
                    neonColor = dominantColor ?: Color.Red,
                    onClick = { shareApk(context) }
                )
                
                SettingItem(
                    icon = Icons.Rounded.Delete,
                    title = "Limpiar Caché",
                    subtitle = "Libera espacio borrando música temporal",
                    applyNeon = applyNeon,
                    neonColor = dominantColor ?: Color.Gray,
                    onClick = {
                        viewModel.clearCache(context)
                        android.widget.Toast.makeText(context, "Caché limpiada correctamente", android.widget.Toast.LENGTH_SHORT).show()
                    }
                )
                
                Spacer(modifier = Modifier.height(16.dp))
                
                SettingItem(
                    icon = Icons.Rounded.Info,
                    title = "Créditos e Información",
                    subtitle = "Versión, desarrolladores y API",
                    applyNeon = applyNeon,
                    neonColor = dominantColor ?: Color.White,
                    onClick = { showCreditsDialog = true }
                )
                Spacer(modifier = Modifier.height(32.dp))
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
                    Text("Motor de Descarga / Reproducción", style = MaterialTheme.typography.labelLarge)
                    Row(verticalAlignment = Alignment.CenterVertically, modifier = Modifier.fillMaxWidth().clickable { apiPref = "Spotify" }) {
                        RadioButton(selected = apiPref == "Spotify", onClick = { apiPref = "Spotify" })
                        Text("Spotify")
                    }
                    Row(verticalAlignment = Alignment.CenterVertically, modifier = Modifier.fillMaxWidth().clickable { apiPref = "YouTube" }) {
                        RadioButton(selected = apiPref == "YouTube", onClick = { apiPref = "YouTube" })
                        Text("YouTube")
                    }
                    Row(verticalAlignment = Alignment.CenterVertically, modifier = Modifier.fillMaxWidth().clickable { apiPref = "Both" }) {
                        RadioButton(selected = apiPref == "Both", onClick = { apiPref = "Both" })
                        Text("Ambas (Automático)")
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

    if (showTransitionsDialog) {
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

    if (showAppearanceDialog) {
        var selectedPrimary by remember { mutableStateOf(stats.primaryColorHex) }
        var selectedBg by remember { mutableStateOf(stats.bgColorHex) }
        var selectedFont by remember { mutableStateOf(stats.fontPreference) }
        var isNeon by remember { mutableStateOf(stats.neonBorders) }
        var isExtract by remember { mutableStateOf(stats.extractAlbumColor) }
        var isShowSpectrums by remember { mutableStateOf(stats.showSpectrums) }
        
        val neonColors = listOf(
            "#00FFFF" to "Cyan", "#FF00FF" to "Magenta", "#00FF00" to "Lime", 
            "#FF9800" to "Naranja", "#E040FB" to "Púrpura", "#F44336" to "Rojo", 
            "#2196F3" to "Azul", "#FFEB3B" to "Amarillo", "#E91E63" to "Rosa"
        )
        val bgColors = listOf("#000000" to "AMOLED Black", "#121212" to "Dark Gray")
        val fonts = listOf("Default", "Serif", "Monospace", "Cursive", "Sans-Serif")
        
        AlertDialog(
            onDismissRequest = { showAppearanceDialog = false },
            title = { Text("Apariencia") },
            text = {
                Column(modifier = Modifier.verticalScroll(rememberScrollState())) {
                    Text("Color de Acento", style = MaterialTheme.typography.labelLarge)
                    
                    // Chip selection for neon colors
                    androidx.compose.foundation.lazy.LazyRow(modifier = Modifier.fillMaxWidth().padding(vertical = 8.dp), horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                        items(neonColors.size) { index ->
                            val colorData = neonColors[index]
                            androidx.compose.material3.FilterChip(
                                selected = selectedPrimary == colorData.first,
                                onClick = { selectedPrimary = colorData.first },
                                label = { Text(colorData.second) }
                            )
                        }
                    }
                    
                    HorizontalDivider(modifier = Modifier.padding(vertical = 8.dp))
                    
                    Text("Tipografía de la App", style = MaterialTheme.typography.labelLarge)
                    androidx.compose.foundation.lazy.LazyRow(modifier = Modifier.fillMaxWidth().padding(vertical = 8.dp), horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                        items(fonts.size) { index ->
                            val fName = fonts[index]
                            androidx.compose.material3.FilterChip(
                                selected = selectedFont == fName,
                                onClick = { selectedFont = fName },
                                label = { Text(fName) }
                            )
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
                    Row(verticalAlignment = Alignment.CenterVertically, modifier = Modifier.fillMaxWidth().clickable { isShowSpectrums = !isShowSpectrums }) {
                        Checkbox(checked = isShowSpectrums, onCheckedChange = { isShowSpectrums = it })
                        Text("Animaciones y Espectros")
                    }
                }
            },
            confirmButton = {
                TextButton(onClick = {
                    viewModel.updateAppearance(selectedPrimary, selectedBg, selectedFont, isNeon, isExtract)
                    viewModel.updateShowSpectrums(isShowSpectrums)
                    showAppearanceDialog = false
                }) { Text("Aplicar") }
            },
            dismissButton = {
                TextButton(onClick = { showAppearanceDialog = false }) { Text("Cancelar") }
            }
        )
    }


    if (showCustomizationDialog) {
        com.example.ui.components.CustomizationDialog(
            userStats = stats,
            onDismiss = { showCustomizationDialog = false },
            onSave = { tab, order, font, vType, vColor ->
                viewModel.updateCustomization(tab, order, font, vType, vColor)
            }
        )
    }
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
                        text = "LumiMusic v${com.example.BuildConfig.VERSION_NAME}",
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
                        text = "IMPULSADO POR ALYA CORE API\nGRACIAS ANDER POR TU API ❤️\u200D\uD83E\uDE79",
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
}

@Composable
fun SettingItem(
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
            .bouncyClick(onClick = onClick)
            .padding(horizontal = 16.dp, vertical = 16.dp),
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
