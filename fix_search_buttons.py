import re

with open("app/src/main/java/com/example/MainActivity.kt", "r") as f:
    content = f.read()

target_more_options = """                            IconButton(onClick = { /* More options */ }) {
                                Icon(Icons.Rounded.MoreVert, contentDescription = "More", tint = Color.White.copy(alpha = 0.6f))
                            }"""

content = content.replace(target_more_options, "")

with open("app/src/main/java/com/example/MainActivity.kt", "w") as f:
    f.write(content)
