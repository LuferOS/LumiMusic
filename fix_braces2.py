import re

with open("app/src/main/java/com/example/ui/components/FullScreenPlayer.kt", "r") as f:
    content = f.read()

target = """                }
            }

            Spacer(modifier = Modifier.weight(0.3f))"""

replacement = """            }

            Spacer(modifier = Modifier.weight(0.3f))"""

content = content.replace(target, replacement)

with open("app/src/main/java/com/example/ui/components/FullScreenPlayer.kt", "w") as f:
    f.write(content)
