package com.example.ui.components

import androidx.compose.foundation.layout.*
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.rounded.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.media3.session.MediaController
import androidx.media3.common.PlaybackParameters
import androidx.compose.ui.platform.LocalView
import android.view.HapticFeedbackConstants
import androidx.compose.foundation.verticalScroll
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.background
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.ui.draw.clip
import androidx.compose.ui.draw.rotate
import androidx.compose.foundation.clickable
import androidx.compose.runtime.collectAsState
import com.example.player.AudioEffectManager

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun AudioSettingsBottomSheet(
    controller: MediaController?,
    onDismissRequest: () -> Unit
) {
    var speed by remember { mutableStateOf(controller?.playbackParameters?.speed ?: 1f) }
    var pitch by remember { mutableStateOf(controller?.playbackParameters?.pitch ?: 1f) }

    val eqState by AudioEffectManager.eqState.collectAsState()
    val view = LocalView.current
    
    ModalBottomSheet(onDismissRequest = onDismissRequest) {
        Column(
            modifier = Modifier
                .fillMaxWidth()
                .padding(horizontal = 24.dp, vertical = 16.dp)
                .verticalScroll(rememberScrollState()),
            horizontalAlignment = Alignment.CenterHorizontally
        ) {
            Icon(
                imageVector = Icons.Rounded.GraphicEq,
                contentDescription = null,
                modifier = Modifier.size(48.dp),
                tint = MaterialTheme.colorScheme.primary
            )
            Spacer(modifier = Modifier.height(16.dp))
            Text(
                text = "Audio FX & Equalizer",
                style = MaterialTheme.typography.headlineSmall,
                fontWeight = FontWeight.Bold
            )
            Spacer(modifier = Modifier.height(24.dp))
            
            // Speed & Pitch
            Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween) {
                Text("Playback Speed: ${String.format("%.2fx", speed)}", style = MaterialTheme.typography.labelLarge)
            }
            Slider(
                value = speed,
                onValueChange = { 
                    speed = it
                    controller?.playbackParameters = PlaybackParameters(speed, pitch)
                },
                valueRange = 0.5f..2.0f,
                steps = 15
            )
            
            Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween) {
                Text("Pitch: ${String.format("%.2fx", pitch)}", style = MaterialTheme.typography.labelLarge)
            }
            Slider(
                value = pitch,
                onValueChange = { 
                    pitch = it
                    controller?.playbackParameters = PlaybackParameters(speed, pitch)
                },
                valueRange = 0.5f..2.0f,
                steps = 15
            )
            
            Spacer(modifier = Modifier.height(16.dp))
            HorizontalDivider()
            Spacer(modifier = Modifier.height(16.dp))
            
            Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween, verticalAlignment = Alignment.CenterVertically) {
                Text("Equalizer", style = MaterialTheme.typography.titleMedium, fontWeight = FontWeight.Bold)
                Row(verticalAlignment = Alignment.CenterVertically) {
                    TextButton(onClick = { 
                        view.performHapticFeedback(HapticFeedbackConstants.VIRTUAL_KEY)
                        AudioEffectManager.reset() 
                    }) {
                        Text("RESET")
                    }
                    Switch(
                        checked = eqState.enabled, 
                        onCheckedChange = { 
                            view.performHapticFeedback(HapticFeedbackConstants.VIRTUAL_KEY)
                            AudioEffectManager.setEnabled(it) 
                        }
                    )
                }
            }
            
            if (eqState.presets.isNotEmpty()) {
                // Presets Dropdown or simple horizontal scroll
                Text("Presets", style = MaterialTheme.typography.labelMedium, modifier = Modifier.fillMaxWidth())
                Spacer(modifier = Modifier.height(8.dp))
                androidx.compose.foundation.lazy.LazyRow(
                    horizontalArrangement = Arrangement.spacedBy(8.dp),
                    modifier = Modifier.fillMaxWidth()
                ) {
                    items(eqState.presets.size) { i ->
                        val isSelected = eqState.currentPreset.toInt() == i
                        Box(
                            modifier = Modifier
                                .clip(RoundedCornerShape(16.dp))
                                .background(if (isSelected) MaterialTheme.colorScheme.primary else MaterialTheme.colorScheme.surfaceVariant)
                                .clickable { 
                                    view.performHapticFeedback(HapticFeedbackConstants.VIRTUAL_KEY)
                                    AudioEffectManager.usePreset(i.toShort()) 
                                }
                                .padding(horizontal = 16.dp, vertical = 8.dp)
                        ) {
                            Text(
                                text = eqState.presets[i],
                                color = if (isSelected) MaterialTheme.colorScheme.onPrimary else MaterialTheme.colorScheme.onSurfaceVariant,
                                style = MaterialTheme.typography.labelMedium
                            )
                        }
                    }
                }
                Spacer(modifier = Modifier.height(24.dp))
            }
            
            if (eqState.bands.isNotEmpty()) {
                // Bands
                Row(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.SpaceEvenly
                ) {
                    eqState.bands.forEach { band ->
                        Column(
                            horizontalAlignment = Alignment.CenterHorizontally,
                            modifier = Modifier.weight(1f)
                        ) {
                            // Vertical slider for EQ
                            Box(modifier = Modifier.height(150.dp).padding(vertical = 8.dp)) {
                                // Draw vertical slider workaround
                                Slider(
                                    value = band.level.toFloat(),
                                    onValueChange = { 
                                        AudioEffectManager.setBandLevel(band.index, it.toInt().toShort()) 
                                    },
                                    valueRange = band.minLevel.toFloat()..band.maxLevel.toFloat(),
                                    modifier = Modifier
                                        .align(Alignment.Center)
                                        .width(150.dp) // The height when rotated
                                        .rotate(-90f) // Vertical
                                )
                            }
                            Text(
                                text = if (band.centerFreqHz >= 1000) "${band.centerFreqHz/1000}k" else "${band.centerFreqHz}",
                                style = MaterialTheme.typography.labelSmall
                            )
                        }
                    }
                }
            } else if (eqState.enabled) {
                 Text(
                    text = "System Equalizer Note: Full band equalizer is applying.",
                    style = MaterialTheme.typography.bodySmall,
                    color = MaterialTheme.colorScheme.onSurfaceVariant
                )
            }
            
            Spacer(modifier = Modifier.height(48.dp))
        }
    }
}