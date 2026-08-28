import re

with open('app/src/main/java/com/example/ui/components/PlayerControls.kt', 'r') as f:
    content = f.read()

# Adjust Previous and Next Icon sizes
content = content.replace('Icons.Rounded.SkipPrevious, contentDescription = "Previous", modifier = Modifier.size(48.dp)', 'Icons.Rounded.SkipPrevious, contentDescription = "Previous", modifier = Modifier.size(40.dp)')
content = content.replace('Icons.Rounded.SkipNext, contentDescription = "Next", modifier = Modifier.size(48.dp)', 'Icons.Rounded.SkipNext, contentDescription = "Next", modifier = Modifier.size(40.dp)')

# Adjust Play/Pause Box and Icon size
content = content.replace('.size(64.dp)', '.size(72.dp)')
content = content.replace('.size(36.dp)', '.size(40.dp)')

with open('app/src/main/java/com/example/ui/components/PlayerControls.kt', 'w') as f:
    f.write(content)

