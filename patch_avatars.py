import re

# LocalMusicScreen.kt
with open('app/src/main/java/com/example/ui/screens/LocalMusicScreen.kt', 'r') as f:
    content = f.read()

content = content.replace('Color(0xFFFF5722)', 'Color(0xFF1DB954)')

with open('app/src/main/java/com/example/ui/screens/LocalMusicScreen.kt', 'w') as f:
    f.write(content)

# ProfileScreen.kt
with open('app/src/main/java/com/example/ui/screens/ProfileScreen.kt', 'r') as f:
    content = f.read()

content = content.replace('Color(0xFFFF5722)', 'Color(0xFF1DB954)')

with open('app/src/main/java/com/example/ui/screens/ProfileScreen.kt', 'w') as f:
    f.write(content)
