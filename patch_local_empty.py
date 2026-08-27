with open("app/src/main/java/com/example/ui/screens/LocalMusicScreen.kt", "r") as f:
    content = f.read()

target = """            if (showingLiked) {
                items(likedSongs) { track ->"""

replacement = """            if (showingLiked) {
                if (likedSongs.isEmpty()) {
                    item {
                        Column(
                            modifier = Modifier.fillMaxWidth().padding(32.dp),
                            horizontalAlignment = Alignment.CenterHorizontally
                        ) {
                            Icon(Icons.Rounded.FavoriteBorder, contentDescription = null, modifier = Modifier.size(64.dp), tint = Color.White.copy(alpha=0.3f))
                            Spacer(modifier = Modifier.height(16.dp))
                            Text("Aún no tienes favoritos", color = Color.White.copy(alpha=0.5f), style = MaterialTheme.typography.bodyLarge)
                        }
                    }
                }
                items(likedSongs) { track ->"""

content = content.replace(target, replacement)

target2 = """            } else {
            items(filteredList) { audio ->"""

replacement2 = """            } else {
                if (filteredList.isEmpty()) {
                    item {
                        Column(
                            modifier = Modifier.fillMaxWidth().padding(32.dp),
                            horizontalAlignment = Alignment.CenterHorizontally
                        ) {
                            Icon(Icons.Rounded.MusicOff, contentDescription = null, modifier = Modifier.size(64.dp), tint = Color.White.copy(alpha=0.3f))
                            Spacer(modifier = Modifier.height(16.dp))
                            Text("No se encontró música", color = Color.White.copy(alpha=0.5f), style = MaterialTheme.typography.bodyLarge)
                        }
                    }
                }
                items(filteredList) { audio ->"""

content = content.replace(target2, replacement2)

with open("app/src/main/java/com/example/ui/screens/LocalMusicScreen.kt", "w") as f:
    f.write(content)
