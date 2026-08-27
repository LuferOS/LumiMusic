with open("app/src/main/java/com/example/ui/components/MiniPlayer.kt", "r") as f:
    content = f.read()

target2 = """                        Text(
                            text = currentArtist, 
                            style = MaterialTheme.typography.bodySmall, 
                            color = Color.White.copy(alpha = 0.7f), 
                            maxLines = 1,
                            overflow = TextOverflow.Ellipsis
                        )"""

replacement2 = """                        Text(
                            text = currentArtist, 
                            style = MaterialTheme.typography.bodySmall, 
                            color = Color.White.copy(alpha = 0.7f), 
                            maxLines = 1,
                            modifier = Modifier.androidx.compose.foundation.basicMarquee()
                        )"""

if target2 in content:
    content = content.replace(target2, replacement2)
else:
    print("Could not find MiniPlayer artist target")

with open("app/src/main/java/com/example/ui/components/MiniPlayer.kt", "w") as f:
    f.write(content)
