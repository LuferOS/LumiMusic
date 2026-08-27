with open("app/src/main/java/com/example/ui/components/CustomizationDialog.kt", "r") as f:
    content = f.read()

import re

target = """                Spacer(modifier = Modifier.height(16.dp))
                Text("Fuente del Reproductor", style = MaterialTheme.typography.labelMedium)
                Row(modifier = Modifier.fillMaxWidth().horizontalScroll(rememberScrollState()), horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                    fonts.forEach { font ->
                        FilterChip(
                            selected = playerFont == font,
                            onClick = { playerFont = font },
                            label = { Text(font) }
                        )
                    }
                }"""

content = content.replace(target, "")

with open("app/src/main/java/com/example/ui/components/CustomizationDialog.kt", "w") as f:
    f.write(content)
