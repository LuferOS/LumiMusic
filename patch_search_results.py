import re

with open("app/src/main/java/com/example/MainActivity.kt", "r") as f:
    content = f.read()

target = """                        Row(
                            modifier = Modifier
                                .fillMaxWidth()
                                .clickable { viewModel.playFromRemotePlaylist(sState.results, index, userStats.apiPreference) }
                                .padding(horizontal = 16.dp, vertical = 8.dp),"""

replacement = """                        Row(
                            modifier = Modifier
                                .fillMaxWidth()
                                .padding(horizontal = 8.dp, vertical = 2.dp)
                                .clip(RoundedCornerShape(12.dp))
                                .clickable { viewModel.playFromRemotePlaylist(sState.results, index, userStats.apiPreference) }
                                .padding(horizontal = 8.dp, vertical = 8.dp),"""
                                
content = content.replace(target, replacement)

with open("app/src/main/java/com/example/MainActivity.kt", "w") as f:
    f.write(content)
