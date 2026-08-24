package com.example.ui.screens
import com.example.viewmodel.MainViewModel

import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.background
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.rounded.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import androidx.media3.session.MediaController
import com.example.viewmodel.LocalMusicViewModel
import com.example.viewmodel.SortOrder
import androidx.compose.foundation.horizontalScroll
import androidx.compose.foundation.rememberScrollState
import androidx.compose.ui.platform.LocalContext


@OptIn(androidx.compose.material3.ExperimentalMaterial3Api::class)
@Composable
fun LocalMusicScreen(
    viewModel: LocalMusicViewModel,
    mainViewModel: MainViewModel,
    controller: MediaController?,
    dominantColor: Color?
) {
    val likedSongs by mainViewModel.likedTracks.collectAsStateWithLifecycle()
    val musicList by viewModel.localMusicList.collectAsStateWithLifecycle()
    val currentSort by viewModel.currentSortOrder.collectAsStateWithLifecycle()
    var isSearchExpanded by remember { mutableStateOf(false) }
    var searchQuery by remember { mutableStateOf("") }
    val context = LocalContext.current

    val filteredList = if (searchQuery.isBlank()) {
        musicList
    } else {
        musicList.filter { it.title.contains(searchQuery, ignoreCase = true) || it.artist.contains(searchQuery, ignoreCase = true) }
    }

    Column(modifier = Modifier.fillMaxSize().background(Color.Black)) {
        // Header
        Row(
            modifier = Modifier
                .fillMaxWidth()
                .padding(horizontal = 16.dp, vertical = 16.dp),
            verticalAlignment = Alignment.CenterVertically
        ) {
            Box(
                modifier = Modifier
                    .size(36.dp)
                    .clip(CircleShape)
                    .background(Color(0xFFFF5722)),
                contentAlignment = Alignment.Center
            ) {
                Text("L", color = Color.White, fontWeight = FontWeight.Bold) // Placeholder for profile initial
            }
            Spacer(modifier = Modifier.width(16.dp))
            Text(
                text = "Tu biblioteca",
                style = MaterialTheme.typography.titleLarge,
                fontWeight = FontWeight.Bold,
                color = Color.White,
                modifier = Modifier.weight(1f)
            )
            IconButton(onClick = { isSearchExpanded = !isSearchExpanded }) {
                Icon(Icons.Rounded.Search, contentDescription = "Search", tint = Color.White)
            }

        }
        
        if (isSearchExpanded) {
            TextField(
                value = searchQuery,
                onValueChange = { searchQuery = it },
                placeholder = { Text("Buscar en descargas...", color = Color.White.copy(alpha=0.5f)) },
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(horizontal = 16.dp, vertical = 8.dp)
                    .clip(RoundedCornerShape(8.dp)),
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

        // Filters (Playlists, Albums, Artists, Downloaded)
        Row(
            modifier = Modifier
                .fillMaxWidth()
                .horizontalScroll(rememberScrollState())
                .padding(horizontal = 16.dp, vertical = 8.dp),
            horizontalArrangement = Arrangement.spacedBy(8.dp)
        ) {
            val chips = listOf("Descargado", "Canciones", "Álbumes", "Artistas")
            chips.forEach { chip ->
                Box(
                    modifier = Modifier
                        .clip(RoundedCornerShape(24.dp))
                        .background(if (chip == "Descargado") Color(0xFF1DB954) else Color(0xFF2A2A2A))
                        .padding(horizontal = 16.dp, vertical = 8.dp)
                ) {
                    Text(chip, color = if (chip == "Descargado") Color.Black else Color.White, style = MaterialTheme.typography.bodyMedium)
                }
            }
        }

        // Sub-header (Recientes, Grid toggle)
        Row(
            modifier = Modifier
                .fillMaxWidth()
                .padding(horizontal = 16.dp, vertical = 12.dp),
            verticalAlignment = Alignment.CenterVertically
        ) {
            Icon(Icons.Rounded.SwapVert, contentDescription = "Sort", tint = Color.White, modifier = Modifier.size(20.dp))
            Spacer(modifier = Modifier.width(8.dp))
            Text("Recientes", color = Color.White, style = MaterialTheme.typography.bodyMedium)
            Spacer(modifier = Modifier.weight(1f))
            Icon(Icons.Rounded.GridView, contentDescription = "Grid", tint = Color.White, modifier = Modifier.size(20.dp))
        }

        var showingLiked by remember { mutableStateOf(false) }
        LazyColumn(
            modifier = Modifier.fillMaxSize(),
            contentPadding = PaddingValues(bottom = 100.dp) // Space for MiniPlayer
        ) {
            // First item: Liked Songs
            
            item {
                Row(
                    modifier = Modifier
                        .fillMaxWidth()
                        .clickable { showingLiked = !showingLiked }
                        .padding(horizontal = 16.dp, vertical = 8.dp),
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    Box(
                        modifier = Modifier
                            .size(64.dp)
                            .clip(RoundedCornerShape(4.dp))
                            .background(Color(0xFF5353CE)),
                        contentAlignment = Alignment.Center
                    ) {
                        Icon(Icons.Rounded.Favorite, contentDescription = null, tint = Color.White)
                    }
                    Spacer(modifier = Modifier.width(16.dp))
                    Column(modifier = Modifier.weight(1f)) {
                        Text("Tus me gusta", color = Color.White, style = MaterialTheme.typography.bodyLarge, fontWeight = FontWeight.Normal)
                        Spacer(modifier = Modifier.height(2.dp))
                        Row(verticalAlignment = Alignment.CenterVertically) {
                            Icon(Icons.Rounded.PushPin, contentDescription = null, tint = Color(0xFF1DB954), modifier = Modifier.size(12.dp))
                            Spacer(modifier = Modifier.width(4.dp))
                            Text("Playlist • ${likedSongs.size} canciones", style = MaterialTheme.typography.bodyMedium, color = Color.White.copy(alpha = 0.6f))
                        }
                    }
                }
            }

            if (showingLiked) {
                items(likedSongs) { track ->
                    Row(
                        modifier = Modifier
                            .fillMaxWidth()
                            .clickable {
                                val index = likedSongs.indexOf(track)
                                if (index != -1 && controller != null) {
                                    val mediaItems = likedSongs.map { t ->
                                        androidx.media3.common.MediaItem.Builder()
                                            .setUri(t.uri)
                                            .setMediaMetadata(
                                                androidx.media3.common.MediaMetadata.Builder()
                                                    .setTitle(t.title)
                                                    .setArtist(t.artist)
                                                    .build()
                                            )
                                            .build()
                                    }
                                    controller.setMediaItems(mediaItems)
                                    controller.seekToDefaultPosition(index)
                                    controller.prepare()
                                    controller.play()
                                }
                            }
                            .padding(horizontal = 16.dp, vertical = 8.dp),
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        coil.compose.AsyncImage(
                            model = track.artworkUrl,
                            contentDescription = null,
                            modifier = Modifier
                                .size(64.dp)
                                .clip(RoundedCornerShape(4.dp))
                                .background(Color(0xFF2A2A2A))
                        )
                        Spacer(modifier = Modifier.width(16.dp))
                        Column(modifier = Modifier.weight(1f)) {
                            Text(track.title, color = Color.White, style = MaterialTheme.typography.bodyLarge, maxLines = 1, overflow = TextOverflow.Ellipsis)
                            Spacer(modifier = Modifier.height(2.dp))
                            Text("Favorito • ${track.artist}", style = MaterialTheme.typography.bodyMedium, color = Color.White.copy(alpha = 0.6f), maxLines = 1, overflow = TextOverflow.Ellipsis)
                        }
                    }
                }
            } else {
            items(filteredList) { audio ->
                Row(
                    modifier = Modifier
                        .fillMaxWidth()
                        .clickable {
                            val index = filteredList.indexOf(audio)
                            if (index != -1 && controller != null) {
                                val mediaItems = filteredList.map { track ->
                                    androidx.media3.common.MediaItem.Builder()
                                        .setUri(track.uri)
                                        .setMediaMetadata(
                                            androidx.media3.common.MediaMetadata.Builder()
                                                .setTitle(track.title)
                                                .setArtist(track.artist)
                                                .build()
                                        )
                                        .build()
                                }
                                controller.setMediaItems(mediaItems)
                                controller.seekToDefaultPosition(index)
                                controller.prepare()
                                controller.play()
                            }
                        }
                        .padding(horizontal = 16.dp, vertical = 8.dp),
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    Box(
                        modifier = Modifier
                            .size(64.dp)
                            .clip(RoundedCornerShape(4.dp))
                            .background(Color(0xFF2A2A2A)),
                        contentAlignment = Alignment.Center
                    ) {
                        Icon(Icons.Rounded.AudioFile, contentDescription = null, tint = Color.White.copy(alpha=0.5f))
                    }
                    Spacer(modifier = Modifier.width(16.dp))
                    Column(modifier = Modifier.weight(1f)) {
                        Text(audio.title, color = Color.White, style = MaterialTheme.typography.bodyLarge, maxLines = 1, overflow = TextOverflow.Ellipsis)
                        Spacer(modifier = Modifier.height(2.dp))
                        Text("Descargado • ${audio.artist}", style = MaterialTheme.typography.bodyMedium, color = Color.White.copy(alpha = 0.6f), maxLines = 1, overflow = TextOverflow.Ellipsis)
                    }
                }
            }
            }
        }
    }
}