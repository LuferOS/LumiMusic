package com.example

import android.content.ComponentName
import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import androidx.activity.viewModels
import androidx.compose.foundation.background
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
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.viewinterop.AndroidView
import androidx.core.graphics.drawable.toBitmap
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import androidx.media3.common.MediaItem
import androidx.media3.common.Player
import androidx.media3.session.MediaController
import androidx.media3.session.SessionToken
import androidx.media3.ui.PlayerView
import androidx.palette.graphics.Palette
import coil.compose.AsyncImage
import coil.request.ImageRequest
import com.example.data.Downloader
import com.example.player.PlaybackService
import com.example.ui.theme.MyApplicationTheme
import com.example.utils.Utils
import com.example.viewmodel.DownloadState
import com.example.viewmodel.MainViewModel
import androidx.compose.animation.togetherWith
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import com.example.viewmodel.LocalMusicViewModel
import com.example.viewmodel.ProfileViewModel
import com.example.ui.screens.ProfileScreen
import androidx.compose.material.icons.filled.*
import android.Manifest
import android.content.pm.PackageManager
import android.os.Build
import androidx.core.content.ContextCompat
import androidx.activity.result.contract.ActivityResultContracts
import com.google.common.util.concurrent.ListenableFuture
import com.google.common.util.concurrent.MoreExecutors
import kotlinx.coroutines.delay

import com.example.ui.components.MiniPlayer
import com.example.ui.components.LyricsBottomSheet

class MainActivity : ComponentActivity() {
    private val viewModel: MainViewModel by viewModels()
    private val localMusicViewModel: LocalMusicViewModel by viewModels()
    private val profileViewModel: ProfileViewModel by viewModels()
    private var controllerFuture: ListenableFuture<MediaController>? = null
    private var mediaController: MediaController? by mutableStateOf(null)

    private val requestPermissionLauncher = registerForActivityResult(
        ActivityResultContracts.RequestPermission()
    ) { isGranted: Boolean ->
        if (isGranted) {
            localMusicViewModel.loadLocalMusic(this)
        }
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        setContent {
            val userStats by profileViewModel.userStats.collectAsStateWithLifecycle()
            var dominantColor by remember { mutableStateOf<Color?>(null) }
            var showLyrics by remember { mutableStateOf(false) }

            // Decide active color based on user setting or extracted cover color
            val activeColor = if (userStats.extractAlbumColor && dominantColor != null) {
                dominantColor!!
            } else {
                try { Color(android.graphics.Color.parseColor(userStats.primaryColorHex)) } catch(e: Exception) { Color(0xFF00FFFF) }
            }

            MyApplicationTheme(
                primaryColorHex = userStats.primaryColorHex,
                bgColorHex = userStats.bgColorHex,
                fontPref = userStats.fontPreference,
                dynamicColor = false
            ) {
                Surface(
                    modifier = Modifier.fillMaxSize(),
                    color = MaterialTheme.colorScheme.background
                ) {
                    var selectedTab by remember { mutableStateOf(0) }

                    if (showLyrics) {
                        LyricsBottomSheet(viewModel = viewModel) {
                            showLyrics = false
                        }
                    }

                    Scaffold(
                        bottomBar = {
                            Column {
                                MiniPlayer(
                                    controller = mediaController,
                                    dominantColor = activeColor,
                                    onShowLyrics = {
                                        val title = mediaController?.currentMediaItem?.mediaMetadata?.title?.toString()
                                        val artist = mediaController?.currentMediaItem?.mediaMetadata?.artist?.toString()
                                        if (!title.isNullOrBlank()) {
                                            viewModel.fetchLyrics(title, artist ?: "")
                                        }
                                        showLyrics = true
                                    }
                                )
                                NavigationBar(
                                    containerColor = MaterialTheme.colorScheme.background,
                                    contentColor = activeColor
                                ) {
                                    NavigationBarItem(
                                        icon = { Icon(Icons.Rounded.Search, contentDescription = "Online") },
                                        label = { Text("Online") },
                                        selected = selectedTab == 0,
                                        onClick = { selectedTab = 0 },
                                        colors = NavigationBarItemDefaults.colors(indicatorColor = activeColor.copy(alpha = 0.2f), selectedIconColor = activeColor, selectedTextColor = activeColor)
                                    )
                                    NavigationBarItem(
                                        icon = { Icon(Icons.Rounded.List, contentDescription = "Local") },
                                        label = { Text("Local") },
                                        selected = selectedTab == 1,
                                        onClick = { 
                                            selectedTab = 1
                                            checkAndRequestPermissions()
                                        },
                                        colors = NavigationBarItemDefaults.colors(indicatorColor = activeColor.copy(alpha = 0.2f), selectedIconColor = activeColor, selectedTextColor = activeColor)
                                    )
                                    NavigationBarItem(
                                        icon = { Icon(Icons.Rounded.Person, contentDescription = "Profile") },
                                        label = { Text("Profile") },
                                        selected = selectedTab == 2,
                                        onClick = { selectedTab = 2 },
                                        colors = NavigationBarItemDefaults.colors(indicatorColor = activeColor.copy(alpha = 0.2f), selectedIconColor = activeColor, selectedTextColor = activeColor)
                                    )
                                }
                            }
                        }
                    ) { padding ->
                        Box(modifier = Modifier.padding(padding)) {
                            androidx.compose.animation.AnimatedContent(
                                targetState = selectedTab,
                                transitionSpec = {
                                    androidx.compose.animation.slideInHorizontally { width -> if (targetState > initialState) width else -width } + androidx.compose.animation.fadeIn() togetherWith
                                    androidx.compose.animation.slideOutHorizontally { width -> if (targetState > initialState) -width else width } + androidx.compose.animation.fadeOut()
                                },
                                label = "TabTransition"
                            ) { tab ->
                                when (tab) {
                                    0 -> MainScreen(
                                        viewModel = viewModel,
                                        profileViewModel = profileViewModel,
                                        controller = mediaController,
                                        onColorExtracted = { color -> dominantColor = color },
                                        dominantColor = activeColor
                                    )
                                    1 -> LocalMusicScreen(
                                        viewModel = localMusicViewModel,
                                        controller = mediaController,
                                        dominantColor = activeColor
                                    )
                                    2 -> ProfileScreen(
                                        viewModel = profileViewModel,
                                        dominantColor = activeColor
                                    )
                                }
                            }
                        }
                    }
                }
            }
        }
    }

    override fun onStart() {
        super.onStart()
        val sessionToken = SessionToken(this, ComponentName(this, PlaybackService::class.java))
        controllerFuture = MediaController.Builder(this, sessionToken).buildAsync()
        controllerFuture?.addListener(
            {
                mediaController = controllerFuture?.get()
            },
            MoreExecutors.directExecutor()
        )
    }

    private fun checkAndRequestPermissions() {
        val permission = if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.TIRAMISU) {
            Manifest.permission.READ_MEDIA_AUDIO
        } else {
            Manifest.permission.READ_EXTERNAL_STORAGE
        }

        if (ContextCompat.checkSelfPermission(this, permission) == PackageManager.PERMISSION_GRANTED) {
            localMusicViewModel.loadLocalMusic(this)
        } else {
            requestPermissionLauncher.launch(permission)
        }
    }

    override fun onStop() {
        super.onStop()
        controllerFuture?.let { MediaController.releaseFuture(it) }
    }
}

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun MainScreen(
    viewModel: MainViewModel,
    profileViewModel: ProfileViewModel,
    controller: MediaController?,
    onColorExtracted: (Color) -> Unit,
    dominantColor: Color?
) {
    var urlInput by remember { mutableStateOf("") }
    val downloadState by viewModel.downloadState.collectAsStateWithLifecycle()
    val searchState by viewModel.searchState.collectAsStateWithLifecycle()
    val context = LocalContext.current
    var isVideoMode by remember { mutableStateOf(false) }
    val userStats by profileViewModel.userStats.collectAsStateWithLifecycle()

    // Media State
    var isPlaying by remember { mutableStateOf(false) }
    var currentPosition by remember { mutableStateOf(0L) }
    var duration by remember { mutableStateOf(0L) }

    LaunchedEffect(controller) {
        if (controller == null) return@LaunchedEffect
        controller.addListener(object : Player.Listener {
            override fun onIsPlayingChanged(playing: Boolean) {
                isPlaying = playing
            }
            override fun onPlaybackStateChanged(playbackState: Int) {
                if (playbackState == Player.STATE_READY) {
                    duration = controller.duration.coerceAtLeast(0L)
                }
            }
        })
    }
    
    LaunchedEffect(controller, isPlaying) {
        if (controller == null || !isPlaying) return@LaunchedEffect
        var secondsAccumulated = 0L
        while (isPlaying) {
            currentPosition = controller.currentPosition.coerceAtLeast(0L)
            secondsAccumulated++
            if (secondsAccumulated >= 5) {
                profileViewModel.recordListeningTime(5)
                secondsAccumulated = 0
            }
            delay(1000)
        }
    }

    Column(
        modifier = Modifier
            .fillMaxSize()
            .padding(16.dp)
            .statusBarsPadding(),
        horizontalAlignment = Alignment.CenterHorizontally
    ) {
        OutlinedTextField(
            value = urlInput,
            onValueChange = { urlInput = it },
            label = { Text("Search Tracks (Spotify/YT)") },
            modifier = Modifier.fillMaxWidth(),
            shape = RoundedCornerShape(32.dp),
            singleLine = true,
            trailingIcon = {
                IconButton(onClick = { viewModel.searchITunes(urlInput) }) {
                    Icon(Icons.Rounded.Search, contentDescription = "Search")
                }
            },
            colors = OutlinedTextFieldDefaults.colors(
                focusedBorderColor = dominantColor ?: MaterialTheme.colorScheme.primary,
                focusedLabelColor = dominantColor ?: MaterialTheme.colorScheme.primary
            )
        )

        Spacer(modifier = Modifier.height(24.dp))

        androidx.compose.animation.AnimatedContent(
            targetState = Pair(downloadState, searchState),
            label = "ScreenStateTransition",
            modifier = Modifier.fillMaxSize()
        ) { (dlState, sState) ->
            if (dlState is DownloadState.Loading || sState is com.example.viewmodel.SearchState.Loading) {
                Box(modifier = Modifier.fillMaxSize(), contentAlignment = Alignment.Center) {
                    CircularProgressIndicator(color = dominantColor ?: MaterialTheme.colorScheme.primary)
                }
            } else if (dlState is DownloadState.Success) {
                val thumbnailUrl = dlState.thumbnail
                Column(horizontalAlignment = Alignment.CenterHorizontally) {
                    Row(verticalAlignment = Alignment.CenterVertically) {
                        Text("Audio")
                        Switch(
                            checked = isVideoMode,
                            onCheckedChange = { isVideoMode = it },
                            modifier = Modifier.padding(horizontal = 8.dp),
                            colors = SwitchDefaults.colors(
                                checkedThumbColor = dominantColor ?: MaterialTheme.colorScheme.primary,
                                checkedTrackColor = (dominantColor ?: MaterialTheme.colorScheme.primary).copy(alpha = 0.5f)
                            )
                        )
                        Text("Video")
                    }

                    Spacer(modifier = Modifier.height(16.dp))

                    Box(
                        modifier = Modifier
                            .fillMaxWidth()
                            .aspectRatio(16f / 9f)
                            .clip(RoundedCornerShape(32.dp))
                            .background(Color.Black)
                    ) {
                        androidx.compose.animation.AnimatedContent(
                            targetState = isVideoMode,
                            label = "MediaModeTransition"
                        ) { isVideo ->
                            if (isVideo) {
                                if (controller != null) {
                                    AndroidView(
                                        factory = { ctx ->
                                            androidx.media3.ui.PlayerView(ctx).apply {
                                                player = controller
                                                useController = false
                                            }
                                        },
                                        modifier = Modifier.fillMaxSize()
                                    )
                                }
                            } else {
                                coil.compose.AsyncImage(
                                    model = coil.request.ImageRequest.Builder(context)
                                        .data(thumbnailUrl)
                                        .crossfade(true)
                                        .allowHardware(false)
                                        .build(),
                                    contentDescription = "Thumbnail",
                                    contentScale = androidx.compose.ui.layout.ContentScale.Crop,
                                    modifier = Modifier.fillMaxSize(),
                                    onSuccess = { result ->
                                        val bitmap = result.result.drawable.toBitmap()
                                        androidx.palette.graphics.Palette.from(bitmap).generate { palette ->
                                            palette?.dominantSwatch?.rgb?.let { colorInt ->
                                                onColorExtracted(Color(colorInt))
                                            }
                                        }
                                    }
                                )
                            }
                        }
                    }

                    Spacer(modifier = Modifier.height(24.dp))

                    Text(
                        text = dlState.title,
                        style = MaterialTheme.typography.titleLarge,
                        fontWeight = FontWeight.Bold,
                        maxLines = 2
                    )

                    Spacer(modifier = Modifier.height(24.dp))

                    Slider(
                        value = if (duration > 0) currentPosition.toFloat() / duration.toFloat() else 0f,
                        onValueChange = {
                            if (duration > 0) {
                                controller?.seekTo((it * duration).toLong())
                            }
                        },
                        modifier = Modifier.fillMaxWidth(),
                        colors = SliderDefaults.colors(
                            thumbColor = dominantColor ?: MaterialTheme.colorScheme.primary,
                            activeTrackColor = dominantColor ?: MaterialTheme.colorScheme.primary
                        )
                    )

                    Row(
                        horizontalArrangement = Arrangement.Center,
                        verticalAlignment = Alignment.CenterVertically,
                        modifier = Modifier.fillMaxWidth()
                    ) {
                        FloatingActionButton(
                            onClick = {
                                if (controller != null) {
                                    if (controller.playbackState == androidx.media3.common.Player.STATE_IDLE || controller.playbackState == androidx.media3.common.Player.STATE_ENDED) {
                                        val mediaItem = androidx.media3.common.MediaItem.Builder().setUri(dlState.url).setMediaMetadata(androidx.media3.common.MediaMetadata.Builder().setTitle(dlState.title).build()).build()
                                        controller.setMediaItem(mediaItem)
                                        controller.prepare()
                                        controller.play()
                                    } else {
                                        if (controller.isPlaying) controller.pause() else controller.play()
                                    }
                                }
                            },
                            shape = RoundedCornerShape(32.dp),
                            containerColor = dominantColor ?: MaterialTheme.colorScheme.primaryContainer,
                            modifier = Modifier.size(80.dp)
                        ) {
                            androidx.compose.animation.AnimatedContent(targetState = isPlaying, label = "PlayPause") { playing ->
                                Icon(
                                    imageVector = if (playing) Icons.Rounded.Pause else Icons.Rounded.PlayArrow,
                                    contentDescription = "Play/Pause",
                                    modifier = Modifier.size(48.dp)
                                )
                            }
                        }
                    }

                    Spacer(modifier = Modifier.height(32.dp))

                    Row {
                        Button(
                            onClick = {
                                val mediaItem = androidx.media3.common.MediaItem.Builder().setUri(dlState.url).setMediaMetadata(androidx.media3.common.MediaMetadata.Builder().setTitle(dlState.title).build()).build()
                                controller?.setMediaItem(mediaItem)
                                controller?.prepare()
                                controller?.play()
                            },
                            colors = ButtonDefaults.buttonColors(containerColor = dominantColor ?: MaterialTheme.colorScheme.primary)
                        ) {
                            Text("Play Online")
                        }
                        Spacer(modifier = Modifier.width(16.dp))
                        Button(
                            onClick = { 
                                com.example.data.Downloader.downloadMp3(context, dlState.url, dlState.title)
                                profileViewModel.recordDownload()
                            },
                            colors = ButtonDefaults.buttonColors(containerColor = MaterialTheme.colorScheme.secondary)
                        ) {
                            Icon(Icons.Rounded.Download, contentDescription = null, modifier = Modifier.size(18.dp))
                            Spacer(modifier = Modifier.width(8.dp))
                            Text("Download")
                        }
                    }
                }
            } else if (sState is com.example.viewmodel.SearchState.Success) {
                LazyColumn(
                    modifier = Modifier.fillMaxSize()
                ) {
                    items(sState.results) { track ->
                        Card(
                            modifier = Modifier
                                .fillMaxWidth()
                                .padding(vertical = 4.dp),
                            shape = RoundedCornerShape(16.dp),
                            colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surfaceVariant),
                            onClick = {
                                viewModel.selectTrack(track.trackName ?: "", track.artistName ?: "", userStats.apiPreference)
                            }
                        ) {
                            Row(
                                modifier = Modifier.padding(12.dp),
                                verticalAlignment = Alignment.CenterVertically
                            ) {
                                coil.compose.AsyncImage(
                                    model = track.artworkUrl100,
                                    contentDescription = null,
                                    modifier = Modifier
                                        .size(56.dp)
                                        .clip(RoundedCornerShape(8.dp))
                                )
                                Spacer(modifier = Modifier.width(16.dp))
                                Column(modifier = Modifier.weight(1f)) {
                                    Text(text = track.trackName ?: "Unknown", fontWeight = FontWeight.Bold, maxLines = 1)
                                    Text(text = track.artistName ?: "Unknown", style = MaterialTheme.typography.bodyMedium, color = MaterialTheme.colorScheme.onSurfaceVariant, maxLines = 1)
                                }
                                Icon(Icons.Rounded.PlayArrow, contentDescription = "Select", tint = dominantColor ?: MaterialTheme.colorScheme.primary)
                            }
                        }
                    }
                }
            } else if (dlState is DownloadState.Error) {
                Box(modifier = Modifier.fillMaxSize(), contentAlignment = Alignment.Center) {
                    Text(dlState.message, color = MaterialTheme.colorScheme.error)
                }
            } else if (sState is com.example.viewmodel.SearchState.Error) {
                Box(modifier = Modifier.fillMaxSize(), contentAlignment = Alignment.Center) {
                    Text(sState.message, color = MaterialTheme.colorScheme.error)
                }
            } else {
                Box(modifier = Modifier.fillMaxSize(), contentAlignment = Alignment.Center) {
                    Column(horizontalAlignment = Alignment.CenterHorizontally) {
                        Icon(Icons.Rounded.Search, contentDescription = null, modifier = Modifier.size(64.dp), tint = MaterialTheme.colorScheme.onSurfaceVariant.copy(alpha = 0.5f))
                        Spacer(modifier = Modifier.height(16.dp))
                        Text("Search for your favorite tracks", color = MaterialTheme.colorScheme.onSurfaceVariant.copy(alpha = 0.5f))
                    }
                }
            }
        }
    }
}

@Composable
fun LocalMusicScreen(
    viewModel: LocalMusicViewModel,
    controller: MediaController?,
    dominantColor: Color?
) {
    val musicList by viewModel.localMusicList.collectAsStateWithLifecycle()
    var searchQuery by remember { mutableStateOf("") }
    var sortType by remember { mutableStateOf(0) } // 0: Title A-Z, 1: Title Z-A, 2: Artist A-Z
    
    val baseFilteredList = if (searchQuery.isBlank()) {
        musicList
    } else {
        musicList.filter { it.title.contains(searchQuery, ignoreCase = true) || it.artist.contains(searchQuery, ignoreCase = true) }
    }

    val filteredList = when(sortType) {
        0 -> baseFilteredList.sortedBy { it.title }
        1 -> baseFilteredList.sortedByDescending { it.title }
        2 -> baseFilteredList.sortedBy { it.artist }
        else -> baseFilteredList
    }

    Column(modifier = Modifier.fillMaxSize()) {
        Row(
            modifier = Modifier
                .fillMaxWidth()
                .padding(16.dp),
            verticalAlignment = Alignment.CenterVertically,
            horizontalArrangement = Arrangement.SpaceBetween
        ) {
            Text(
                text = "Local Music",
                style = MaterialTheme.typography.headlineMedium,
                fontWeight = FontWeight.Bold
            )
            Row {
                IconButton(onClick = { sortType = (sortType + 1) % 3 }) {
                    Icon(
                        imageVector = if (sortType == 2) Icons.Rounded.Person else Icons.Rounded.SortByAlpha,
                        contentDescription = "Sort",
                        tint = dominantColor ?: MaterialTheme.colorScheme.primary
                    )
                }
                IconButton(
                    onClick = {
                        if (filteredList.isNotEmpty() && controller != null) {
                            val shuffled = filteredList.shuffled()
                            controller.clearMediaItems()
                            shuffled.forEach { audio ->
                                controller.addMediaItem(androidx.media3.common.MediaItem.Builder().setUri(audio.uri).setMediaMetadata(androidx.media3.common.MediaMetadata.Builder().setTitle(audio.title).setArtist(audio.artist).build()).build())
                            }
                            controller.shuffleModeEnabled = false // We already shuffled the list
                            controller.prepare()
                            controller.play()
                        }
                    }
                ) {
                    Icon(
                        imageVector = Icons.Rounded.Shuffle,
                        contentDescription = "Shuffle Play",
                        tint = dominantColor ?: MaterialTheme.colorScheme.primary
                    )
                }
            }
        }
        
        OutlinedTextField(
            value = searchQuery,
            onValueChange = { searchQuery = it },
            label = { Text("Search local tracks (Title/Artist)") },
            modifier = Modifier
                .fillMaxWidth()
                .padding(horizontal = 16.dp),
            shape = RoundedCornerShape(32.dp),
            singleLine = true,
            leadingIcon = { Icon(Icons.Rounded.Search, contentDescription = null) },
            colors = OutlinedTextFieldDefaults.colors(
                focusedBorderColor = dominantColor ?: MaterialTheme.colorScheme.primary,
                focusedLabelColor = dominantColor ?: MaterialTheme.colorScheme.primary
            )
        )
        
        Spacer(modifier = Modifier.height(8.dp))

        if (musicList.isEmpty()) {
            Box(modifier = Modifier.fillMaxSize(), contentAlignment = Alignment.Center) {
                Text("No local music found.")
            }
        } else {
            androidx.compose.animation.AnimatedContent(
                targetState = filteredList.isEmpty(),
                label = "LocalSearchTransition"
            ) { empty ->
                if (empty) {
                    Box(modifier = Modifier.fillMaxSize(), contentAlignment = Alignment.Center) {
                        Text("No matching tracks found.")
                    }
                } else {
                    LazyColumn(
                        modifier = Modifier.fillMaxSize(),
                        contentPadding = PaddingValues(16.dp)
                    ) {
                        items(filteredList, key = { it.id }) { audio ->
                            Card(
                                modifier = Modifier
                                    .fillMaxWidth()
                                    .padding(vertical = 8.dp),
                                shape = RoundedCornerShape(24.dp),
                                colors = CardDefaults.cardColors(
                                    containerColor = MaterialTheme.colorScheme.surfaceVariant
                                ),
                                onClick = {
                                    val mediaItem = androidx.media3.common.MediaItem.Builder().setUri(audio.uri).setMediaMetadata(androidx.media3.common.MediaMetadata.Builder().setTitle(audio.title).setArtist(audio.artist).build()).build()
                                    controller?.setMediaItem(mediaItem)
                                    controller?.prepare()
                                    controller?.play()
                                }
                            ) {
                                Row(
                                    modifier = Modifier.padding(16.dp),
                                    verticalAlignment = Alignment.CenterVertically
                                ) {
                                    Icon(
                                        Icons.Rounded.MusicNote,
                                        contentDescription = null,
                                        modifier = Modifier
                                            .size(48.dp)
                                            .background(
                                                dominantColor ?: MaterialTheme.colorScheme.primaryContainer,
                                                shape = RoundedCornerShape(16.dp)
                                            )
                                            .padding(12.dp)
                                    )
                                    Spacer(modifier = Modifier.width(16.dp))
                                    Column(modifier = Modifier.weight(1f)) {
                                        Text(
                                            text = audio.title,
                                            style = MaterialTheme.typography.titleMedium,
                                            fontWeight = FontWeight.Bold,
                                            maxLines = 1
                                        )
                                        Text(
                                            text = audio.artist,
                                            style = MaterialTheme.typography.bodyMedium,
                                            color = MaterialTheme.colorScheme.onSurfaceVariant,
                                            maxLines = 1
                                        )
                                    }
                                    Icon(
                                        Icons.Rounded.PlayArrow,
                                        contentDescription = "Play",
                                        tint = dominantColor ?: MaterialTheme.colorScheme.primary
                                    )
                                }
                            }
                        }
                    }
                }
            }
        }
    }
}

