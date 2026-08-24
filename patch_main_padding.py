import re

with open("app/src/main/java/com/example/MainActivity.kt", "r") as f:
    content = f.read()

old_lazy = """                LazyColumn(
                    modifier = Modifier.fillMaxSize()
                ) {"""
new_lazy = """                LazyColumn(
                    modifier = Modifier.fillMaxSize(),
                    contentPadding = PaddingValues(bottom = 100.dp)
                ) {"""

content = content.replace(old_lazy, new_lazy)

with open("app/src/main/java/com/example/MainActivity.kt", "w") as f:
    f.write(content)
