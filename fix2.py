with open('app/src/main/java/com/example/ui/screens/ProfileScreen.kt', 'r') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if "background(Color(0xFF121212))" in line:
        start_idx = i + 2
        break

for i, line in enumerate(lines[start_idx:]):
    if "Column(" in line and "verticalScroll(" in lines[start_idx+i+2]:
        end_idx = start_idx + i
        break

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

new_lines = lines[:start_idx] + [new_header] + lines[end_idx:]
with open('app/src/main/java/com/example/ui/screens/ProfileScreen.kt', 'w') as f:
    f.writelines(new_lines)
