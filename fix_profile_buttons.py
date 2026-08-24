import re

with open("app/src/main/java/com/example/ui/screens/ProfileScreen.kt", "r") as f:
    content = f.read()

target_back = """                IconButton(onClick = { /* Back */ }) {
                    Icon(Icons.Rounded.ArrowBack, contentDescription = "Back", tint = Color.White)
                }"""
content = content.replace(target_back, "")

target_search = """                IconButton(onClick = { /* Search Settings */ }) {
                    Icon(Icons.Rounded.Search, contentDescription = "Search", tint = Color.White)
                }"""
content = content.replace(target_search, "")

with open("app/src/main/java/com/example/ui/screens/ProfileScreen.kt", "w") as f:
    f.write(content)
