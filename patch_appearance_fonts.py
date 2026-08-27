with open("app/src/main/java/com/example/ui/screens/ProfileScreen.kt", "r") as f:
    content = f.read()

target = """                    Text("Color de Acento", style = MaterialTheme.typography.labelLarge)
                    neonColors.forEach { (hex, name) ->
                        Row(verticalAlignment = Alignment.CenterVertically, modifier = Modifier.fillMaxWidth().clickable { selectedPrimary = hex }) {
                            RadioButton(selected = selectedPrimary == hex, onClick = { selectedPrimary = hex })
                            Text(name)
                        }
                    }"""

replacement = """                    Text("Color de Acento", style = MaterialTheme.typography.labelLarge)
                    
                    // Chip selection for neon colors
                    androidx.compose.foundation.lazy.LazyRow(modifier = Modifier.fillMaxWidth().padding(vertical = 8.dp), horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                        items(neonColors.size) { index ->
                            val colorData = neonColors[index]
                            androidx.compose.material3.FilterChip(
                                selected = selectedPrimary == colorData.first,
                                onClick = { selectedPrimary = colorData.first },
                                label = { Text(colorData.second) }
                            )
                        }
                    }
                    
                    HorizontalDivider(modifier = Modifier.padding(vertical = 8.dp))
                    
                    Text("Tipografía de la App", style = MaterialTheme.typography.labelLarge)
                    androidx.compose.foundation.lazy.LazyRow(modifier = Modifier.fillMaxWidth().padding(vertical = 8.dp), horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                        items(fonts.size) { index ->
                            val fName = fonts[index]
                            androidx.compose.material3.FilterChip(
                                selected = selectedFont == fName,
                                onClick = { selectedFont = fName },
                                label = { Text(fName) }
                            )
                        }
                    }"""

content = content.replace(target, replacement)
with open("app/src/main/java/com/example/ui/screens/ProfileScreen.kt", "w") as f:
    f.write(content)
