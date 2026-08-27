import re

with open("app/src/main/java/com/example/ui/screens/LocalMusicScreen.kt", "r") as f:
    content = f.read()

target1 = """                Row(
                    modifier = Modifier
                        .fillMaxWidth()
                        .clickable { showingLiked = !showingLiked }
                        .padding(horizontal = 16.dp, vertical = 8.dp),"""
replacement1 = """                Row(
                    modifier = Modifier
                        .fillMaxWidth()
                        .padding(horizontal = 8.dp, vertical = 2.dp)
                        .clip(RoundedCornerShape(12.dp))
                        .clickable { showingLiked = !showingLiked }
                        .padding(horizontal = 8.dp, vertical = 8.dp),"""
                        
target2 = """                    Row(
                        modifier = Modifier
                            .fillMaxWidth()
                            .clickable {"""
replacement2 = """                    Row(
                        modifier = Modifier
                            .fillMaxWidth()
                            .padding(horizontal = 8.dp, vertical = 2.dp)
                            .clip(RoundedCornerShape(12.dp))
                            .clickable {"""
                            
target3 = """                Row(
                    modifier = Modifier
                        .fillMaxWidth()
                        .clickable {"""

content = content.replace(target1, replacement1)
content = content.replace(target2, replacement2)
content = content.replace(target3, replacement2)

with open("app/src/main/java/com/example/ui/screens/LocalMusicScreen.kt", "w") as f:
    f.write(content)
