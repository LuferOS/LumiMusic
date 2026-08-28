import re

with open('app/src/main/java/com/example/ui/screens/LocalMusicScreen.kt', 'r') as f:
    content = f.read()

# Make artworks slightly larger in lists for a modern look
content = content.replace(".size(56.dp)", ".size(64.dp)")
content = content.replace(".clip(RoundedCornerShape(8.dp))", ".clip(RoundedCornerShape(12.dp))")
content = content.replace('Color.White.copy(alpha = 0.6f)', 'Color.White.copy(alpha = 0.5f)')

with open('app/src/main/java/com/example/ui/screens/LocalMusicScreen.kt', 'w') as f:
    f.write(content)
