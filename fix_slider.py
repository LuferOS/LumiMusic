import re

with open("app/src/main/java/com/example/ui/components/AudioSettingsBottomSheet.kt", "r") as f:
    content = f.read()

# I need to fix the modifier line:
# modifier = Modifier
#     .align(Alignment.Center)
#     .width(150.dp) // The height when rotated
#     .androidx.compose.ui.draw.rotate(-90f) // Vertical

if "import androidx.compose.ui.draw.rotate" not in content:
    content = content.replace("import androidx.compose.ui.draw.clip", "import androidx.compose.ui.draw.clip\nimport androidx.compose.ui.draw.rotate")

# Revert whatever my sed did
content = re.sub(r'\.androidx\.compose\.ui\.draw\.rotate\(-90f\)', '.rotate(-90f)', content)
# And if my sed replaced it with just "-90f", fix that
content = re.sub(r'\.-90f\(-90f\)', '.rotate(-90f)', content)
content = re.sub(r'\.-90f', '.rotate(-90f)', content)

with open("app/src/main/java/com/example/ui/components/AudioSettingsBottomSheet.kt", "w") as f:
    f.write(content)
