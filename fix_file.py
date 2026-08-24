import re

with open("app/src/main/java/com/example/MainActivity.kt", "r") as f:
    lines = f.readlines()

# The file has a syntax error because I injected things wrongly.
# Let's just fix the whole structure of onCreate.

# Let's find "fun onCreate"
start_idx = 0
for i, l in enumerate(lines):
    if "override fun onCreate" in l:
        start_idx = i
        break

# Let's find "override fun onStart"
end_idx = 0
for i, l in enumerate(lines):
    if "override fun onStart" in l:
        end_idx = i
        break

on_create_content = "".join(lines[start_idx:end_idx])

# We need to find where the Scaffold is in on_create_content
# and fix the braces. Actually, I can just replace the whole onCreate with a clean version.

clean_on_create = """    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        setContent {
            val userStats by profileViewModel.userStats.collectAsStateWithLifecycle()
            var dominantColor by remember { mutableStateOf<Color?>(null) }
            var showFullScreenPlayer by remember { mutableStateOf(false) }

            val activeColor = if (userStats.extractAlbumColor && dominantColor != null) {
                dominantColor!!
            } else {
                try { Color(android.graphics.Color.parseColor(userStats.primaryColorHex)) } catch(e: Exception) { Color(0xFF00FFFF) }
            }

            MyApplicationTheme(
                primaryColorHex = userStats.primaryColorHex,
                fontPref = userStats.fontPreference,
                dynamicColor = false
            ) {
                Surface(
                    modifier = Modifier.fillMaxSize(),
                    color = MaterialTheme.colorScheme.background
                ) {
                    var selectedTab by remember { mutableStateOf(0) }
                    var showEqualizer by remember { mutableStateOf(false) }

                    Box(modifier = Modifier.fillMaxSize()) {
                        Scaffold(
                            bottomBar = {
                                Column {
                                    MiniPlayer(
                                        controller = mediaController,
                                        dominantColor = activeColor,
                                        onExpand = {
                                            val title = mediaController?.currentMediaItem?.mediaMetadata?.title?.toString()
                                            val artist = mediaController?.currentMediaItem?.mediaMetadata?.artist?.toString()
                                            if (!title.isNullOrBlank()) {
                                                viewModel.fetchLyrics(title, artist ?: "")
                                            }
                                            showFullScreenPlayer = true
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
                                            dominantColor = activeColor,
                                            onOpenEqualizer = { showEqualizer = true }
                                        )
                                    }
                                }
                            }
                        }
                        
                        if (showFullScreenPlayer) {
                            val lyricsState by viewModel.lyricsState.collectAsStateWithLifecycle()
                            FullScreenPlayer(
                                controller = mediaController,
                                dominantColor = activeColor,
                                lyrics = lyricsState ?: "Loading...",
                                onClose = { showFullScreenPlayer = false }
                            )
                        }

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
"""

with open("app/src/main/java/com/example/MainActivity.kt", "w") as f:
    f.writelines(lines[:start_idx])
    f.write(clean_on_create + "\n")
    f.writelines(lines[end_idx:])
