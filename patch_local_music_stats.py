import re
with open("app/src/main/java/com/example/ui/screens/LocalMusicScreen.kt", "r") as f:
    content = f.read()

# Add UserStats import if not present
if "import com.example.data.local.UserStats" not in content:
    content = content.replace("import com.example.viewmodel.MainViewModel", "import com.example.viewmodel.MainViewModel\nimport com.example.data.local.UserStats\nimport com.example.ui.theme.neonGlow")

content = content.replace(
    "controller: MediaController?,\n    dominantColor: Color?\n)",
    "controller: MediaController?,\n    dominantColor: Color?,\n    userStats: UserStats\n)"
)

# Apply neonGlow to LocalMusicScreen list items
target = """            Row(
                modifier = Modifier
                    .fillMaxWidth()
                    .clickable { 
                        mainViewModel.playLocalPlaylist(musicList, index)
                    }
                    .padding(horizontal = 16.dp, vertical = 12.dp),"""

replacement = """            Row(
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(horizontal = 8.dp, vertical = 4.dp)
                    .neonGlow(color = dominantColor ?: Color.White, cornerRadius = 8.dp, enabled = userStats.neonBorders)
                    .clip(RoundedCornerShape(8.dp))
                    .clickable { 
                        mainViewModel.playLocalPlaylist(musicList, index)
                    }
                    .padding(horizontal = 8.dp, vertical = 8.dp),"""
                    
content = content.replace(target, replacement)

# Apply neonGlow to LocalMusicScreen top action buttons (Aleatorio, Liked)
target_buttons = """        Row(modifier = Modifier.fillMaxWidth().padding(horizontal = 16.dp), horizontalArrangement = Arrangement.spacedBy(16.dp)) {
            Button(
                onClick = { mainViewModel.playLocalPlaylist(musicList, 0, shuffle = true) },
                modifier = Modifier.weight(1f),
                colors = ButtonDefaults.buttonColors(containerColor = dominantColor ?: MaterialTheme.colorScheme.primary)
            ) {
                Icon(Icons.Rounded.Shuffle, contentDescription = null)
                Spacer(modifier = Modifier.width(8.dp))
                Text("Aleatorio")
            }
            Button(
                onClick = { mainViewModel.playLikedPlaylist() },
                modifier = Modifier.weight(1f),
                colors = ButtonDefaults.buttonColors(containerColor = Color(0xFFE91E63))
            ) {
                Icon(Icons.Rounded.Favorite, contentDescription = null)
                Spacer(modifier = Modifier.width(8.dp))
                Text("Favoritos")
            }
        }"""
        
replacement_buttons = """        Row(modifier = Modifier.fillMaxWidth().padding(horizontal = 16.dp), horizontalArrangement = Arrangement.spacedBy(16.dp)) {
            Button(
                onClick = { mainViewModel.playLocalPlaylist(musicList, 0, shuffle = true) },
                modifier = Modifier.weight(1f).neonGlow(color = dominantColor ?: MaterialTheme.colorScheme.primary, cornerRadius = 24.dp, enabled = userStats.neonBorders),
                colors = ButtonDefaults.buttonColors(containerColor = dominantColor ?: MaterialTheme.colorScheme.primary)
            ) {
                Icon(Icons.Rounded.Shuffle, contentDescription = null)
                Spacer(modifier = Modifier.width(8.dp))
                Text("Aleatorio")
            }
            Button(
                onClick = { mainViewModel.playLikedPlaylist() },
                modifier = Modifier.weight(1f).neonGlow(color = Color(0xFFE91E63), cornerRadius = 24.dp, enabled = userStats.neonBorders),
                colors = ButtonDefaults.buttonColors(containerColor = Color(0xFFE91E63))
            ) {
                Icon(Icons.Rounded.Favorite, contentDescription = null)
                Spacer(modifier = Modifier.width(8.dp))
                Text("Favoritos")
            }
        }"""
        
content = content.replace(target_buttons, replacement_buttons)

with open("app/src/main/java/com/example/ui/screens/LocalMusicScreen.kt", "w") as f:
    f.write(content)
