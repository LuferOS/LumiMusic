import re

with open("app/src/main/java/com/example/ui/components/FullScreenPlayer.kt", "r") as f:
    content = f.read()

target = """                IconButton(onClick = { /* Like */ }) {
                    Icon(Icons.Rounded.CheckCircle, contentDescription = "Liked", tint = Color(0xFF1DB954), modifier = Modifier.size(32.dp))
                }"""

replacement = """                val currentUri = controller?.currentMediaItem?.localConfiguration?.uri?.toString() ?: ""
                val isLiked by viewModel.isLiked(currentUri).collectAsStateWithLifecycle(initialValue = false)
                IconButton(onClick = { 
                    viewModel.toggleLike(currentUri, currentTitle, currentArtist, artworkUri?.toString())
                }) {
                    Icon(
                        imageVector = if (isLiked) Icons.Rounded.Favorite else Icons.Rounded.FavoriteBorder, 
                        contentDescription = "Like", 
                        tint = if (isLiked) Color(0xFF1DB954) else Color.White, 
                        modifier = Modifier.size(32.dp)
                    )
                }"""

content = content.replace(target, replacement)

with open("app/src/main/java/com/example/ui/components/FullScreenPlayer.kt", "w") as f:
    f.write(content)
