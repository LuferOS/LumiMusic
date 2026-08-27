with open("app/src/main/java/com/example/ui/components/CustomizationDialog.kt", "r") as f:
    content = f.read()

import re

# Add horizontalScroll import if not present
if "import androidx.compose.foundation.horizontalScroll" not in content:
    content = content.replace("import androidx.compose.foundation.verticalScroll", "import androidx.compose.foundation.verticalScroll\nimport androidx.compose.foundation.horizontalScroll")

# Expand visualizer colors
content = content.replace(
    """val vColors = listOf("Dinámico", "#1DB954", "#FF5722", "#E91E63", "#00BCD4")""",
    """val vColors = listOf("Dinámico", "#1DB954", "#FF5722", "#E91E63", "#00BCD4", "#9C27B0", "#FFEB3B", "#4CAF50", "#2196F3")"""
)

# Expand fonts
content = content.replace(
    """val fonts = listOf("Default", "Serif", "Monospace", "Cursive")""",
    """val fonts = listOf("Default", "Serif", "Monospace", "Cursive", "Sans-Serif")"""
)

# Make rows scrollable horizontally (first 4 rows only, the tab reorder row is fine as is)
# "Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceEvenly)"
content = content.replace(
    """Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceEvenly)""",
    """Row(modifier = Modifier.fillMaxWidth().horizontalScroll(rememberScrollState()), horizontalArrangement = Arrangement.spacedBy(8.dp))"""
)

with open("app/src/main/java/com/example/ui/components/CustomizationDialog.kt", "w") as f:
    f.write(content)
