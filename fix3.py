with open('app/src/main/java/com/example/ui/screens/ProfileScreen.kt', 'r') as f:
    lines = f.readlines()

new_header = """            // Header
            Row(
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(horizontal = 16.dp, vertical = 16.dp),
                verticalAlignment = Alignment.CenterVertically
            ) {
                Text(
                    text = "Configuración",
                    style = MaterialTheme.typography.titleLarge,
                    fontWeight = FontWeight.Bold,
                    color = Color.White,
                    modifier = Modifier.weight(1f),
                    textAlign = androidx.compose.ui.text.style.TextAlign.Center
                )
            }
"""

new_lines = lines[:56] + [new_header] + lines[70:]
with open('app/src/main/java/com/example/ui/screens/ProfileScreen.kt', 'w') as f:
    f.writelines(new_lines)
