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
import androidx.compose.runtime.collectAsState
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.foundation.basicMarquee
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import androidx.compose.ui.platform.LocalView
import android.view.HapticFeedbackConstants
import androidx.media3.common.Player
import androidx.media3.session.MediaController
import coil.compose.AsyncImage
import kotlinx.coroutines.delay

import com.example.viewmodel.MainViewModel
import com.example.data.local.UserStats
import com.example.ui.theme.neonGlow

@OptIn(androidx.compose.animation.ExperimentalSharedTransitionApi::class)
@Composable
fun MiniPlayer(
    controller: MediaController?,
    dominantColor: Color?,
    viewModel: MainViewModel,
    userStats: UserStats,
    sharedTransitionScope: androidx.compose.animation.SharedTransitionScope,
    onExpand: () -> Unit
) {
    if (controller == null) return
    val view = LocalView.current
    var isPlaying by remember { mutableStateOf(false) }
    var currentTitle by remember { mutableStateOf("") }
    var currentArtist by remember { mutableStateOf("") }
    var hasMedia by remember { mutableStateOf(false) }
    var currentPosition by remember { mutableStateOf(0L) }
    var duration by remember { mutableStateOf(0L) }
    var artworkUri by remember { mutableStateOf<android.net.Uri?>(null) }

    LaunchedEffect(controller) {
        val listener = object : Player.Listener {
            override fun onIsPlayingChanged(playing: Boolean) {
                isPlaying = playing
            }
            override fun onMediaItemTransition(mediaItem: androidx.media3.common.MediaItem?, reason: Int) {
                hasMedia = mediaItem != null
                currentTitle = mediaItem?.mediaMetadata?.title?.toString() ?: mediaItem?.localConfiguration?.uri?.lastPathSegment ?: "Unknown"
                currentArtist = mediaItem?.mediaMetadata?.artist?.toString() ?: "Unknown"
                artworkUri = mediaItem?.mediaMetadata?.artworkUri
                duration = controller.duration.coerceAtLeast(0L)
            }
            override fun onPlaybackStateChanged(playbackState: Int) {
                duration = controller.duration.coerceAtLeast(0L)
            }
        }
        controller.addListener(listener)
        // Initial state
        hasMedia = controller.currentMediaItem != null
        isPlaying = controller.isPlaying
        currentTitle = controller.currentMediaItem?.mediaMetadata?.title?.toString() ?: controller.currentMediaItem?.localConfiguration?.uri?.lastPathSegment ?: "Unknown"
        currentArtist = controller.currentMediaItem?.mediaMetadata?.artist?.toString() ?: "Unknown"
        artworkUri = controller.currentMediaItem?.mediaMetadata?.artworkUri
        duration = controller.duration.coerceAtLeast(0L)
        
        while (true) {
            if (controller.isPlaying) {
                currentPosition = controller.currentPosition.coerceAtLeast(0L)
            }
            delay(1000)
        }
    }

    AnimatedVisibility(
        visible = hasMedia,
        enter = slideInVertically(initialOffsetY = { it }),
        exit = slideOutVertically(targetOffsetY = { it })
    ) {
        val progress = if (duration > 0) currentPosition.toFloat() / duration.toFloat() else 0f
        
        Card(
            modifier = Modifier
                .fillMaxWidth()
                .padding(horizontal = 8.dp, vertical = 4.dp)
                .neonGlow(color = dominantColor ?: Color.White, enabled = userStats.neonBorders)
                .clickable { view.performHapticFeedback(HapticFeedbackConstants.CLOCK_TICK); onExpand() },
            shape = RoundedCornerShape(8.dp),
            colors = CardDefaults.cardColors(containerColor = dominantColor ?: Color(0xFF333333))
        ) {
            Column {
                Row(
                    modifier = Modifier
                        .fillMaxWidth()
                        .padding(8.dp),
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    with(sharedTransitionScope) {
                        Box(
                            modifier = Modifier
                                .size(40.dp)
                                .sharedElement(
                                    state = rememberSharedContentState(key = "album_art"),
                                    animatedVisibilityScope = this@AnimatedVisibility
                                )
                                .clip(RoundedCornerShape(4.dp))
                                .background(Color.White.copy(alpha = 0.1f)),
                            contentAlignment = Alignment.Center
                        ) {
                        if (artworkUri != null) {
                            AsyncImage(
                                model = artworkUri,
                                contentDescription = "Album Art",
                                contentScale = ContentScale.Crop,
                                modifier = Modifier.fillMaxSize()
                            )
                        } else {
                            Icon(
                                imageVector = Icons.Rounded.MusicNote,
                                contentDescription = null,
                                tint = Color.White.copy(alpha = 0.5f)
                            )
                        }
                        }
                    }
                    
                    Spacer(modifier = Modifier.width(12.dp))
                    
                    Column(modifier = Modifier.weight(1f)) {
                        Text(
                            text = currentTitle, 
                            style = MaterialTheme.typography.bodyMedium, 
                            fontWeight = FontWeight.Bold, 
                            color = Color.White,
                            maxLines = 1,
                            modifier = Modifier.basicMarquee()
                        )
                        Text(
                            text = currentArtist, 
                            style = MaterialTheme.typography.bodySmall, 
                            color = Color.White.copy(alpha = 0.7f), 
                            maxLines = 1,
                            modifier = Modifier.basicMarquee()
                        )
                    }
                    
                    val currentUri = controller?.currentMediaItem?.localConfiguration?.uri?.toString() ?: ""
                    val isLiked by viewModel.isLiked(currentUri).collectAsState(initial = false)
                    
                    IconButton(onClick = {
                        view.performHapticFeedback(HapticFeedbackConstants.CLOCK_TICK)
                        viewModel.toggleLike(currentUri, currentTitle, currentArtist, artworkUri?.toString())
                    }) {
                        Icon(
                            imageVector = if (isLiked) Icons.Rounded.Favorite else Icons.Rounded.FavoriteBorder,
                            contentDescription = "Like",
                            tint = if (isLiked) Color(0xFF1DB954) else Color.White
                        )
                    }
                    IconButton(onClick = {
                        view.performHapticFeedback(HapticFeedbackConstants.CLOCK_TICK)
                        if (isPlaying) controller.pause() else controller.play()
                    }) {
                        androidx.compose.animation.AnimatedContent(
                            targetState = isPlaying,
                            label = "play_pause_anim_mini"
                        ) { playing ->
                            Icon(
                                imageVector = if (playing) Icons.Rounded.Pause else Icons.Rounded.PlayArrow,
                                contentDescription = "Play/Pause",
                                tint = Color.White
                            )
                        }
                    }
                    IconButton(onClick = {
                        view.performHapticFeedback(HapticFeedbackConstants.CLOCK_TICK)
                        if ((controller.mediaItemCount ?: 0) <= 1) {
                            val isShuffle = controller.shuffleModeEnabled == true
                            val repeatMode = controller.repeatMode ?: Player.REPEAT_MODE_OFF
                            viewModel.playNextRemote(isShuffle, repeatMode)
                        } else {
                            controller.seekToNext()
                        }
                    }) {
                        Icon(
                            imageVector = Icons.Rounded.SkipNext,
                            contentDescription = "Next",
                            tint = Color.White
                        )
                    }
                }
                
                // Bottom progress bar
                Box(
                    modifier = Modifier
                        .fillMaxWidth()
                        .height(2.dp)
                        .padding(horizontal = 8.dp)
                        .background(Color.White.copy(alpha = 0.2f), RoundedCornerShape(1.dp))
                ) {
                    Box(
                        modifier = Modifier
                            .fillMaxWidth(fraction = progress)
                            .height(2.dp)
                            .background(Color.White, RoundedCornerShape(1.dp))
                    )
                }
                Spacer(modifier = Modifier.height(2.dp))
            }
        }
    }
}