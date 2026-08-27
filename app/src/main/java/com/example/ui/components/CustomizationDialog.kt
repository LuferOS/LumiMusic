package com.example.ui.components
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
import androidx.compose.foundation.horizontalScroll

import androidx.compose.foundation.layout.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import com.example.data.local.UserStats

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun CustomizationDialog(
    userStats: UserStats,
    onDismiss: () -> Unit,
    onSave: (Int, String, String, String, String) -> Unit
) {
    var selectedTab by remember { mutableStateOf(userStats.startupTab) }
    var navOrder by remember { mutableStateOf(userStats.navOrder) }
    var playerFont by remember { mutableStateOf(userStats.playerFont) }
    var visualizerType by remember { mutableStateOf(userStats.visualizerType) }
    var visualizerColor by remember { mutableStateOf(userStats.visualizerColor) }

    val tabs = listOf("Online", "Local", "Perfil")
    val fonts = listOf("Default", "Serif", "Monospace", "Cursive", "Sans-Serif")
    val vTypes = listOf("Ondas", "Bloques", "Barras")
    val vColors = listOf("Dinámico", "#1DB954", "#FF5722", "#E91E63", "#00BCD4", "#9C27B0", "#FFEB3B", "#4CAF50", "#2196F3")

    AlertDialog(
        onDismissRequest = onDismiss,
        title = { Text("Personalización") },
        text = {
            Column(modifier = Modifier.fillMaxWidth().verticalScroll(rememberScrollState())) {
                Text("Pantalla de Inicio", style = MaterialTheme.typography.labelMedium)
                Row(modifier = Modifier.fillMaxWidth().horizontalScroll(rememberScrollState()), horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                    tabs.forEachIndexed { index, name ->
                        FilterChip(
                            selected = selectedTab == index,
                            onClick = { selectedTab = index },
                            label = { Text(name) }
                        )
                    }
                }
                


                Spacer(modifier = Modifier.height(16.dp))
                Text("Tipo de Visualizador", style = MaterialTheme.typography.labelMedium)
                Row(modifier = Modifier.fillMaxWidth().horizontalScroll(rememberScrollState()), horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                    vTypes.forEach { type ->
                        FilterChip(
                            selected = visualizerType == type,
                            onClick = { visualizerType = type },
                            label = { Text(type) }
                        )
                    }
                }

                Spacer(modifier = Modifier.height(16.dp))
                Text("Color del Visualizador", style = MaterialTheme.typography.labelMedium)
                Row(modifier = Modifier.fillMaxWidth().horizontalScroll(rememberScrollState()), horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                    vColors.forEach { color ->
                        FilterChip(
                            selected = visualizerColor == color,
                            onClick = { visualizerColor = color },
                            label = { Text(if (color == "Dinámico") "Auto" else "Color") }
                        )
                    }
                }
                
                Spacer(modifier = Modifier.height(16.dp))
                Text("Orden de Pestañas (Toca para rotar)", style = MaterialTheme.typography.labelMedium)
                val orderIndices = navOrder.split(",").mapNotNull { it.toIntOrNull() }
                Row(modifier = Modifier.fillMaxWidth().padding(top = 8.dp), horizontalArrangement = Arrangement.SpaceEvenly) {
                    orderIndices.forEach { tabIndex ->
                        val tabName = when (tabIndex) {
                            0 -> "Buscar"
                            1 -> "Local"
                            else -> "Perfil"
                        }
                        Button(onClick = {
                            val newList = orderIndices.toMutableList()
                            val i = newList.indexOf(tabIndex)
                            if (i < newList.size - 1) {
                                newList[i] = newList[i+1]
                                newList[i+1] = tabIndex
                            } else {
                                newList[newList.size - 1] = newList[0]
                                newList[0] = tabIndex
                            }
                            navOrder = newList.joinToString(",")
                        }, modifier = Modifier.weight(1f).padding(horizontal = 4.dp)) {
                            Text(tabName, maxLines = 1, overflow = androidx.compose.ui.text.style.TextOverflow.Ellipsis)
                        }
                    }
                }
            }
        },
        confirmButton = {
            TextButton(onClick = {
                onSave(selectedTab, navOrder, playerFont, visualizerType, visualizerColor)
                onDismiss()
            }) {
                Text("Guardar")
            }
        },
        dismissButton = {
            TextButton(onClick = onDismiss) {
                Text("Cancelar")
            }
        }
    )
}
