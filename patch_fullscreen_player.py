import re

with open('app/src/main/java/com/example/ui/components/FullScreenPlayer.kt', 'r') as f:
    content = f.read()

# Make the seekbar look more prominent and spacing more elegant
# Slider Modifier:
old_slider = """                modifier = Modifier
                    .fillMaxWidth()
                    .height(24.dp),"""
new_slider = """                modifier = Modifier
                    .fillMaxWidth()
                    .height(24.dp),""" # Wait, what if we just increase spacing?

# Let's adjust the Row above Slider to be spaced slightly differently.
old_times = """            Row(
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(top = 4.dp),
                horizontalArrangement = Arrangement.SpaceBetween
            ) {
                Text(formatTime(currentPosition), style = MaterialTheme.typography.labelMedium, color = Color.White.copy(alpha = 0.7f))
                Text(formatTime(duration), style = MaterialTheme.typography.labelMedium, color = Color.White.copy(alpha = 0.7f))
            }"""
new_times = """            Row(
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(horizontal = 8.dp),
                horizontalArrangement = Arrangement.SpaceBetween
            ) {
                Text(formatTime(currentPosition), style = MaterialTheme.typography.labelMedium, color = Color.White.copy(alpha = 0.5f), fontWeight = FontWeight.SemiBold)
                Text(formatTime(duration), style = MaterialTheme.typography.labelMedium, color = Color.White.copy(alpha = 0.5f), fontWeight = FontWeight.SemiBold)
            }"""

content = content.replace(old_times, new_times)

# Make the Lyrics Peek Box more unified
old_lyrics = """                    .background(if (isLyricsExpanded) Color.Black.copy(alpha = 0.6f) else Color.White.copy(alpha = 0.1f))"""
new_lyrics = """                    .background(if (isLyricsExpanded) Color.Black.copy(alpha = 0.4f) else Color.White.copy(alpha = 0.08f))"""

content = content.replace(old_lyrics, new_lyrics)

with open('app/src/main/java/com/example/ui/components/FullScreenPlayer.kt', 'w') as f:
    f.write(content)
