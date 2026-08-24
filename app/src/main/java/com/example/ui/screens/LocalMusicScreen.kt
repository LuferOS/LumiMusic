package com.example.ui.screens

import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.background
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
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
import androidx.compose.ui.unit.dp
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import androidx.media3.session.MediaController
import com.example.viewmodel.LocalMusicViewModel
import com.example.viewmodel.SortOrder
import androidx.compose.foundation.horizontalScroll
import androidx.compose.foundation.rememberScrollState
import androidx.compose.ui.platform.LocalContext

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun LocalMusicScreen(
    viewModel: LocalMusicViewModel,
    controller: MediaController?,
    dominantColor: Color?
) {
    val musicList by viewModel.localMusicList.collectAsStateWithLifecycle()
    val currentSort by viewModel.currentSortOrder.collectAsStateWithLifecycle()
    var searchQuery by remember { mutableStateOf("") }
    val context = LocalContext.current

    val filteredList = if (searchQuery.isBlank()) {
        musicList
    } else {
        musicList.filter { it.title.contains(searchQuery, ignoreCase = true) || it.artist.contains(searchQuery, ignoreCase = true) }
    }

    Column(modifier = Modifier.fillMaxSize()) {
        Row(
            modifier = Modifier
                .fillMaxWidth()
                .padding(16.dp),
            verticalAlignment = Alignment.CenterVertically,
            horizontalArrangement = Arrangement.SpaceBetween
        ) {
            Text(
                text = "My Library",
                style = MaterialTheme.typography.headlineMedium,
                fontWeight = FontWeight.Bold
            )
            IconButton(
                onClick = {
                    if (filteredList.isNotEmpty() && controller != null) {
                        val shuffled = filteredList.shuffled()
                        controller.clearMediaItems()
                        shuffled.forEach { audio ->
                            controller.addMediaItem(androidx.media3.common.MediaItem.Builder().setUri(audio.uri).setMediaMetadata(androidx.media3.common.MediaMetadata.Builder().setTitle(audio.title).setArtist(audio.artist).build()).build())
                        }
                        controller.prepare()
                        controller.play()
                    }
                }
            ) {
                Icon(
                    imageVector = Icons.Rounded.Shuffle,
                    contentDescription = "Shuffle All",
                    tint = dominantColor ?: MaterialTheme.colorScheme.primary
                )
            }
        }

        OutlinedTextField(
            value = searchQuery,
            onValueChange = { searchQuery = it },
            placeholder = { Text("Search your downloads...") },
            leadingIcon = { Icon(Icons.Rounded.Search, contentDescription = null) },
            modifier = Modifier
                .fillMaxWidth()
                .padding(horizontal = 16.dp),
            shape = RoundedCornerShape(24.dp),
            singleLine = true
        )

        Row(
            modifier = Modifier
                .fillMaxWidth()
                .horizontalScroll(rememberScrollState())
                .padding(horizontal = 16.dp, vertical = 8.dp),
            horizontalArrangement = Arrangement.spacedBy(8.dp)
        ) {
            FilterChip(
                selected = currentSort == SortOrder.DATE_ADDED,
                onClick = { viewModel.setSortOrder(SortOrder.DATE_ADDED, context) },
                label = { Text("Newest") },
                leadingIcon = if (currentSort == SortOrder.DATE_ADDED) {
                    { Icon(Icons.Rounded.Check, contentDescription = null, modifier = Modifier.size(16.dp)) }
                } else null
            )
            FilterChip(
                selected = currentSort == SortOrder.TITLE,
                onClick = { viewModel.setSortOrder(SortOrder.TITLE, context) },
                label = { Text("A-Z") },
                leadingIcon = if (currentSort == SortOrder.TITLE) {
                    { Icon(Icons.Rounded.Check, contentDescription = null, modifier = Modifier.size(16.dp)) }
                } else null
            )
            FilterChip(
                selected = currentSort == SortOrder.ARTIST,
                onClick = { viewModel.setSortOrder(SortOrder.ARTIST, context) },
                label = { Text("Artist") },
                leadingIcon = if (currentSort == SortOrder.ARTIST) {
                    { Icon(Icons.Rounded.Check, contentDescription = null, modifier = Modifier.size(16.dp)) }
                } else null
            )
        }

        LazyColumn(
            modifier = Modifier.fillMaxSize(),
            contentPadding = PaddingValues(bottom = 100.dp) // Space for MiniPlayer
        ) {
            items(filteredList) { audio ->
                ListItem(
                    headlineContent = { Text(audio.title, maxLines = 1) },
                    supportingContent = { Text(audio.artist, maxLines = 1) },
                    leadingContent = {
                        Box(
                            modifier = Modifier
                                .size(48.dp)
                                .clip(RoundedCornerShape(8.dp))
                                .background(MaterialTheme.colorScheme.surfaceVariant),
                            contentAlignment = Alignment.Center
                        ) {
                            Icon(Icons.Rounded.AudioFile, contentDescription = null)
                        }
                    },
                    modifier = Modifier.clickable {
                        controller?.let {
                            it.clearMediaItems()
                            it.addMediaItem(
                                androidx.media3.common.MediaItem.Builder()
                                    .setUri(audio.uri)
                                    .setMediaMetadata(
                                        androidx.media3.common.MediaMetadata.Builder()
                                            .setTitle(audio.title)
                                            .setArtist(audio.artist)
                                            .build()
                                    )
                                    .build()
                            )
                            it.prepare()
                            it.play()
                        }
                    }
                )
            }
        }
    }
}
