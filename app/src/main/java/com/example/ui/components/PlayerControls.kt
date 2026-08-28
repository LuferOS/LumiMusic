package com.example.ui.components

import android.view.HapticFeedbackConstants
import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.rounded.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.platform.LocalView
import androidx.compose.ui.unit.dp
import androidx.media3.common.Player
import androidx.media3.session.MediaController
import com.example.viewmodel.MainViewModel

@Composable
fun PlayerControls(
    controller: MediaController?,
    isPlaying: Boolean,
    viewModel: MainViewModel,
    isBatterySaverOn: Boolean
) {
    val view = LocalView.current
    var isShuffle by remember { mutableStateOf(controller?.shuffleModeEnabled == true) }
    var repeatMode by remember { mutableStateOf(controller?.repeatMode ?: Player.REPEAT_MODE_OFF) }

    Row(
        modifier = Modifier.fillMaxWidth(),
        horizontalArrangement = Arrangement.SpaceBetween,
        verticalAlignment = Alignment.CenterVertically
    ) {
        IconButton(onClick = { 
            view.performHapticFeedback(HapticFeedbackConstants.CLOCK_TICK)
            controller?.shuffleModeEnabled = !isShuffle
            isShuffle = !isShuffle
        }) {
            Icon(Icons.Rounded.Shuffle, contentDescription = "Shuffle", tint = if (isShuffle) Color(0xFF1DB954) else Color.White.copy(alpha = 0.7f))
        }
        
        IconButton(onClick = { 
            view.performHapticFeedback(HapticFeedbackConstants.CLOCK_TICK)
            if (controller?.hasPreviousMediaItem() == false) {
                val isShuffleMode = controller?.shuffleModeEnabled == true
                val mode = controller?.repeatMode ?: Player.REPEAT_MODE_OFF
                viewModel.playPreviousRemote(isShuffleMode, mode)
            } else {
                controller?.seekToPrevious() 
            }
        }) {
            Icon(Icons.Rounded.SkipPrevious, contentDescription = "Previous", modifier = Modifier.size(40.dp), tint = Color.White)
        }
        
        Box(
            modifier = Modifier
                .size(72.dp)
                .clip(CircleShape)
                .background(Color.White)
                .clickable { 
                    view.performHapticFeedback(HapticFeedbackConstants.CLOCK_TICK)
                    if (isPlaying) controller?.pause() else controller?.play() 
                },
            contentAlignment = Alignment.Center
        ) {
            if (isBatterySaverOn) {
                Icon(
                    imageVector = if (isPlaying) Icons.Rounded.Pause else Icons.Rounded.PlayArrow,
                    contentDescription = "Play/Pause",
                    modifier = Modifier.size(40.dp),
                    tint = Color.Black
                )
            } else {
                androidx.compose.animation.AnimatedContent(
                    targetState = isPlaying,
                    label = "play_pause_anim"
                ) { playing ->
                    Icon(
                        imageVector = if (playing) Icons.Rounded.Pause else Icons.Rounded.PlayArrow,
                        contentDescription = "Play/Pause",
                        modifier = Modifier.size(40.dp),
                        tint = Color.Black
                    )
                }
            }
        }
        
        IconButton(onClick = { 
            view.performHapticFeedback(HapticFeedbackConstants.CLOCK_TICK)
            if (controller?.hasNextMediaItem() == false) {
                val isShuffleMode = controller?.shuffleModeEnabled == true
                val mode = controller?.repeatMode ?: Player.REPEAT_MODE_OFF
                viewModel.playNextRemote(isShuffleMode, mode)
            } else {
                controller?.seekToNext() 
            }
        }) {
            Icon(Icons.Rounded.SkipNext, contentDescription = "Next", modifier = Modifier.size(40.dp), tint = Color.White)
        }
        
        IconButton(onClick = { 
            view.performHapticFeedback(HapticFeedbackConstants.CLOCK_TICK)
            val nextMode = when(repeatMode) {
                Player.REPEAT_MODE_OFF -> Player.REPEAT_MODE_ALL
                Player.REPEAT_MODE_ALL -> Player.REPEAT_MODE_ONE
                else -> Player.REPEAT_MODE_OFF
            }
            controller?.repeatMode = nextMode
            repeatMode = nextMode
        }) {
            Icon(
                imageVector = if (repeatMode == Player.REPEAT_MODE_ONE) Icons.Rounded.RepeatOne else Icons.Rounded.Repeat, 
                contentDescription = "Repeat", 
                tint = if (repeatMode != Player.REPEAT_MODE_OFF) Color(0xFF1DB954) else Color.White.copy(alpha = 0.7f)
            )
        }
    }
}
