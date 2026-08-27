with open("app/src/main/java/com/example/MainActivity.kt", "r") as f:
    content = f.read()

target = """            if (sState is com.example.viewmodel.SearchState.Success) {
                LazyVerticalGrid(
                    columns = GridCells.Adaptive(minSize = 350.dp),
                    modifier = Modifier.fillMaxSize(),
                    contentPadding = PaddingValues(bottom = 100.dp)
                ) {
                    items(sState.results.size) { index ->"""

replacement = """            if (sState is com.example.viewmodel.SearchState.Success) {
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
                    items(sState.results.size) { index ->"""

content = content.replace(target, replacement)

# We need to find where the LazyVerticalGrid ends and add the closing brace for `else`
# Let's just find `SearchState.Error`

target2 = """                        }
                    }
                }
            } else if (sState is com.example.viewmodel.SearchState.Error) {"""

replacement2 = """                        }
                    }
                }
                }
            } else if (sState is com.example.viewmodel.SearchState.Error) {"""

content = content.replace(target2, replacement2)

with open("app/src/main/java/com/example/MainActivity.kt", "w") as f:
    f.write(content)
