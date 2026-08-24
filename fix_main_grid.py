import re

with open("app/src/main/java/com/example/MainActivity.kt", "r") as f:
    content = f.read()

target = """                LazyVerticalGrid(
                    columns = GridCells.Adaptive(minSize = 350.dp),
                    modifier = Modifier.fillMaxSize(),
                    contentPadding = PaddingValues(bottom = 100.dp)
                ) {
                    androidx.compose.foundation.lazy.grid.itemsIndexed(sState.results) { index, track ->
                        Row(
                            modifier = Modifier
                                .fillMaxWidth()
                                .clickable { viewModel.playFromRemotePlaylist(sState.results, index, userStats.apiPreference) }
                                .padding(horizontal = 16.dp, vertical = 8.dp),
                            verticalAlignment = Alignment.CenterVertically
                        ) {"""

replacement = """                LazyVerticalGrid(
                    columns = GridCells.Adaptive(minSize = 350.dp),
                    modifier = Modifier.fillMaxSize(),
                    contentPadding = PaddingValues(bottom = 100.dp)
                ) {
                    items(sState.results.size) { index ->
                        val track = sState.results[index]
                        Row(
                            modifier = Modifier
                                .fillMaxWidth()
                                .clickable { viewModel.playFromRemotePlaylist(sState.results, index, userStats.apiPreference) }
                                .padding(horizontal = 16.dp, vertical = 8.dp),
                            verticalAlignment = Alignment.CenterVertically
                        ) {"""
content = content.replace(target, replacement)

with open("app/src/main/java/com/example/MainActivity.kt", "w") as f:
    f.write(content)
