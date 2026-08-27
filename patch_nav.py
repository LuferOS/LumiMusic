with open("app/src/main/java/com/example/MainActivity.kt", "r") as f:
    content = f.read()

import_line = "import com.example.utils.bouncyClick\n"
if "import com.example.utils.bouncyClick" not in content:
    content = content.replace("import com.example.ui.theme.neonGlow\n", "import com.example.ui.theme.neonGlow\nimport com.example.utils.bouncyClick\n")

target = """                                                    0 -> NavigationBarItem(
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
                                                    )"""

replacement = """                                                    0 -> NavigationBarItem(
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
                                                    )"""

if target in content:
    content = content.replace(target, replacement)
else:
    print("Could not find nav items")

with open("app/src/main/java/com/example/MainActivity.kt", "w") as f:
    f.write(content)
