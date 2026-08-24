import re

with open("app/src/main/java/com/example/ui/screens/ProfileScreen.kt", "r") as f:
    content = f.read()

target = """                    Text("API Preferida", style = MaterialTheme.typography.labelLarge)
                    Row(verticalAlignment = Alignment.CenterVertically) {
                        RadioButton(selected = apiPref == "itunes", onClick = { apiPref = "itunes" })
                        Text("iTunes (Rápido, 30s preview)")
                    }
                    Row(verticalAlignment = Alignment.CenterVertically) {
                        RadioButton(selected = apiPref == "youtube", onClick = { apiPref = "youtube" })
                        Text("YouTube (Audio completo)")
                    }"""

replacement = """                    Text("Motor de Descarga / Reproducción", style = MaterialTheme.typography.labelLarge)
                    Row(verticalAlignment = Alignment.CenterVertically, modifier = Modifier.fillMaxWidth().clickable { apiPref = "Spotify" }) {
                        RadioButton(selected = apiPref == "Spotify", onClick = { apiPref = "Spotify" })
                        Text("Spotify")
                    }
                    Row(verticalAlignment = Alignment.CenterVertically, modifier = Modifier.fillMaxWidth().clickable { apiPref = "YouTube" }) {
                        RadioButton(selected = apiPref == "YouTube", onClick = { apiPref = "YouTube" })
                        Text("YouTube")
                    }
                    Row(verticalAlignment = Alignment.CenterVertically, modifier = Modifier.fillMaxWidth().clickable { apiPref = "Both" }) {
                        RadioButton(selected = apiPref == "Both", onClick = { apiPref = "Both" })
                        Text("Ambas (Automático)")
                    }"""

content = content.replace(target, replacement)

with open("app/src/main/java/com/example/ui/screens/ProfileScreen.kt", "w") as f:
    f.write(content)
