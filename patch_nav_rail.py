with open("app/src/main/java/com/example/MainActivity.kt", "r") as f:
    content = f.read()

target = """                                    NavigationRail(
                                        containerColor = MaterialTheme.colorScheme.background,
                                        contentColor = activeColor
                                    ) {
                                        NavigationRailItem(
                                            icon = { Icon(Icons.Rounded.Search, contentDescription = "Online") },
                                            label = { Text("Online") },
                                            selected = selectedTab == 0,
                                            onClick = { selectedTab = 0 },
                                            colors = NavigationRailItemDefaults.colors(selectedIconColor = activeColor, selectedTextColor = activeColor)
                                        )
                                        NavigationRailItem(
                                            icon = { Icon(Icons.Rounded.LibraryMusic, contentDescription = "Local") },
                                            label = { Text("Local") },
                                            selected = selectedTab == 1,
                                            onClick = { 
                                                selectedTab = 1
                                                checkAndRequestPermissions()
                                            },
                                            colors = NavigationRailItemDefaults.colors(selectedIconColor = activeColor, selectedTextColor = activeColor)
                                        )
                                        NavigationRailItem(
                                            icon = { Icon(Icons.Rounded.Person, contentDescription = "Perfil") },
                                            label = { Text("Perfil") },
                                            selected = selectedTab == 2,
                                            onClick = { selectedTab = 2 },
                                            colors = NavigationRailItemDefaults.colors(selectedIconColor = activeColor, selectedTextColor = activeColor)
                                        )
                                    }"""

replacement = """                                    NavigationRail(
                                        containerColor = MaterialTheme.colorScheme.background,
                                        contentColor = activeColor
                                    ) {
                                        val orderIndices = userStats.navOrder.split(",").mapNotNull { it.toIntOrNull() }
                                        val validIndices = if (orderIndices.size == 3 && orderIndices.containsAll(listOf(0,1,2))) orderIndices else listOf(0,1,2)
                                        
                                        validIndices.forEach { tabIndex ->
                                            when (tabIndex) {
                                                0 -> NavigationRailItem(
                                                    icon = { Icon(Icons.Rounded.Search, contentDescription = "Online") },
                                                    label = { Text("Online") },
                                                    selected = selectedTab == 0,
                                                    onClick = { selectedTab = 0 },
                                                    colors = NavigationRailItemDefaults.colors(selectedIconColor = activeColor, selectedTextColor = activeColor)
                                                )
                                                1 -> NavigationRailItem(
                                                    icon = { Icon(Icons.Rounded.LibraryMusic, contentDescription = "Local") },
                                                    label = { Text("Local") },
                                                    selected = selectedTab == 1,
                                                    onClick = { 
                                                        selectedTab = 1
                                                        checkAndRequestPermissions()
                                                    },
                                                    colors = NavigationRailItemDefaults.colors(selectedIconColor = activeColor, selectedTextColor = activeColor)
                                                )
                                                2 -> NavigationRailItem(
                                                    icon = { Icon(Icons.Rounded.Person, contentDescription = "Perfil") },
                                                    label = { Text("Perfil") },
                                                    selected = selectedTab == 2,
                                                    onClick = { selectedTab = 2 },
                                                    colors = NavigationRailItemDefaults.colors(selectedIconColor = activeColor, selectedTextColor = activeColor)
                                                )
                                            }
                                        }
                                    }"""
content = content.replace(target, replacement)
with open("app/src/main/java/com/example/MainActivity.kt", "w") as f:
    f.write(content)
