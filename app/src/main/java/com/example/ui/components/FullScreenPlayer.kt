package com.example.ui.components

import androidx.compose.animation.animateContentSize
import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.gestures.detectDragGestures
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
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.graphicsLayer
import androidx.compose.ui.input.pointer.pointerInput
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import androidx.compose.ui.platform.LocalView
import android.view.HapticFeedbackConstants
import androidx.media3.common.Player
import androidx.media3.session.MediaController
import kotlinx.coroutines.delay

import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.itemsIndexed
import androidx.compose.foundation.lazy.rememberLazyListState
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import com.example.viewmodel.MainViewModel
import com.example.utils.rememberBatteryLevel

@OptIn(ExperimentalMaterial3Api::class, androidx.compose.animation.ExperimentalSharedTransitionApi::class)
@Composable
fun FullScreenPlayer(
    controller: MediaController?,
    dominantColor: Color?,
    viewModel: MainViewModel,
    userStats: com.example.data.local.UserStats,
    sharedTransitionScope: androidx.compose.animation.SharedTransitionScope,
    animatedVisibilityScope: androidx.compose.animation.AnimatedVisibilityScope,
    onClose: () -> Unit
) {
    val view = LocalView.current
    var isPlaying by remember { mutableStateOf(controller?.isPlaying == true) }
    var currentTitle by remember { mutableStateOf("") }
    var currentArtist by remember { mutableStateOf("") }
    var currentPosition by remember { mutableStateOf(0L) }
    var duration by remember { mutableStateOf(0L) }
    var artworkUri by remember { mutableStateOf<android.net.Uri?>(null) }
    var isLyricsExpanded by remember { mutableStateOf(false) }
    val lrcState by viewModel.lrcState.collectAsStateWithLifecycle()
    val lyricsState by viewModel.lyricsState.collectAsStateWithLifecycle()

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
            }
            override fun onPlaybackStateChanged(playbackState: Int) {
                duration = controller?.duration?.coerceAtLeast(0L) ?: 0L
            }
        }
        controller?.addListener(listener)
        currentTitle = controller?.currentMediaItem?.mediaMetadata?.title?.toString() ?: "Unknown"
        currentArtist = controller?.currentMediaItem?.mediaMetadata?.artist?.toString() ?: "Unknown"
        artworkUri = controller?.currentMediaItem?.mediaMetadata?.artworkUri
        duration = controller?.duration?.coerceAtLeast(0L) ?: 0L
        
        while (true) {
            if (controller?.isPlaying == true) {
                currentPosition = controller.currentPosition.coerceAtLeast(0L)
            }
            // Battery Saver: Update UI every 1s instead of 100ms when battery is low
            delay(if (isBatterySaverOn) 1000L else 100L)
        }
    }

    val progress = if (duration > 0) currentPosition.toFloat() / duration.toFloat() else 0f
    
    // Minimalist Design: Flat gradient, more dark/subtle
    val topColor = dominantColor ?: Color.DarkGray
    val bottomColor = Color(0xFF121212)

    Box(
        modifier = Modifier
            .fillMaxSize()
            .background(Brush.verticalGradient(listOf(topColor.copy(alpha = 0.5f), bottomColor)))
            .pointerInput(Unit) {
                detectDragGestures { _, dragAmount ->
                    if (dragAmount.y > 50) {
                        onClose()
                    }
                }
            }
    ) {
        Column(
            modifier = Modifier
                .fillMaxSize()
                .animateContentSize()
                .padding(horizontal = 24.dp)
                .statusBarsPadding()
                .navigationBarsPadding(),
        ) {
            // Top Bar
            Row(
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(top = 16.dp, bottom = 16.dp),
                horizontalArrangement = Arrangement.SpaceBetween,
                verticalAlignment = Alignment.CenterVertically
            ) {
                IconButton(onClick = {
                    view.performHapticFeedback(HapticFeedbackConstants.CLOCK_TICK)
                    onClose()
                }) {
                    Icon(Icons.Rounded.KeyboardArrowDown, contentDescription = "Close", tint = Color.White)
                }
                Text(
                    text = "Now Playing",
                    style = MaterialTheme.typography.labelMedium,
                    color = Color.White.copy(alpha = 0.7f),
                    fontWeight = FontWeight.Bold
                )
                Spacer(modifier = Modifier.size(48.dp))
            }

            Spacer(modifier = Modifier.weight(0.2f))

            PlayerArtwork(
                artworkUri = artworkUri,
                dominantColor = dominantColor,
                neonBorders = userStats.neonBorders,
                isBatterySaverOn = isBatterySaverOn,
                sharedTransitionScope = sharedTransitionScope,
                animatedVisibilityScope = animatedVisibilityScope
            )

            Spacer(modifier = Modifier.weight(0.15f))
            
            // Battery Saver: Disable Visualizer
            if (userStats.showSpectrums && !isBatterySaverOn) {
                VisualizerView(
                    isPlaying = isPlaying,
                    visualizerType = userStats.visualizerType,
                    primaryColor = if (userStats.visualizerColor == "Dinámico") (dominantColor ?: Color.White) else {
                        try { Color(android.graphics.Color.parseColor(userStats.visualizerColor)) } catch(e: Exception) { Color.White }
                    },
                    modifier = Modifier.padding(horizontal = 32.dp)
                )
            } else {
                Spacer(modifier = Modifier.height(100.dp))
            }

            Spacer(modifier = Modifier.weight(0.15f))

            // Title & Artist Row
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.SpaceBetween,
                verticalAlignment = Alignment.CenterVertically
            ) {
                Column(modifier = Modifier.weight(1f)) {
                    Text(
                        text = currentTitle,
                        style = MaterialTheme.typography.headlineMedium.copy(fontWeight = FontWeight.Bold),
                        color = Color.White,
                        maxLines = 1,
                        modifier = if (isBatterySaverOn) Modifier else Modifier.basicMarquee()
                    )
                    Spacer(modifier = Modifier.height(4.dp))
                    Text(
                        text = currentArtist,
                        style = MaterialTheme.typography.titleMedium,
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
                        tint = if (isLiked) Color(0xFF1DB954) else Color.White, 
                        modifier = Modifier.size(32.dp)
                    )
                }
            }

            Spacer(modifier = Modifier.height(16.dp))

            // Seekbar
            Slider(
                value = progress,
                onValueChange = { 
                    val newPosition = (it * duration).toLong()
                    if (Math.abs(currentPosition - newPosition) > 1000) {
                        view.performHapticFeedback(HapticFeedbackConstants.CLOCK_TICK)
                    }
                    controller?.seekTo(newPosition)
                    currentPosition = newPosition
                },
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(horizontal = 8.dp)
                    .height(24.dp),
                colors = SliderDefaults.colors(
                    thumbColor = Color.White,
                    activeTrackColor = Color.White,
                    inactiveTrackColor = Color.White.copy(alpha = 0.3f)
                )
            )
            Row(
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(horizontal = 8.dp),
                horizontalArrangement = Arrangement.SpaceBetween
            ) {
                Text(formatTime(currentPosition), style = MaterialTheme.typography.labelMedium, color = Color.White.copy(alpha = 0.5f), fontWeight = FontWeight.SemiBold)
                Text(formatTime(duration), style = MaterialTheme.typography.labelMedium, color = Color.White.copy(alpha = 0.5f), fontWeight = FontWeight.SemiBold)
            }

            Spacer(modifier = Modifier.height(16.dp))

            PlayerControls(
                controller = controller,
                isPlaying = isPlaying,
                viewModel = viewModel,
                isBatterySaverOn = isBatterySaverOn
            )

            Spacer(modifier = Modifier.height(16.dp))

            // Lyrics Peek Box
            Box(
                modifier = Modifier
                    .fillMaxWidth()
                    .heightIn(min = 90.dp)
                    .clip(RoundedCornerShape(16.dp))
                    .background(if (isLyricsExpanded) Color.Black.copy(alpha = 0.4f) else Color.White.copy(alpha = 0.08f))
                    .clickable { isLyricsExpanded = !isLyricsExpanded }
                    .padding(16.dp)
                    .weight(if (isLyricsExpanded) 1f else 0.001f, fill = false)
            ) {
                Column(modifier = Modifier.fillMaxSize()) {
                    Row(
                        modifier = Modifier.fillMaxWidth(),
                        horizontalArrangement = Arrangement.SpaceBetween,
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        Text(
                            "Lyrics", 
                            style = MaterialTheme.typography.titleMedium.copy(fontWeight = FontWeight.Bold), 
                            color = Color.White
                        )
                        Icon(
                            imageVector = if (isLyricsExpanded) Icons.Rounded.CloseFullscreen else Icons.Rounded.OpenInFull, 
                            contentDescription = "Expand", 
                            tint = Color.White, 
                            modifier = Modifier.size(18.dp)
                        )
                    }
                    Spacer(modifier = Modifier.height(16.dp))
                    
                    if (lrcState != null) {
                        val activeLineIndex by remember(lrcState) {
                            derivedStateOf {
                                val lines = lrcState ?: emptyList()
                                val idx = lines.indexOfLast { it.timeMs <= currentPosition }
                                if (idx == -1) 0 else idx
                            }
                        }
                        
                        val listState = rememberLazyListState()
                        LaunchedEffect(activeLineIndex) {
                            if (isLyricsExpanded && !lrcState.isNullOrEmpty() && !isBatterySaverOn) {
                                val targetIdx = maxOf(0, activeLineIndex - 2)
                                listState.animateScrollToItem(targetIdx)
                            }
                        }
                        
                        LazyColumn(
                            state = listState,
                            modifier = Modifier.fillMaxSize(),
                            contentPadding = PaddingValues(bottom = if (isLyricsExpanded) 64.dp else 0.dp)
                        ) {
                            itemsIndexed(lrcState ?: emptyList()) { index, line ->
                                val isActive = index == activeLineIndex
                                val alpha = if (isActive) 1f else 0.4f
                                val scale = if (isActive) (if (isBatterySaverOn) 1f else 1.05f) else 1f
                                Text(
                                    text = line.text,
                                    style = MaterialTheme.typography.headlineSmall.copy(fontWeight = if (isActive) FontWeight.Bold else FontWeight.Medium),
                                    color = Color.White.copy(alpha = alpha),
                                    modifier = Modifier
                                        .padding(vertical = 8.dp)
                                        .graphicsLayer {
                                            scaleX = scale
                                            scaleY = scale
                                        }
                                )
                            }
                        }
                    } else {
                        val lyricsText = lyricsState ?: "Loading..."
                        val peekLyrics = if (!isLyricsExpanded && lyricsText.isNotBlank() && lyricsText != "Failed to load lyrics") {
                            lyricsText.lines().take(2).joinToString("\n")
                        } else {
                            lyricsText
                        }
                        Text(
                            text = peekLyrics,
                            style = MaterialTheme.typography.bodyLarge,
                            color = Color.White.copy(alpha = 0.7f),
                            maxLines = if (isLyricsExpanded) Int.MAX_VALUE else 2,
                            overflow = if (isLyricsExpanded) TextOverflow.Clip else TextOverflow.Ellipsis
                        )
                    }
                }
            }
            
            Spacer(modifier = Modifier.height(24.dp))
        }
    }
}

private fun formatTime(ms: Long): String {
    val totalSeconds = ms / 1000
    val minutes = totalSeconds / 60
    val seconds = totalSeconds % 60
    return String.format("%d:%02d", minutes, seconds)
}
