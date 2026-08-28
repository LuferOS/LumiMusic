import re

with open('app/src/main/java/com/example/ui/screens/MainScreen.kt', 'r') as f:
    content = f.read()

# Fix double clip
content = content.replace(".clip(RoundedCornerShape(8.dp))\n                                    .clip(RoundedCornerShape(8.dp))", ".clip(RoundedCornerShape(12.dp))")
content = content.replace(".size(56.dp)", ".size(64.dp)") # Make artworks slightly larger in lists for a modern look
content = content.replace('Color.White.copy(alpha = 0.6f)', 'Color.White.copy(alpha = 0.5f)')

# Update quotes
old_quotes = """                    listOf(
                        "Cargando...",
                        "Sabias que está aplicación fue una idea que de la nada se me ocurrió mientras veía una silla",
                        "La aplicación demoró 5 días en armarse, no esperaba la verdad demasiado."
                    ).random()"""
new_quotes = """                    listOf(
                        "Sintonizando frecuencias...",
                        "Buscando en la inmensidad musical...",
                        "Preparando el escenario para ti...",
                        "Conectando con Alya Core..."
                    ).random()"""
content = content.replace(old_quotes, new_quotes)

# Search idle state text
old_idle = """                            "Busca tus canciones favoritas", 
                             color = Color.White.copy(alpha = 0.6f),"""
new_idle = """                            "Explora un mundo de música", 
                             color = Color.White.copy(alpha = 0.6f),"""
content = content.replace(old_idle, new_idle)

old_idle_sub = """                            "Escribe el nombre de un artista, canción o pódcast para empezar a escuchar en Alya Core.", 
                             color = Color.White.copy(alpha = 0.4f),"""
new_idle_sub = """                            "Encuentra artistas, álbumes y canciones para empezar a reproducir de inmediato.", 
                             color = Color.White.copy(alpha = 0.4f),"""
content = content.replace(old_idle_sub, new_idle_sub)


with open('app/src/main/java/com/example/ui/screens/MainScreen.kt', 'w') as f:
    f.write(content)
