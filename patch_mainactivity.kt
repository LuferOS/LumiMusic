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
