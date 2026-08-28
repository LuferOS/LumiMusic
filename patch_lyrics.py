import re

with open('app/src/main/java/com/example/ui/components/LyricsBottomSheet.kt', 'r') as f:
    content = f.read()

content = content.replace('style = MaterialTheme.typography.bodyLarge,', 'style = MaterialTheme.typography.titleLarge.copy(lineHeight = androidx.compose.ui.unit.sp(32)),\n                color = MaterialTheme.colorScheme.onSurface.copy(alpha = 0.8f),\n                textAlign = androidx.compose.ui.text.style.TextAlign.Center,')
if 'import androidx.compose.ui.unit.sp' not in content:
    content = content.replace('import androidx.compose.ui.unit.dp', 'import androidx.compose.ui.unit.dp\nimport androidx.compose.ui.unit.sp')

with open('app/src/main/java/com/example/ui/components/LyricsBottomSheet.kt', 'w') as f:
    f.write(content)
