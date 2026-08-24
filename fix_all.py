import re

with open("app/src/main/java/com/example/ui/components/FullScreenPlayer.kt", "r") as f:
    content = f.read()

# Let's find the AsyncImage block and replace everything up to Spacer
target_regex = r"if \(artworkUri != null\) \{[\s\S]*?else \{[\s\S]*?Icon\([\s\S]*?tint = Color\.White\.copy\(alpha = 0\.3f\)[\s\S]*?\n\s*\}[ \t\n]*Spacer\(modifier = Modifier\.weight\(0\.3f\)\)"

replacement = """if (artworkUri != null) {
                    AsyncImage(
                        model = artworkUri,
                        contentDescription = "Album Art",
                        contentScale = ContentScale.Crop,
                        modifier = Modifier.fillMaxSize()
                    )
                } else {
                    Icon(
                        imageVector = Icons.Rounded.MusicNote,
                        contentDescription = null,
                        modifier = Modifier.size(100.dp),
                        tint = Color.White.copy(alpha = 0.3f)
                    )
                }
                }
            }

            Spacer(modifier = Modifier.weight(0.3f))"""

import re
content = re.sub(target_regex, replacement, content)

with open("app/src/main/java/com/example/ui/components/FullScreenPlayer.kt", "w") as f:
    f.write(content)
