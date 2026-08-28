import re

with open('app/src/main/java/com/example/ui/screens/LocalMusicScreen.kt', 'r') as f:
    content = f.read()

content = content.replace('Text("L", color = Color.White, fontWeight = FontWeight.Bold) // Placeholder for profile initial', 'Text(userStats.userName.firstOrNull()?.toString()?.uppercase() ?: "U", color = Color.White, fontWeight = FontWeight.Bold)')

with open('app/src/main/java/com/example/ui/screens/LocalMusicScreen.kt', 'w') as f:
    f.write(content)
