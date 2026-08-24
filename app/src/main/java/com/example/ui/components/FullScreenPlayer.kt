package com.example.ui.components

import androidx.compose.animation.animateContentSize
import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.gestures.detectDragGestures
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.rounded.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.runtime.collectAsState
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.graphicsLayer
import androidx.compose.ui.input.pointer.pointerInput
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import androidx.compose.ui.platform.LocalView
import android.view.HapticFeedbackConstants
import androidx.media3.common.Player
import androidx.media3.session.MediaController
import coil.compose.AsyncImage
import kotlinx.coroutines.delay

import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.itemsIndexed
import androidx.compose.foundation.lazy.rememberLazyListState
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import com.example.utils.LrcLine
import com.example.viewmodel.MainViewModel

@OptIn(ExperimentalMaterial3Api::class, androidx.compose.animation.ExperimentalSharedTransitionApi::class)
@Composable
fun FullScreenPlayer(
    controller: MediaController?,
    dominantColor: Color?,
    viewModel: MainViewModel,
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

    LaunchedEffect(controller) {
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
            delay(100) // Fast update for smooth lyrics and progress
        }
    }

    val progress = if (duration > 0) currentPosition.toFloat() / duration.toFloat() else 0f
    
    // Dynamic Gradient based on dominantColor (Spotify style)
    val topColor = dominantColor ?: Color.DarkGray
    val bottomColor = Color(0xFF121212)

    Box(
        modifier = Modifier
            .fillMaxSize()
            .background(Brush.verticalGradient(listOf(topColor.copy(alpha = 0.6f), bottomColor)))
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
                    view.performHapticFeedback(HapticFeedbackConstants.VIRTUAL_KEY)
                    onClose()
                }) {
                    Icon(Icons.Rounded.KeyboardArrowDown, contentDescription = "Close", tint = Color.White)
                }
                Column(horizontalAlignment = Alignment.CenterHorizontally) {
                    Text(
                        text = "Now Playing",
                        style = MaterialTheme.typography.labelMedium,
                        color = Color.White.copy(alpha = 0.7f),
                        fontWeight = FontWeight.Bold
                    )
                }
                Spacer(modifier = Modifier.size(48.dp)) // To balance the back button
            }

            Spacer(modifier = Modifier.weight(0.2f))

            // Cover Art
            with(sharedTransitionScope) {
                Box(
                    modifier = Modifier
                        .fillMaxWidth()
                        .aspectRatio(1f)
                        .sharedElement(
                            state = rememberSharedContentState(key = "album_art"),
                            animatedVisibilityScope = animatedVisibilityScope
                        )
                        .clip(RoundedCornerShape(8.dp))
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
                        modifier = Modifier.size(100.dp),
                        tint = Color.White.copy(alpha = 0.3f)
                    )
                }
                }
            }

            Spacer(modifier = Modifier.weight(0.3f))

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
                        overflow = TextOverflow.Ellipsis
                    )
                    Spacer(modifier = Modifier.height(4.dp))
                    Text(
                        text = currentArtist,
                        style = MaterialTheme.typography.titleMedium,
                        color = Color.White.copy(alpha = 0.7f),
                        maxLines = 1,
                        overflow = TextOverflow.Ellipsis
                    )
                }
                val currentUri = controller?.currentMediaItem?.localConfiguration?.uri?.toString() ?: ""
                val isLiked by viewModel.isLiked(currentUri).collectAsStateWithLifecycle(initialValue = false)
                IconButton(onClick = { 
                    view.performHapticFeedback(HapticFeedbackConstants.VIRTUAL_KEY)
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
                    .height(24.dp), // Thinner look
                colors = SliderDefaults.colors(
                    thumbColor = Color.White,
                    activeTrackColor = Color.White,
                    inactiveTrackColor = Color.White.copy(alpha = 0.3f)
                )
            )
            Row(
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(top = 4.dp),
                horizontalArrangement = Arrangement.SpaceBetween
            ) {
                Text(formatTime(currentPosition), style = MaterialTheme.typography.labelMedium, color = Color.White.copy(alpha = 0.7f))
                Text(formatTime(duration), style = MaterialTheme.typography.labelMedium, color = Color.White.copy(alpha = 0.7f))
            }

            Spacer(modifier = Modifier.height(16.dp))

            // Playback Controls
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.SpaceBetween,
                verticalAlignment = Alignment.CenterVertically
            ) {
                var isShuffle by remember { mutableStateOf(controller?.shuffleModeEnabled == true) }
                IconButton(onClick = { 
                    view.performHapticFeedback(HapticFeedbackConstants.VIRTUAL_KEY)
                    controller?.shuffleModeEnabled = !isShuffle
                    isShuffle = !isShuffle
                }) {
                    Icon(Icons.Rounded.Shuffle, contentDescription = "Shuffle", tint = if (isShuffle) Color(0xFF1DB954) else Color.White.copy(alpha = 0.7f))
                }
                IconButton(onClick = { 
                        view.performHapticFeedback(HapticFeedbackConstants.VIRTUAL_KEY)
                        if ((controller?.mediaItemCount ?: 0) <= 1) {
                            val isShuffle = controller?.shuffleModeEnabled == true
                            val repeatMode = controller?.repeatMode ?: Player.REPEAT_MODE_OFF
                            viewModel.playPreviousRemote(isShuffle, repeatMode)
                        } else {
                            controller?.seekToPrevious() 
                        }
                    }) {
                    Icon(Icons.Rounded.SkipPrevious, contentDescription = "Previous", modifier = Modifier.size(48.dp), tint = Color.White)
                }
                
                Box(
                    modifier = Modifier
                        .size(64.dp)
                        .clip(CircleShape)
                        .background(Color.White)
                        .clickable { 
                            view.performHapticFeedback(HapticFeedbackConstants.VIRTUAL_KEY)
                            if (isPlaying) controller?.pause() else controller?.play() 
                        },
                    contentAlignment = Alignment.Center
                ) {
                    Icon(
                        imageVector = if (isPlaying) Icons.Rounded.Pause else Icons.Rounded.PlayArrow,
                        contentDescription = "Play/Pause",
                        modifier = Modifier.size(36.dp),
                        tint = Color.Black
                    )
                }
                
                IconButton(onClick = { 
                        view.performHapticFeedback(HapticFeedbackConstants.VIRTUAL_KEY)
                        if ((controller?.mediaItemCount ?: 0) <= 1) {
                            val isShuffle = controller?.shuffleModeEnabled == true
                            val repeatMode = controller?.repeatMode ?: Player.REPEAT_MODE_OFF
                            viewModel.playNextRemote(isShuffle, repeatMode)
                        } else {
                            controller?.seekToNext() 
                        }
                    }) {
                    Icon(Icons.Rounded.SkipNext, contentDescription = "Next", modifier = Modifier.size(48.dp), tint = Color.White)
                }
                var repeatMode by remember { mutableStateOf(controller?.repeatMode ?: Player.REPEAT_MODE_OFF) }
                IconButton(onClick = { 
                    view.performHapticFeedback(HapticFeedbackConstants.VIRTUAL_KEY)
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

            Spacer(modifier = Modifier.height(16.dp))
            


            // Lyrics Peek Box
            Box(
                modifier = Modifier
                    .fillMaxWidth()
                    .heightIn(min = 90.dp)
                    .clip(RoundedCornerShape(16.dp))
                    .background(if (isLyricsExpanded) Color.Black.copy(alpha = 0.6f) else Color.White.copy(alpha = 0.1f))
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
                                val lines = lrcState!!
                                val idx = lines.indexOfLast { it.timeMs <= currentPosition }
                                if (idx == -1) 0 else idx
                            }
                        }
                        
                        val listState = rememberLazyListState()
                        LaunchedEffect(activeLineIndex) {
                            if (isLyricsExpanded && lrcState!!.isNotEmpty()) {
                                // Smooth scroll to keep active line near center
                                val targetIdx = maxOf(0, activeLineIndex - 2)
                                listState.animateScrollToItem(targetIdx)
                            }
                        }
                        
                        LazyColumn(
                            state = listState,
                            modifier = Modifier.fillMaxSize(),
                            contentPadding = PaddingValues(bottom = if (isLyricsExpanded) 64.dp else 0.dp)
                        ) {
                            itemsIndexed(lrcState!!) { index, line ->
                                val isActive = index == activeLineIndex
                                val alpha = if (isActive) 1f else 0.4f
                                val scale = if (isActive) 1.05f else 1f
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
