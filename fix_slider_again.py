import re

with open("app/src/main/java/com/example/ui/components/AudioSettingsBottomSheet.kt", "r") as f:
    content = f.read()

content = content.replace("                                        -90f(-90f) // Vertical", "                                        .rotate(-90f) // Vertical")

with open("app/src/main/java/com/example/ui/components/AudioSettingsBottomSheet.kt", "w") as f:
    f.write(content)
