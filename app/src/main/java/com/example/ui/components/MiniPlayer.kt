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
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import androidx.media3.common.Player
import androidx.media3.session.MediaController
import coil.compose.AsyncImage
import kotlinx.coroutines.delay

import com.example.viewmodel.MainViewModel
import com.example.data.local.UserStats
import com.example.ui.theme.neonGlow
import com.example.utils.rememberBatteryLevel

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
    val view = LocalView.current
    var isPlaying by remember { mutableStateOf(controller?.isPlaying == true) }
    var currentTitle by remember { mutableStateOf("") }
    var currentArtist by remember { mutableStateOf("") }
    var currentPosition by remember { mutableStateOf(0L) }
    var duration by remember { mutableStateOf(0L) }
    var artworkUri by remember { mutableStateOf<android.net.Uri?>(null) }
    var showMiniPlayer by remember { mutableStateOf(controller?.currentMediaItem != null) }

    val batteryLevel = rememberBatteryLevel()
    val isBatterySaverOn = userStats.batterySaver && batteryLevel <= 20f

    LaunchedEffect(controller, isBatterySaverOn) {
        val listener = object : Player.Listener {
            override fun onIsPlayingChanged(playing: Boolean) {
                isPlaying = playing
            }
            override fun onMediaItemTransition(mediaItem: androidx.media3.common.MediaItem?, reason: Int) {
                currentTitle = mediaItem?.mediaMetadata?.title?.toString() ?: "Unknown"
                currentArtist = mediaItem?.mediaMetadata?.artist?.toString() ?: "Unknown"
                artworkUri = mediaItem?.mediaMetadata?.artworkUri
                duration = controller?.duration?.coerceAtLeast(0L) ?: 0L
                if (mediaItem != null) showMiniPlayer = true
            }
            override fun onPlaybackStateChanged(playbackState: Int) {
                duration = controller?.duration?.coerceAtLeast(0L) ?: 0L
                if (playbackState == Player.STATE_READY) showMiniPlayer = true
            }
        }
        controller?.addListener(listener)
        currentTitle = controller?.currentMediaItem?.mediaMetadata?.title?.toString() ?: "Unknown"
        currentArtist = controller?.currentMediaItem?.mediaMetadata?.artist?.toString() ?: "Unknown"
        artworkUri = controller?.currentMediaItem?.mediaMetadata?.artworkUri
        duration = controller?.duration?.coerceAtLeast(0L) ?: 0L
        if (controller?.currentMediaItem != null) showMiniPlayer = true

        while (true) {
            if (controller?.isPlaying == true) {
                currentPosition = controller.currentPosition.coerceAtLeast(0L)
            }
            delay(if (isBatterySaverOn) 1000L else 100L)
        }
    }

    val progress = if (duration > 0) currentPosition.toFloat() / duration.toFloat() else 0f

    AnimatedVisibility(
        visible = showMiniPlayer,
        enter = slideInVertically(initialOffsetY = { it }),
        exit = slideOutVertically(targetOffsetY = { it })
    ) {
        val animatedVisibilityScope = this
        val baseModifier = Modifier
            .fillMaxWidth()
            .padding(horizontal = 12.dp, vertical = 8.dp)
            .height(64.dp)
            
        val enhancedModifier = if (!isBatterySaverOn && userStats.neonBorders) {
            baseModifier.neonGlow(color = dominantColor ?: Color.White, enabled = true)
        } else {
            baseModifier
        }
            
        Card(
            modifier = enhancedModifier.clickable { 
                view.performHapticFeedback(HapticFeedbackConstants.CLOCK_TICK)
                onExpand() 
            },
            shape = RoundedCornerShape(32.dp),
            colors = CardDefaults.cardColors(containerColor = dominantColor ?: Color(0xFF1E1E1E))
        ) {
            Column {
                Row(
                    modifier = Modifier
                        .fillMaxWidth()
                        .weight(1f)
                        .padding(horizontal = 12.dp),
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    with(sharedTransitionScope) {
                        Box(
                            modifier = Modifier
                                .size(40.dp)
                                .sharedElement(
                                    state = rememberSharedContentState(key = "album_art"),
                                    animatedVisibilityScope = animatedVisibilityScope
                                )
                                .clip(androidx.compose.foundation.shape.CircleShape)
                                .background(Color.White.copy(alpha = 0.2f)),
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
                                Icon(Icons.Rounded.MusicNote, contentDescription = null, tint = Color.White)
                            }
                        }
                    }
                    Spacer(modifier = Modifier.width(12.dp))
                    Column(modifier = Modifier.weight(1f)) {
                        Text(
                            text = currentTitle,
                            style = MaterialTheme.typography.bodyMedium.copy(fontWeight = FontWeight.Bold),
                            color = Color.White,
                            maxLines = 1,
                            modifier = if (isBatterySaverOn) Modifier else Modifier.basicMarquee()
                        )
                        Text(
                            text = currentArtist,
                            style = MaterialTheme.typography.bodySmall,
                            color = Color.White.copy(alpha = 0.7f),
                            maxLines = 1,
                            modifier = if (isBatterySaverOn) Modifier else Modifier.basicMarquee()
                        )
                    }
                    val currentUri = controller?.currentMediaItem?.localConfiguration?.uri?.toString() ?: ""
                    val isLiked by viewModel.isLiked(currentUri).collectAsStateWithLifecycle(initialValue = false)
                    
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
                    Box(contentAlignment = Alignment.Center) {
                        CircularProgressIndicator(
                            progress = { progress },
                            modifier = Modifier.size(44.dp),
                            color = Color.White.copy(alpha = 0.5f),
                            trackColor = Color.White.copy(alpha = 0.1f),
                            strokeWidth = 2.dp,
                            strokeCap = androidx.compose.ui.graphics.StrokeCap.Round
                        )
                        IconButton(onClick = {
                            view.performHapticFeedback(HapticFeedbackConstants.CLOCK_TICK)
                            if (isPlaying) controller?.pause() else controller?.play()
                        }) {
                            if (isBatterySaverOn) {
                                Icon(
                                    imageVector = if (isPlaying) Icons.Rounded.Pause else Icons.Rounded.PlayArrow,
                                    contentDescription = "Play/Pause",
                                    tint = Color.White,
                                    modifier = Modifier.size(28.dp)
                                )
                            } else {
                                androidx.compose.animation.AnimatedContent(
                                    targetState = isPlaying,
                                    label = "play_pause_anim_mini"
                                ) { playing ->
                                    Icon(
                                        imageVector = if (playing) Icons.Rounded.Pause else Icons.Rounded.PlayArrow,
                                        contentDescription = "Play/Pause",
                                        tint = Color.White,
                                        modifier = Modifier.size(28.dp)
                                    )
                                }
                            }
                        }
                    }
                    IconButton(onClick = {
                        view.performHapticFeedback(HapticFeedbackConstants.CLOCK_TICK)
                        if ((controller?.mediaItemCount ?: 0) <= 1) {
                            val isShuffle = controller?.shuffleModeEnabled == true
                            val repeatMode = controller?.repeatMode ?: Player.REPEAT_MODE_OFF
                            viewModel.playNextRemote(isShuffle, repeatMode)
                        } else {
                            controller?.seekToNext()
                        }
                    }) {
                        Icon(Icons.Rounded.SkipNext, contentDescription = "Next", tint = Color.White)
                    }
                }

            }
        }
    }
}
