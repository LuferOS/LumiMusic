import re

with open("app/src/main/java/com/example/MainActivity.kt", "r") as f:
    content = f.read()

target = """                                        NavigationBar(
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

replacement = """                                        NavigationBar(
                                            containerColor = Color.Transparent,
                                            contentColor = Color.White
                                        ) {
                                            val orderIndices = userStats.navOrder.split(",").mapNotNull { it.toIntOrNull() }
                                            val validIndices = if (orderIndices.size == 3 && orderIndices.containsAll(listOf(0,1,2))) orderIndices else listOf(0,1,2)
                                            
                                            validIndices.forEach { tabIndex ->
                                                when (tabIndex) {
                                                    0 -> NavigationBarItem(
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
                                                    1 -> NavigationBarItem(
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
                                                    2 -> NavigationBarItem(
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
                                                }
                                            }
                                        }"""
                                        
content = content.replace(target, replacement)
with open("app/src/main/java/com/example/MainActivity.kt", "w") as f:
    f.write(content)
