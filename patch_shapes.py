import re

# Patch PlayerArtwork.kt
with open('app/src/main/java/com/example/ui/components/PlayerArtwork.kt', 'r') as f:
    content = f.read()
content = content.replace('RoundedCornerShape(8.dp)', 'RoundedCornerShape(24.dp)')
with open('app/src/main/java/com/example/ui/components/PlayerArtwork.kt', 'w') as f:
    f.write(content)

# Patch MiniPlayer.kt
with open('app/src/main/java/com/example/ui/components/MiniPlayer.kt', 'r') as f:
    content = f.read()
content = content.replace('RoundedCornerShape(8.dp)', 'RoundedCornerShape(32.dp)')
content = content.replace('.padding(horizontal = 8.dp, vertical = 4.dp)', '.padding(horizontal = 16.dp, vertical = 8.dp)')
# Let's also make the album art inside the mini player rounded like a circle
content = content.replace('.clip(RoundedCornerShape(4.dp))', '.clip(androidx.compose.foundation.shape.CircleShape)')
with open('app/src/main/java/com/example/ui/components/MiniPlayer.kt', 'w') as f:
    f.write(content)
