import re

with open("app/src/main/java/com/example/ui/screens/ProfileScreen.kt", "r") as f:
    content = f.read()

content = content.replace("stats.listeningTime", "stats.totalListeningSeconds")
content = content.replace("stats.songsDownloaded", "stats.totalDownloads")

if "import androidx.compose.foundation.clickable" not in content:
    content = content.replace("import androidx.compose.foundation.layout.*", "import androidx.compose.foundation.layout.*\nimport androidx.compose.foundation.clickable")

with open("app/src/main/java/com/example/ui/screens/ProfileScreen.kt", "w") as f:
    f.write(content)
