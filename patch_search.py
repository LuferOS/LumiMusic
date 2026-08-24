import re

with open("app/src/main/java/com/example/MainActivity.kt", "r") as f:
    content = f.read()

search_bar_target = """        Row(
            modifier = Modifier
                .fillMaxWidth()
                .padding(16.dp),
            verticalAlignment = Alignment.CenterVertically
        ) {
            OutlinedTextField(
                value = urlInput,
                onValueChange = { urlInput = it },
                label = { Text("Search YouTube / Spotify") },
                modifier = Modifier.weight(1f),
                shape = RoundedCornerShape(24.dp),
                singleLine = true,
                colors = OutlinedTextFieldDefaults.colors(
                    focusedBorderColor = dominantColor ?: MaterialTheme.colorScheme.primary,
                    focusedLabelColor = dominantColor ?: MaterialTheme.colorScheme.primary
                )
            )
            Spacer(modifier = Modifier.width(8.dp))
            FloatingActionButton(
                onClick = {
                    viewModel.searchITunes(urlInput)
                },
                shape = RoundedCornerShape(24.dp),
                containerColor = dominantColor ?: MaterialTheme.colorScheme.primaryContainer
            ) {
                Icon(Icons.Rounded.Search, contentDescription = "Search")
            }
        }"""

search_bar_replacement = """        // Search Header
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
        }"""

content = content.replace(search_bar_target, search_bar_replacement)

results_target = """                        Card(
                            modifier = Modifier
                                .fillMaxWidth()
                                .padding(horizontal = 16.dp, vertical = 4.dp),
                            shape = RoundedCornerShape(16.dp),
                            colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surfaceVariant),
                            onClick = {
                                viewModel.selectTrack(track.trackName ?: "", track.artistName ?: "", userStats.apiPreference, "play")
                            }
                        ) {
                            Row(
                                modifier = Modifier.padding(12.dp),
                                verticalAlignment = Alignment.CenterVertically
                            ) {
                                coil.compose.AsyncImage(
                                    model = track.artworkUrl100,
                                    contentDescription = null,
                                    modifier = Modifier
                                        .size(56.dp)
                                        .clip(RoundedCornerShape(8.dp))
                                )
                                Spacer(modifier = Modifier.width(16.dp))
                                Column(modifier = Modifier.weight(1f)) {
                                    Text(text = track.trackName ?: "Unknown", fontWeight = FontWeight.Bold, maxLines = 1)
                                    Text(text = track.artistName ?: "Unknown", style = MaterialTheme.typography.bodyMedium, color = MaterialTheme.colorScheme.onSurfaceVariant, maxLines = 1)
                                }
                                IconButton(onClick = {
                                    viewModel.selectTrack(track.trackName ?: "", track.artistName ?: "", userStats.apiPreference, "download")
                                }) {
                                    Icon(Icons.Rounded.Download, contentDescription = "Download", tint = MaterialTheme.colorScheme.secondary)
                                }
                                Icon(Icons.Rounded.PlayArrow, contentDescription = "Select", tint = dominantColor ?: MaterialTheme.colorScheme.primary)
                            }
                        }"""

results_replacement = """                        Row(
                            modifier = Modifier
                                .fillMaxWidth()
                                .clickable { viewModel.selectTrack(track.trackName ?: "", track.artistName ?: "", userStats.apiPreference, "play") }
                                .padding(horizontal = 16.dp, vertical = 8.dp),
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
                                Text(text = track.trackName ?: "Unknown", color = Color.White, style = MaterialTheme.typography.bodyLarge, fontWeight = FontWeight.Normal, maxLines = 1, overflow = TextOverflow.Ellipsis)
                                Spacer(modifier = Modifier.height(2.dp))
                                Text(text = "Canción • ${track.artistName ?: "Unknown"}", style = MaterialTheme.typography.bodyMedium, color = Color.White.copy(alpha = 0.6f), maxLines = 1, overflow = TextOverflow.Ellipsis)
                            }
                            IconButton(onClick = {
                                viewModel.selectTrack(track.trackName ?: "", track.artistName ?: "", userStats.apiPreference, "download")
                            }) {
                                Icon(Icons.Rounded.Download, contentDescription = "Download", tint = Color.White.copy(alpha = 0.6f))
                            }
                            IconButton(onClick = { /* More options */ }) {
                                Icon(Icons.Rounded.MoreVert, contentDescription = "More", tint = Color.White.copy(alpha = 0.6f))
                            }
                        }"""

content = content.replace(results_target, results_replacement)

empty_target = """            } else if (sState is com.example.viewmodel.SearchState.Idle) {
                Box(modifier = Modifier.fillMaxSize(), contentAlignment = Alignment.Center) {
                    Column(horizontalAlignment = Alignment.CenterHorizontally) {
                        Icon(Icons.Rounded.Search, contentDescription = null, modifier = Modifier.size(64.dp), tint = MaterialTheme.colorScheme.onSurfaceVariant.copy(alpha = 0.5f))
                        Spacer(modifier = Modifier.height(16.dp))
                        Text("Search for music to play or download", color = MaterialTheme.colorScheme.onSurfaceVariant)
                    }
                }
            }"""

empty_replacement = """            } else if (sState is com.example.viewmodel.SearchState.Idle) {
                Box(modifier = Modifier.fillMaxSize().padding(top = 16.dp)) {
                    Text(
                        text = "Recientes",
                        style = MaterialTheme.typography.titleLarge,
                        fontWeight = FontWeight.Bold,
                        color = Color.White,
                        modifier = Modifier.padding(horizontal = 16.dp)
                    )
                }
            }"""

content = content.replace(empty_target, empty_replacement)

with open("app/src/main/java/com/example/MainActivity.kt", "w") as f:
    f.write(content)
