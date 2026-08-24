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

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun AudioSettingsBottomSheet(
    controller: MediaController?,
    onDismissRequest: () -> Unit
) {
    var speed by remember { mutableStateOf(controller?.playbackParameters?.speed ?: 1f) }
    var pitch by remember { mutableStateOf(controller?.playbackParameters?.pitch ?: 1f) }

    ModalBottomSheet(onDismissRequest = onDismissRequest) {
        Column(
            modifier = Modifier
                .fillMaxWidth()
                .padding(24.dp),
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
                text = "Audio FX & Playback",
                style = MaterialTheme.typography.headlineSmall,
                fontWeight = FontWeight.Bold
            )
            Spacer(modifier = Modifier.height(32.dp))

            // Playback Speed
            Text(
                text = "Playback Speed: ${String.format("%.2fx", speed)}",
                style = MaterialTheme.typography.bodyLarge
            )
            Slider(
                value = speed,
                onValueChange = { 
                    speed = it
                    controller?.playbackParameters = PlaybackParameters(speed, pitch)
                },
                valueRange = 0.5f..2.0f,
                steps = 15,
                modifier = Modifier.fillMaxWidth()
            )

            Spacer(modifier = Modifier.height(16.dp))

            // Pitch
            Text(
                text = "Pitch: ${String.format("%.2fx", pitch)}",
                style = MaterialTheme.typography.bodyLarge
            )
            Slider(
                value = pitch,
                onValueChange = { 
                    pitch = it
                    controller?.playbackParameters = PlaybackParameters(speed, pitch)
                },
                valueRange = 0.5f..2.0f,
                steps = 15,
                modifier = Modifier.fillMaxWidth()
            )

            Spacer(modifier = Modifier.height(16.dp))
            
            Text(
                text = "System Equalizer Note: Full band equalizer requires OS-level audio routing permissions which are currently managed by your device's built-in Equalizer settings.",
                style = MaterialTheme.typography.bodySmall,
                color = MaterialTheme.colorScheme.onSurfaceVariant
            )

            Spacer(modifier = Modifier.height(48.dp))
        }
    }
}
