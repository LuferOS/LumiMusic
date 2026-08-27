package com.example

import android.content.ComponentName
import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import androidx.activity.viewModels
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.clickable
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.rounded.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import com.example.utils.bouncyClick
import androidx.compose.foundation.basicMarquee
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.text.style.TextOverflow
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
import androidx.compose.foundation.lazy.grid.LazyVerticalGrid
import androidx.compose.foundation.lazy.grid.GridCells
import androidx.compose.foundation.lazy.grid.items
import androidx.compose.foundation.lazy.items
import com.example.viewmodel.LocalMusicViewModel
import com.example.viewmodel.ProfileViewModel
import com.example.ui.screens.ProfileScreen
import com.example.ui.screens.LocalMusicScreen
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
import com.example.ui.components.FullScreenPlayer
import com.example.ui.components.LyricsBottomSheet
import com.example.ui.components.AudioSettingsBottomSheet

@OptIn(androidx.compose.animation.ExperimentalSharedTransitionApi::class)
class MainActivity : ComponentActivity() {
    private val viewModel: MainViewModel by viewModels()
    private val localMusicViewModel: LocalMusicViewModel by viewModels()
    private val profileViewModel: ProfileViewModel by viewModels()
    private var controllerFuture: ListenableFuture<MediaController>? = null
    private var mediaController: MediaController? by mutableStateOf(null)

    private val requestPermissionLauncher = registerForActivityResult(
        ActivityResultContracts.RequestMultiplePermissions()
    ) { permissions ->
        val mediaPermission = if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.TIRAMISU) {
            Manifest.permission.READ_MEDIA_AUDIO
        } else {
            Manifest.permission.READ_EXTERNAL_STORAGE
        }
        
        if (permissions[mediaPermission] == true) {
            localMusicViewModel.loadLocalMusic(this)
        }
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()

        val sessionToken = androidx.media3.session.SessionToken(this, android.content.ComponentName(this, com.example.player.PlaybackService::class.java))
        controllerFuture = androidx.media3.session.MediaController.Builder(this, sessionToken).buildAsync()
        controllerFuture?.addListener(
            {
                mediaController = controllerFuture?.get()
                mediaController?.addListener(object : androidx.media3.common.Player.Listener {
                    override fun onMediaItemTransition(mediaItem: androidx.media3.common.MediaItem?, reason: Int) {
                        super.onMediaItemTransition(mediaItem, reason)
                        if (reason == androidx.media3.common.Player.MEDIA_ITEM_TRANSITION_REASON_AUTO) {
                            // If auto-transition happened, wait and see if we have next item. If not, the player might stop.
                            // However, we want to add random tracks. 
                        }
                    }
                    
                    override fun onPlaybackStateChanged(playbackState: Int) {
                        if (playbackState == androidx.media3.common.Player.STATE_ENDED) {
                            // Queue ended, try next remote, else random
                            if (mediaController?.mediaItemCount == 1) {
                                val isShuffle = mediaController?.shuffleModeEnabled == true
                                val repeatMode = mediaController?.repeatMode ?: androidx.media3.common.Player.REPEAT_MODE_OFF
                                if (!viewModel.playNextRemote(isShuffle, repeatMode)) {
                                    viewModel.playNextRandomTrack(profileViewModel.userStats.value.apiPreference)
                                }
                            }
                        }
                    }
                })
            },
            com.google.common.util.concurrent.MoreExecutors.directExecutor()
        )

        setContent {
            val userStats by profileViewModel.userStats.collectAsStateWithLifecycle()
            var dominantColor by remember { mutableStateOf<Color?>(null) }
            var showFullScreenPlayer by remember { mutableStateOf(false) }

            val activeColor = if (userStats.extractAlbumColor && dominantColor != null) {
                dominantColor!!
            } else {
                try { Color(android.graphics.Color.parseColor(userStats.primaryColorHex)) } catch(e: Exception) { Color(0xFF00FFFF) }
            }

            val updateInfo by viewModel.updateInfo.collectAsStateWithLifecycle()
            val context = androidx.compose.ui.platform.LocalContext.current
            var showUpdateDialog by remember { mutableStateOf(true) }

            MyApplicationTheme(
                primaryColorHex = userStats.primaryColorHex,
                fontPref = userStats.fontPreference,
                dynamicColor = false
            ) {
                com.example.ui.components.UpdateDialog(
                    isAvailable = updateInfo.isAvailable && showUpdateDialog,
                    newVersion = updateInfo.newVersion,
                    updateUrl = updateInfo.updateUrl,
                    releaseNotes = updateInfo.releaseNotes,
                    onDismiss = { showUpdateDialog = false }
                )
                Surface(
                    modifier = Modifier.fillMaxSize(),
                    color = Color.Black
                ) {
                  androidx.compose.animation.SharedTransitionLayout {
                    var selectedTab by remember { mutableStateOf(userStats.startupTab) }
                    var showEqualizer by remember { mutableStateOf(false) }
                    var showSplash by remember { mutableStateOf(true) }
                    
                    LaunchedEffect(Unit) {
                        kotlinx.coroutines.delay(2000)
                        showSplash = false
                    }

                    BoxWithConstraints(modifier = Modifier.fillMaxSize()) {
                        if (showSplash) {
                            com.example.ui.screens.SplashScreen(primaryColor = activeColor)
                        } else if (!userStats.hasSeenOnboarding) {
                            com.example.ui.screens.OnboardingScreen(
                                primaryColor = activeColor,
                                onComplete = { profileViewModel.completeOnboarding() }
                            )
                        } else {
                            val isWideScreen = maxWidth >= 600.dp
                        
                        Scaffold(
                            bottomBar = {
                                Column {
                                    MiniPlayer(viewModel = viewModel, userStats = userStats, 
                                        controller = mediaController,
                                        dominantColor = activeColor,
                                        sharedTransitionScope = this@SharedTransitionLayout,
                                        onExpand = {
                                            val title = mediaController?.currentMediaItem?.mediaMetadata?.title?.toString()
                                            val artist = mediaController?.currentMediaItem?.mediaMetadata?.artist?.toString()
                                            if (!title.isNullOrBlank()) {
                                                viewModel.fetchLyrics(title, artist ?: "")
                                            }
                                            showFullScreenPlayer = true
                                        }
                                    )
                                    if (!isWideScreen) {
                                        NavigationBar(
                                            containerColor = Color.Transparent,
                                            contentColor = Color.White
                                        ) {
                                            val orderIndices = userStats.navOrder.split(",").mapNotNull { it.toIntOrNull() }
                                            val validIndices = if (orderIndices.size == 3 && orderIndices.containsAll(listOf(0,1,2))) orderIndices else listOf(0,1,2)
                                            
                                            validIndices.forEach { tabIndex ->
                                                when (tabIndex) {
                                                    0 -> NavigationBarItem(
                                                        icon = { Icon(Icons.Rounded.Search, contentDescription = "Buscar", modifier = Modifier.size(28.dp).bouncyClick { selectedTab = 0 }) },
                                                        label = { Text("Buscar", style = MaterialTheme.typography.labelSmall) },
                                                        selected = selectedTab == 0,
                                                        onClick = { selectedTab = 0 },
                                                        colors = NavigationBarItemDefaults.colors(
                                                            indicatorColor = Color.Transparent,
                                                            selectedIconColor = Color.White,
                                                            selectedTextColor = Color.White,
                                                            unselectedIconColor = Color.White.copy(alpha = 0.5f),
                                                            unselectedTextColor = Color.White.copy(alpha = 0.5f)
                                                        )
                                                    )
                                                    1 -> NavigationBarItem(
                                                        icon = { Icon(Icons.Rounded.LibraryMusic, contentDescription = "Tu biblioteca", modifier = Modifier.size(28.dp).bouncyClick { selectedTab = 1; checkAndRequestPermissions() }) },
                                                        label = { Text("Tu biblioteca", style = MaterialTheme.typography.labelSmall) },
                                                        selected = selectedTab == 1,
                                                        onClick = { selectedTab = 1; checkAndRequestPermissions() },
                                                        colors = NavigationBarItemDefaults.colors(
                                                            indicatorColor = Color.Transparent,
                                                            selectedIconColor = Color.White,
                                                            selectedTextColor = Color.White,
                                                            unselectedIconColor = Color.White.copy(alpha = 0.5f),
                                                            unselectedTextColor = Color.White.copy(alpha = 0.5f)
                                                        )
                                                    )
                                                    2 -> NavigationBarItem(
                                                        icon = { Icon(Icons.Rounded.Person, contentDescription = "Perfil", modifier = Modifier.size(28.dp).bouncyClick { selectedTab = 2 }) },
                                                        label = { Text("Perfil", style = MaterialTheme.typography.labelSmall) },
                                                        selected = selectedTab == 2,
                                                        onClick = { selectedTab = 2 },
                                                        colors = NavigationBarItemDefaults.colors(
                                                            indicatorColor = Color.Transparent,
                                                            selectedIconColor = Color.White,
                                                            selectedTextColor = Color.White,
                                                            unselectedIconColor = Color.White.copy(alpha = 0.5f),
                                                            unselectedTextColor = Color.White.copy(alpha = 0.5f)
                                                        )
                                                    )
                                                }
                                            }
                                        }
                                    }
                                }
                            }
                        ) { padding ->
                            Row(modifier = Modifier.fillMaxSize().padding(padding)) {
                                if (isWideScreen) {
                                    NavigationRail(
                                        containerColor = MaterialTheme.colorScheme.background,
                                        contentColor = activeColor
                                    ) {
                                        NavigationRailItem(
                                            icon = { Icon(Icons.Rounded.Search, contentDescription = "Online") },
                                            label = { Text("Online") },
                                            selected = selectedTab == 0,
                                            onClick = { selectedTab = 0 },
                                            colors = NavigationRailItemDefaults.colors(indicatorColor = activeColor.copy(alpha = 0.2f), selectedIconColor = activeColor, selectedTextColor = activeColor)
                                        )
                                        NavigationRailItem(
                                            icon = { Icon(Icons.Rounded.LibraryMusic, contentDescription = "Local") },
                                            label = { Text("Local") },
                                            selected = selectedTab == 1,
                                            onClick = { 
                                                selectedTab = 1
                                                checkAndRequestPermissions()
                                            },
                                            colors = NavigationRailItemDefaults.colors(indicatorColor = activeColor.copy(alpha = 0.2f), selectedIconColor = activeColor, selectedTextColor = activeColor)
                                        )
                                        NavigationRailItem(
                                            icon = { Icon(Icons.Rounded.Person, contentDescription = "Profile") },
                                            label = { Text("Profile") },
                                            selected = selectedTab == 2,
                                            onClick = { selectedTab = 2 },
                                            colors = NavigationRailItemDefaults.colors(indicatorColor = activeColor.copy(alpha = 0.2f), selectedIconColor = activeColor, selectedTextColor = activeColor)
                                        )
                                    }
                                }
                                Box(modifier = Modifier.weight(1f)) {
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
                                            1 -> LocalMusicScreen(mainViewModel = viewModel, userStats = userStats, 
                                                viewModel = localMusicViewModel,
                                                controller = mediaController,
                                                dominantColor = activeColor
                                            )
                                            2 -> ProfileScreen(
                                                viewModel = profileViewModel,
                                                dominantColor = activeColor,
                                                onOpenEqualizer = { showEqualizer = true }
                                            )
                                        }
                                    }
                                }
                            }
                        }
                        
                        androidx.compose.animation.AnimatedVisibility(
                            visible = showFullScreenPlayer,
                            enter = androidx.compose.animation.slideInVertically(
                                initialOffsetY = { it }
                            ),
                            exit = androidx.compose.animation.slideOutVertically(
                                targetOffsetY = { it }
                            )
                        ) {
                            FullScreenPlayer(viewModel = viewModel, userStats = userStats, 
                                controller = mediaController,
                                dominantColor = activeColor,
                                sharedTransitionScope = this@SharedTransitionLayout,
                                animatedVisibilityScope = this,
                                onClose = { showFullScreenPlayer = false }
                            )
                        }

                        } // end else
                        if (showEqualizer) {
                            AudioSettingsBottomSheet(controller = mediaController) {
                                showEqualizer = false
                            }
                        }
                    }
                  }
                }
            }
        }
    }

    private fun checkAndRequestPermissions() {
        val permissionsToRequest = mutableListOf<String>()
        val mediaPermission = if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.TIRAMISU) {
            Manifest.permission.READ_MEDIA_AUDIO
        } else {
            Manifest.permission.READ_EXTERNAL_STORAGE
        }
        
        if (ContextCompat.checkSelfPermission(this, mediaPermission) != PackageManager.PERMISSION_GRANTED) {
            permissionsToRequest.add(mediaPermission)
        } else {
            localMusicViewModel.loadLocalMusic(this)
        }

        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.TIRAMISU) {
            if (ContextCompat.checkSelfPermission(this, Manifest.permission.POST_NOTIFICATIONS) != PackageManager.PERMISSION_GRANTED) {
                permissionsToRequest.add(Manifest.permission.POST_NOTIFICATIONS)
            }
        }
        
        if (permissionsToRequest.isNotEmpty()) {
            requestPermissionLauncher.launch(permissionsToRequest.toTypedArray())
        }
    }

    override fun onDestroy() {
        super.onDestroy()
        controllerFuture?.let { androidx.media3.session.MediaController.releaseFuture(it) }
    }
}

@OptIn(ExperimentalMaterial3Api::class, androidx.compose.animation.ExperimentalSharedTransitionApi::class)
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
    val userStats by profileViewModel.userStats.collectAsStateWithLifecycle()

    LaunchedEffect(downloadState) {
        val state = downloadState
        if (state is com.example.viewmodel.DownloadState.Success) {
            if (state.action == "play") {
                val mediaItem = androidx.media3.common.MediaItem.Builder()
                    .setUri(state.url)
                    .setMediaMetadata(
                        androidx.media3.common.MediaMetadata.Builder()
                            .setTitle(state.title)
                            .setArtist(state.title) // Fallback if artist not fully parsed
                            .build()
                    ).build()
                controller?.setMediaItem(mediaItem)
                controller?.prepare()
                controller?.play()
                
                // Extract color if needed
                if (state.thumbnail != null) {
                    val request = coil.request.ImageRequest.Builder(context)
                        .data(state.thumbnail)
                        .allowHardware(false)
                        .build()
                    val result = coil.ImageLoader(context).execute(request)
                    if (result is coil.request.SuccessResult) {
                        val bitmap = (result.drawable as? android.graphics.drawable.BitmapDrawable)?.bitmap
                        if (bitmap != null) {
                            androidx.palette.graphics.Palette.from(bitmap).generate { palette ->
                                palette?.dominantSwatch?.rgb?.let { colorInt ->
                                    onColorExtracted(Color(colorInt))
                                }
                            }
                        }
                    }
                }
            } else if (state.action == "download") {
                com.example.data.Downloader.downloadMp3(context, state.url, state.title)
                profileViewModel.recordDownload()
            }
            viewModel.resetState() // Go back to idle to hide loading
        }
    }

    Column(modifier = Modifier.fillMaxSize()) {
        // Search Header
        Column(
            modifier = Modifier
                .fillMaxWidth()
                .background(Color(0xFF121212))
                .padding(horizontal = 16.dp, vertical = 8.dp)
        ) {
            TextField(
                value = urlInput,
                onValueChange = { urlInput = it },
                placeholder = { Text("¿Qué quieres escuchar?", color = Color.White.copy(alpha = 0.5f), style = MaterialTheme.typography.bodyLarge) },
                modifier = Modifier
                    .fillMaxWidth()
                    .clip(RoundedCornerShape(8.dp)),
                leadingIcon = { Icon(Icons.Rounded.Search, contentDescription = "Search", tint = Color.White) },
                singleLine = true,
                keyboardOptions = androidx.compose.foundation.text.KeyboardOptions(imeAction = androidx.compose.ui.text.input.ImeAction.Search),
                keyboardActions = androidx.compose.foundation.text.KeyboardActions(
                    onSearch = {
                        if (urlInput.isNotBlank()) viewModel.searchITunes(urlInput)
                    }
                ),
                colors = TextFieldDefaults.colors(
                    focusedContainerColor = Color(0xFF242424),
                    unfocusedContainerColor = Color(0xFF242424),
                    focusedIndicatorColor = Color.Transparent,
                    unfocusedIndicatorColor = Color.Transparent,
                    focusedTextColor = Color.White,
                    unfocusedTextColor = Color.White,
                    cursorColor = Color.White
                )
            )
        }

        Box(modifier = Modifier.weight(1f)) {
            val sState = searchState
            val dlState = downloadState

            if (sState is com.example.viewmodel.SearchState.Success) {
                if (sState.results.isEmpty()) {
                    Column(
                        modifier = Modifier.fillMaxSize().padding(32.dp),
                        horizontalAlignment = Alignment.CenterHorizontally,
                        verticalArrangement = Arrangement.Center
                    ) {
                        Icon(Icons.Rounded.SearchOff, contentDescription = null, modifier = Modifier.size(64.dp), tint = Color.White.copy(alpha=0.3f))
                        Spacer(modifier = Modifier.height(16.dp))
                        Text("No se encontraron resultados", color = Color.White.copy(alpha=0.5f), style = MaterialTheme.typography.bodyLarge)
                    }
                } else {
                LazyVerticalGrid(
                    columns = GridCells.Adaptive(minSize = 350.dp),
                    modifier = Modifier.fillMaxSize(),
                    contentPadding = PaddingValues(bottom = 100.dp)
                ) {
                    items(sState.results.size) { index ->
                        val track = sState.results[index]
                        Row(
                            modifier = Modifier
                                .fillMaxWidth()
                                .padding(horizontal = 8.dp, vertical = 2.dp)
                                .clip(RoundedCornerShape(12.dp))
                                .clickable { viewModel.playFromRemotePlaylist(sState.results, index, userStats.apiPreference) }
                                .padding(horizontal = 8.dp, vertical = 8.dp),
                            verticalAlignment = Alignment.CenterVertically
                        ) {
                            coil.compose.AsyncImage(
                                model = track.artworkUrl100,
                                contentDescription = null,
                                modifier = Modifier
                                    .size(56.dp)
                                    .clip(RoundedCornerShape(4.dp))
                            )
                            Spacer(modifier = Modifier.width(16.dp))
                            Column(modifier = Modifier.weight(1f)) {
                                Text(text = track.trackName ?: "Unknown", color = Color.White, style = MaterialTheme.typography.bodyLarge, fontWeight = FontWeight.Normal, maxLines = 1, modifier = Modifier.basicMarquee())
                                Spacer(modifier = Modifier.height(2.dp))
                                Text(text = "Canción • ${track.artistName ?: "Unknown"}", style = MaterialTheme.typography.bodyMedium, color = Color.White.copy(alpha = 0.6f), maxLines = 1, modifier = Modifier.basicMarquee())
                            }
                            IconButton(onClick = {
                                viewModel.selectTrack(track.trackName ?: "", track.artistName ?: "", userStats.apiPreference, "download")
                            }) {
                                Icon(Icons.Rounded.Download, contentDescription = "Download", tint = Color.White.copy(alpha = 0.6f))
                            }

                        }
                    }
                }
                }
            } else if (sState is com.example.viewmodel.SearchState.Error) {
                Box(modifier = Modifier.fillMaxSize(), contentAlignment = Alignment.Center) {
                    Text(sState.message, color = MaterialTheme.colorScheme.error)
                }
            } else if (sState is com.example.viewmodel.SearchState.Idle) {
                Box(modifier = Modifier.fillMaxSize(), contentAlignment = Alignment.Center) {
                    Column(horizontalAlignment = Alignment.CenterHorizontally, modifier = Modifier.padding(32.dp)) {
                        Icon(
                            Icons.Rounded.Search, 
                            contentDescription = null, 
                            modifier = Modifier.size(80.dp), 
                            tint = Color.White.copy(alpha = 0.2f)
                        )
                        Spacer(modifier = Modifier.height(24.dp))
                        Text(
                            "Busca tus canciones favoritas", 
                            color = Color.White.copy(alpha = 0.6f),
                            style = MaterialTheme.typography.titleMedium,
                            textAlign = TextAlign.Center
                        )
                        Spacer(modifier = Modifier.height(8.dp))
                        Text(
                            "Escribe el nombre de un artista, canción o pódcast para empezar a escuchar en Alya Core.", 
                            color = Color.White.copy(alpha = 0.4f),
                            style = MaterialTheme.typography.bodyMedium,
                            textAlign = TextAlign.Center
                        )
                    }
                }
            }

            // Overlay for Download/Play Loading or Error
            if (dlState is com.example.viewmodel.DownloadState.Loading || sState is com.example.viewmodel.SearchState.Loading) {
                val loadingQuote = remember(dlState, sState) {
                    listOf(
                        "Alya Core hizo posible esta aplicación gracias a su API de Gran velocidad.",
                        "Sabias que está aplicación fue una idea que de la nada se me ocurrió mientras veía una silla",
                        "La aplicación demoró 5 días en armarse, no esperaba la verdad demasiado."
                    ).random()
                }
                Box(
                    modifier = Modifier
                        .fillMaxSize()
                        .background(Color.Black.copy(alpha = 0.6f)),
                    contentAlignment = Alignment.Center
                ) {
                    Column(
                        horizontalAlignment = Alignment.CenterHorizontally,
                        modifier = Modifier
                            .padding(32.dp)
                            .clip(RoundedCornerShape(16.dp))
                            .background(MaterialTheme.colorScheme.surface.copy(alpha = 0.9f))
                            .padding(24.dp)
                    ) {
                        CircularProgressIndicator(color = dominantColor ?: MaterialTheme.colorScheme.primary)
                        Spacer(modifier = Modifier.height(24.dp))
                        Text(
                            text = loadingQuote,
                            color = MaterialTheme.colorScheme.onSurface,
                            textAlign = TextAlign.Center,
                            style = MaterialTheme.typography.bodyLarge
                        )
                        Spacer(modifier = Modifier.height(16.dp))
                        TextButton(onClick = { viewModel.resetState() }) {
                            Text("Cancelar", color = MaterialTheme.colorScheme.error)
                        }
                    }
                }
            } else if (dlState is com.example.viewmodel.DownloadState.Error) {
                Box(
                    modifier = Modifier
                        .fillMaxSize()
                        .background(Color.Black.copy(alpha = 0.3f))
                        .clickable { viewModel.resetState() }, // Click to dismiss
                    contentAlignment = Alignment.Center
                ) {
                    Card(modifier = Modifier.padding(16.dp), colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.errorContainer)) {
                        Text(dlState.message, color = MaterialTheme.colorScheme.onErrorContainer, modifier = Modifier.padding(16.dp))
                    }
                }
            }
        }
    }


}