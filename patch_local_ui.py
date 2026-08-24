import re

with open("app/src/main/java/com/example/ui/screens/LocalMusicScreen.kt", "r") as f:
    content = f.read()

target_imports = """    val musicList by viewModel.localMusicList.collectAsStateWithLifecycle()"""
replacement_imports = """    val likedSongs by mainViewModel.likedTracks.collectAsStateWithLifecycle()
    val musicList by viewModel.localMusicList.collectAsStateWithLifecycle()"""

content = content.replace(target_imports, replacement_imports)

target_liked = """            item {
                Row(
                    modifier = Modifier
                        .fillMaxWidth()
                        .clickable { /* open liked songs */ }
                        .padding(horizontal = 16.dp, vertical = 8.dp),"""
replacement_liked = """            var showingLiked by remember { mutableStateOf(false) }
            
            item {
                Row(
                    modifier = Modifier
                        .fillMaxWidth()
                        .clickable { showingLiked = !showingLiked }
                        .padding(horizontal = 16.dp, vertical = 8.dp),"""
content = content.replace(target_liked, replacement_liked)

target_liked_text = """                            Text("Playlist • Favoritos", style = MaterialTheme.typography.bodyMedium, color = Color.White.copy(alpha = 0.6f))"""
replacement_liked_text = """                            Text("Playlist • ${likedSongs.size} canciones", style = MaterialTheme.typography.bodyMedium, color = Color.White.copy(alpha = 0.6f))"""
content = content.replace(target_liked_text, replacement_liked_text)

target_items = """            items(filteredList) { audio ->
                Row("""
replacement_items = """            if (showingLiked) {
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
                Row("""
content = content.replace(target_items, replacement_items)

# Add closing brace for else block
target_end_items = """                    }
                }
            }
        }
    }
}"""
replacement_end_items = """                    }
                }
            }
            }
        }
    }
}"""
content = content.replace(target_end_items, replacement_end_items)

with open("app/src/main/java/com/example/ui/screens/LocalMusicScreen.kt", "w") as f:
    f.write(content)
