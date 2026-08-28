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

import com.example.ui.screens.MainScreen
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
                    color = Color(0xFF121212)
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

