package com.example.ui.components

import androidx.compose.animation.AnimatedVisibility
import androidx.compose.animation.slideInVertically
import androidx.compose.animation.slideOutVertically
import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.rounded.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.media3.common.Player
import androidx.media3.session.MediaController
import kotlinx.coroutines.delay

@Composable
fun MiniPlayer(
    controller: MediaController?,
    dominantColor: Color?,
    onShowLyrics: () -> Unit
) {
    if (controller == null) return

    var isPlaying by remember { mutableStateOf(false) }
    var currentTitle by remember { mutableStateOf("") }
    var currentArtist by remember { mutableStateOf("") }
    var hasMedia by remember { mutableStateOf(false) }

    LaunchedEffect(controller) {
        val listener = object : Player.Listener {
            override fun onIsPlayingChanged(playing: Boolean) {
                isPlaying = playing
            }
            override fun onMediaItemTransition(mediaItem: androidx.media3.common.MediaItem?, reason: Int) {
                hasMedia = mediaItem != null
                currentTitle = mediaItem?.mediaMetadata?.title?.toString() ?: mediaItem?.localConfiguration?.uri?.lastPathSegment ?: "Unknown"
                currentArtist = mediaItem?.mediaMetadata?.artist?.toString() ?: "Unknown"
            }
        }
        controller.addListener(listener)
        // Initial state
        hasMedia = controller.currentMediaItem != null
        isPlaying = controller.isPlaying
        currentTitle = controller.currentMediaItem?.mediaMetadata?.title?.toString() ?: controller.currentMediaItem?.localConfiguration?.uri?.lastPathSegment ?: "Unknown"
        currentArtist = controller.currentMediaItem?.mediaMetadata?.artist?.toString() ?: "Unknown"
    }

    AnimatedVisibility(
        visible = hasMedia,
        enter = slideInVertically(initialOffsetY = { it }),
        exit = slideOutVertically(targetOffsetY = { it })
    ) {
        Card(
            modifier = Modifier
                .fillMaxWidth()
                .padding(8.dp)
                .clickable { onShowLyrics() },
            shape = RoundedCornerShape(16.dp),
            colors = CardDefaults.cardColors(containerColor = dominantColor ?: MaterialTheme.colorScheme.surfaceVariant)
        ) {
            Row(
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(horizontal = 16.dp, vertical = 8.dp),
                verticalAlignment = Alignment.CenterVertically
            ) {
                Icon(
                    imageVector = Icons.Rounded.MusicNote,
                    contentDescription = null,
                    modifier = Modifier
                        .size(40.dp)
                        .background(Color.Black.copy(alpha = 0.2f), RoundedCornerShape(8.dp))
                        .padding(8.dp),
                    tint = MaterialTheme.colorScheme.onSurface
                )
                Spacer(modifier = Modifier.width(12.dp))
                Column(modifier = Modifier.weight(1f)) {
                    Text(text = currentTitle, style = MaterialTheme.typography.bodyLarge, fontWeight = FontWeight.Bold, maxLines = 1)
                    Text(text = currentArtist, style = MaterialTheme.typography.bodyMedium, color = MaterialTheme.colorScheme.onSurface.copy(alpha = 0.7f), maxLines = 1)
                }
                IconButton(onClick = {
                    if (isPlaying) controller.pause() else controller.play()
                }) {
                    Icon(
                        imageVector = if (isPlaying) Icons.Rounded.Pause else Icons.Rounded.PlayArrow,
                        contentDescription = "Play/Pause"
                    )
                }
            }
        }
    }
}
