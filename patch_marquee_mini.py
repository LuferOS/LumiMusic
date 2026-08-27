with open("app/src/main/java/com/example/ui/components/MiniPlayer.kt", "r") as f:
    content = f.read()

target1 = """                        Text(
                            text = currentTitle, 
                            style = MaterialTheme.typography.bodyMedium, 
                            fontWeight = FontWeight.Bold, 
                            color = Color.White,
                            maxLines = 1,
                            overflow = TextOverflow.Ellipsis
                        )"""

replacement1 = """                        Text(
                            text = currentTitle, 
                            style = MaterialTheme.typography.bodyMedium, 
                            fontWeight = FontWeight.Bold, 
                            color = Color.White,
                            maxLines = 1,
                            modifier = Modifier.androidx.compose.foundation.basicMarquee()
                        )"""

if target1 in content:
    content = content.replace(target1, replacement1)
else:
    print("Could not find MiniPlayer title target")

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
