import re

with open("app/src/main/java/com/example/MainActivity.kt", "r") as f:
    content = f.read()

# We need to find the Surface block inside setContent
start_surface = content.find("                Surface(")
end_surface = content.find("                    } // Box end", start_surface) # Wait, it ends with a closing of Surface

start_idx = content.find("var selectedTab by remember { mutableStateOf(0) }")
end_idx = content.find("if (showFullScreenPlayer) {")

if start_idx != -1 and end_idx != -1:
    old_layout = content[start_idx:end_idx]
    
    new_layout = """var selectedTab by remember { mutableStateOf(0) }
                    var showEqualizer by remember { mutableStateOf(false) }

                    BoxWithConstraints(modifier = Modifier.fillMaxSize()) {
                        val isWideScreen = maxWidth >= 600.dp
                        
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
                                    if (!isWideScreen) {
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
                                                icon = { Icon(Icons.AutoMirrored.Rounded.List, contentDescription = "Local") },
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
                                            icon = { Icon(Icons.AutoMirrored.Rounded.List, contentDescription = "Local") },
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
                        }
                        
                        """
    content = content.replace(old_layout, new_layout)
    
    with open("app/src/main/java/com/example/MainActivity.kt", "w") as f:
        f.write(content)
else:
    print("Failed to find boundaries in MainActivity.kt")
