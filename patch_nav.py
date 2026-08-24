import re

with open("app/src/main/java/com/example/MainActivity.kt", "r") as f:
    content = f.read()

nav_target = """                                        NavigationBar(
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
                                                icon = { Icon(Icons.Rounded.LibraryMusic, contentDescription = "Local") },
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
                                        }"""

nav_replacement = """                                        NavigationBar(
                                            containerColor = Color.Transparent,
                                            contentColor = Color.White
                                        ) {
                                            NavigationBarItem(
                                                icon = { Icon(Icons.Rounded.Search, contentDescription = "Buscar", modifier = Modifier.size(28.dp)) },
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
                                            NavigationBarItem(
                                                icon = { Icon(Icons.Rounded.LibraryMusic, contentDescription = "Tu biblioteca", modifier = Modifier.size(28.dp)) },
                                                label = { Text("Tu biblioteca", style = MaterialTheme.typography.labelSmall) },
                                                selected = selectedTab == 1,
                                                onClick = { 
                                                    selectedTab = 1
                                                    checkAndRequestPermissions()
                                                },
                                                colors = NavigationBarItemDefaults.colors(
                                                    indicatorColor = Color.Transparent,
                                                    selectedIconColor = Color.White,
                                                    selectedTextColor = Color.White,
                                                    unselectedIconColor = Color.White.copy(alpha = 0.5f),
                                                    unselectedTextColor = Color.White.copy(alpha = 0.5f)
                                                )
                                            )
                                            NavigationBarItem(
                                                icon = { Icon(Icons.Rounded.Person, contentDescription = "Perfil", modifier = Modifier.size(28.dp)) },
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
                                        }"""

content = content.replace(nav_target, nav_replacement)

# Also let's fix the background container color to be dark like Spotify.
bg_target = """                Surface(
                    modifier = Modifier.fillMaxSize(),
                    color = MaterialTheme.colorScheme.background
                )"""

bg_replacement = """                Surface(
                    modifier = Modifier.fillMaxSize(),
                    color = Color.Black
                )"""

content = content.replace(bg_target, bg_replacement)

with open("app/src/main/java/com/example/MainActivity.kt", "w") as f:
    f.write(content)
