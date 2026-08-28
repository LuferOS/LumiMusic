package com.example.ui.screens

import com.example.viewmodel.MainViewModel
import com.example.viewmodel.ProfileViewModel
import com.example.ui.components.MiniPlayer
import com.example.ui.components.FullScreenPlayer
import com.example.ui.components.LyricsBottomSheet
import com.example.ui.components.AudioSettingsBottomSheet

import android.content.ComponentName
import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import androidx.activity.viewModels
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.clickable
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.rounded.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import com.example.utils.bouncyClick
import androidx.compose.foundation.basicMarquee
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import androidx.compose.ui.viewinterop.AndroidView
import androidx.core.graphics.drawable.toBitmap
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import androidx.media3.common.MediaItem
import androidx.media3.common.Player
import androidx.media3.session.MediaController
import androidx.media3.session.SessionToken
import androidx.media3.ui.PlayerView
import androidx.palette.graphics.Palette
import coil.compose.AsyncImage
import coil.request.ImageRequest
import com.example.data.Downloader
import com.example.player.PlaybackService
import com.example.ui.theme.MyApplicationTheme
import com.example.utils.Utils
import com.example.viewmodel.DownloadState
import androidx.compose.animation.togetherWith
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.grid.LazyVerticalGrid
import androidx.compose.foundation.lazy.grid.GridCells
import androidx.compose.foundation.lazy.grid.items
@Composable
fun MainScreen(
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
        } else if (state is com.example.viewmodel.DownloadState.Append) {
            val mediaItem = androidx.media3.common.MediaItem.Builder()
                .setUri(state.url)
                .setMediaMetadata(
                    androidx.media3.common.MediaMetadata.Builder()
                        .setTitle(state.title)
                        .setArtist(state.title)
                        .build()
                ).build()
            controller?.addMediaItem(mediaItem)
            viewModel.resetState()
        }
    }

    Column(modifier = Modifier.fillMaxSize()) {
        // Search Header
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
                    .clip(RoundedCornerShape(32.dp)),
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
        }

        Box(modifier = Modifier.weight(1f)) {
            val sState = searchState
            val dlState = downloadState

            if (sState is com.example.viewmodel.SearchState.Success) {
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
                    items(sState.results.size) { index ->
                        val track = sState.results[index]
                        Row(
                            modifier = Modifier
                                .fillMaxWidth()
                                .padding(horizontal = 8.dp, vertical = 2.dp)
                                .clip(RoundedCornerShape(12.dp))
                                .clickable { viewModel.playFromRemotePlaylist(sState.results, index, userStats.apiPreference) }
                                .padding(horizontal = 8.dp, vertical = 8.dp),
                            verticalAlignment = Alignment.CenterVertically
                        ) {
                            coil.compose.AsyncImage(
                                model = track.artworkUrl100,
                                contentDescription = null,
                                modifier = Modifier
                                    .size(64.dp)
                                    .clip(RoundedCornerShape(12.dp))
                            )
                            Spacer(modifier = Modifier.width(16.dp))
                            Column(modifier = Modifier.weight(1f)) {
                                Text(text = track.trackName ?: "Unknown", color = Color.White, style = MaterialTheme.typography.bodyLarge, fontWeight = FontWeight.Normal, maxLines = 1, modifier = Modifier.basicMarquee())
                                Spacer(modifier = Modifier.height(2.dp))
                                Text(text = "Canción • ${track.artistName ?: "Unknown"}", style = MaterialTheme.typography.bodyMedium, color = Color.White.copy(alpha = 0.5f), maxLines = 1, modifier = Modifier.basicMarquee())
                            }
                            IconButton(onClick = {
                                viewModel.selectTrack(track.trackName ?: "", track.artistName ?: "", userStats.apiPreference, "download")
                            }) {
                                Icon(Icons.Rounded.Download, contentDescription = "Download", tint = Color.White.copy(alpha = 0.5f))
                            }

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
                    Column(horizontalAlignment = Alignment.CenterHorizontally, modifier = Modifier.padding(32.dp)) {
                        Icon(
                            Icons.Rounded.Search, 
                            contentDescription = null, 
                            modifier = Modifier.size(80.dp), 
                            tint = Color.White.copy(alpha = 0.2f)
                        )
                        Spacer(modifier = Modifier.height(24.dp))
                        Text(
                            "Busca tus canciones favoritas", 
                            color = Color.White.copy(alpha = 0.5f),
                            style = MaterialTheme.typography.titleMedium,
                            textAlign = TextAlign.Center
                        )
                        Spacer(modifier = Modifier.height(8.dp))
                        Text(
                            "Escribe el nombre de un artista, canción o pódcast para empezar a escuchar en Alya Core.", 
                            color = Color.White.copy(alpha = 0.4f),
                            style = MaterialTheme.typography.bodyMedium,
                            textAlign = TextAlign.Center
                        )
                    }
                }
            }

            // Overlay for Download/Play Loading or Error
            if (dlState is com.example.viewmodel.DownloadState.Loading || sState is com.example.viewmodel.SearchState.Loading) {
                val loadingQuote = remember(dlState, sState) {
                    listOf(
                        "Sintonizando frecuencias...",
                        "Buscando en la inmensidad musical...",
                        "Preparando el escenario para ti...",
                        "Conectando con Alya Core..."
                    ).random()
                }
                Box(
                    modifier = Modifier
                        .fillMaxSize()
                        .background(Color.Black.copy(alpha = 0.6f)),
                    contentAlignment = Alignment.Center
                ) {
                    Column(
                        horizontalAlignment = Alignment.CenterHorizontally,
                        modifier = Modifier
                            .padding(32.dp)
                            .clip(RoundedCornerShape(16.dp))
                            .background(MaterialTheme.colorScheme.surface.copy(alpha = 0.9f))
                            .padding(24.dp)
                    ) {
                        CircularProgressIndicator(color = dominantColor ?: MaterialTheme.colorScheme.primary)
                        Spacer(modifier = Modifier.height(24.dp))
                        Text(
                            text = loadingQuote,
                            color = MaterialTheme.colorScheme.onSurface,
                            textAlign = TextAlign.Center,
                            style = MaterialTheme.typography.bodyLarge
                        )
                        Spacer(modifier = Modifier.height(16.dp))
                        TextButton(onClick = { viewModel.resetState() }) {
                            Text("Cancelar", color = MaterialTheme.colorScheme.error)
                        }
                    }
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