import re

with open("app/src/main/java/com/example/ui/screens/LocalMusicScreen.kt", "r") as f:
    content = f.read()

target = """            IconButton(onClick = { /* Add */ }) {
                Icon(Icons.Rounded.Add, contentDescription = "Add", tint = Color.White)
            }"""
            
content = content.replace(target, "")

with open("app/src/main/java/com/example/ui/screens/LocalMusicScreen.kt", "w") as f:
    f.write(content)
