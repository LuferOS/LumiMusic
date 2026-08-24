import re

with open("app/src/main/java/com/example/ui/components/FullScreenPlayer.kt", "r") as f:
    content = f.read()

target = """                        val activeLineIndex by remember(currentPosition) {
                            derivedStateOf {
                                val lines = lrcState!!
                                val idx = lines.indexOfLast { it.timeMs <= currentPosition }
                                if (idx == -1) 0 else idx
                            }
                        }"""

replacement = """                        val activeLineIndex by remember(lrcState) {
                            derivedStateOf {
                                val lines = lrcState!!
                                val idx = lines.indexOfLast { it.timeMs <= currentPosition }
                                if (idx == -1) 0 else idx
                            }
                        }"""

content = content.replace(target, replacement)

with open("app/src/main/java/com/example/ui/components/FullScreenPlayer.kt", "w") as f:
    f.write(content)
