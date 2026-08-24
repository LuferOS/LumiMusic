import re

with open("app/src/main/java/com/example/MainActivity.kt", "r") as f:
    content = f.read()

# We need to find MainScreen and rewrite the state rendering logic.
# Because the current one is an `if-else` chain that hides things.

# First, let's extract the MainScreen function content.
start_idx = content.find("fun MainScreen(")
end_idx = content.find("override fun onStart() {", start_idx)

mainscreen_content = content[start_idx:end_idx]

# I will write a completely new MainScreen implementation that solves the user's issues.

new_mainscreen = """fun MainScreen(
    viewModel: MainViewModel,
    profileViewModel: ProfileViewModel,
    controller: MediaController?,
    onColorExtracted: (Color) -> Unit,
    dominantColor: Color?
) {
    var urlInput by remember { mutableStateOf("") }
    val downloadState by viewModel.downloadState.collectAsStateWithLifecycle()
    val searchState by viewModel.searchState.collectAsStateWithLifecycle()
    val context = LocalContext.current
    val userStats by profileViewModel.userStats.collectAsStateWithLifecycle()

    LaunchedEffect(downloadState) {
        val state = downloadState
        if (state is com.example.viewmodel.DownloadState.Success) {
            if (state.action == "play") {
                val mediaItem = androidx.media3.common.MediaItem.Builder()
                    .setUri(state.url)
                    .setMediaMetadata(
                        androidx.media3.common.MediaMetadata.Builder()
                            .setTitle(state.title)
                            .setArtist(state.title) // Fallback if artist not fully parsed
                            .build()
                    ).build()
                controller?.setMediaItem(mediaItem)
                controller?.prepare()
                controller?.play()
                
                // Extract color if needed
                if (state.thumbnail != null) {
                    val request = coil.request.ImageRequest.Builder(context)
                        .data(state.thumbnail)
                        .allowHardware(false)
                        .build()
                    val result = coil.ImageLoader(context).execute(request)
                    if (result is coil.request.SuccessResult) {
                        val bitmap = (result.drawable as? android.graphics.drawable.BitmapDrawable)?.bitmap
                        if (bitmap != null) {
                            androidx.palette.graphics.Palette.from(bitmap).generate { palette ->
                                palette?.dominantSwatch?.rgb?.let { colorInt ->
                                    onColorExtracted(Color(colorInt))
                                }
                            }
                        }
                    }
                }
            } else if (state.action == "download") {
                com.example.data.Downloader.downloadMp3(context, state.url, state.title)
                profileViewModel.recordDownload()
            }
            viewModel.resetState() // Go back to idle to hide loading
        }
    }

    Column(modifier = Modifier.fillMaxSize()) {
        Row(
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
        }

        Box(modifier = Modifier.weight(1f)) {
            val sState = searchState
            val dlState = downloadState

            if (sState is com.example.viewmodel.SearchState.Success) {
                LazyColumn(
                    modifier = Modifier.fillMaxSize(),
                    contentPadding = PaddingValues(bottom = 100.dp)
                ) {
                    items(sState.results) { track ->
                        Card(
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
                        }
                    }
                }
            } else if (sState is com.example.viewmodel.SearchState.Error) {
                Box(modifier = Modifier.fillMaxSize(), contentAlignment = Alignment.Center) {
                    Text(sState.message, color = MaterialTheme.colorScheme.error)
                }
            } else if (sState is com.example.viewmodel.SearchState.Idle) {
                Box(modifier = Modifier.fillMaxSize(), contentAlignment = Alignment.Center) {
                    Column(horizontalAlignment = Alignment.CenterHorizontally) {
                        Icon(Icons.Rounded.Search, contentDescription = null, modifier = Modifier.size(64.dp), tint = MaterialTheme.colorScheme.onSurfaceVariant.copy(alpha = 0.5f))
                        Spacer(modifier = Modifier.height(16.dp))
                        Text("Search for your favorite tracks", color = MaterialTheme.colorScheme.onSurfaceVariant.copy(alpha = 0.5f))
                    }
                }
            }

            // Overlay for Download/Play Loading or Error
            if (dlState is com.example.viewmodel.DownloadState.Loading || sState is com.example.viewmodel.SearchState.Loading) {
                Box(
                    modifier = Modifier
                        .fillMaxSize()
                        .background(Color.Black.copy(alpha = 0.3f)),
                    contentAlignment = Alignment.Center
                ) {
                    CircularProgressIndicator(color = dominantColor ?: MaterialTheme.colorScheme.primary)
                }
            } else if (dlState is com.example.viewmodel.DownloadState.Error) {
                Box(
                    modifier = Modifier
                        .fillMaxSize()
                        .background(Color.Black.copy(alpha = 0.3f))
                        .clickable { viewModel.resetState() }, // Click to dismiss
                    contentAlignment = Alignment.Center
                ) {
                    Card(modifier = Modifier.padding(16.dp), colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.errorContainer)) {
                        Text(dlState.message, color = MaterialTheme.colorScheme.onErrorContainer, modifier = Modifier.padding(16.dp))
                    }
                }
            }
        }
    }
}
"""

content = content.replace(mainscreen_content, new_mainscreen)

with open("app/src/main/java/com/example/MainActivity.kt", "w") as f:
    f.write(content)
