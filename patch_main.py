import re

with open("app/src/main/java/com/example/MainActivity.kt", "r") as f:
    content = f.read()

# Replace onPlaybackStateChanged
target_listener = """                    override fun onPlaybackStateChanged(playbackState: Int) {
                        if (playbackState == androidx.media3.common.Player.STATE_ENDED) {
                            // Queue ended, play next random
                            viewModel.playNextRandomTrack(profileViewModel.userStats.value.apiPreference)
                        }
                    }"""

replacement_listener = """                    override fun onPlaybackStateChanged(playbackState: Int) {
                        if (playbackState == androidx.media3.common.Player.STATE_ENDED) {
                            // Queue ended, try next remote, else random
                            if (mediaController?.mediaItemCount == 1) {
                                if (!viewModel.playNextRemote()) {
                                    viewModel.playNextRandomTrack(profileViewModel.userStats.value.apiPreference)
                                }
                            }
                        }
                    }"""
content = content.replace(target_listener, replacement_listener)

# Replace LazyVerticalGrid in Search Results
target_grid = """                LazyVerticalGrid(
                    columns = GridCells.Adaptive(minSize = 350.dp),
                    modifier = Modifier.fillMaxSize(),
                    contentPadding = PaddingValues(bottom = 100.dp)
                ) {
                    items(sState.results) { track ->
                        Row(
                            modifier = Modifier
                                .fillMaxWidth()
                                .clickable { viewModel.selectTrack(track.trackName ?: "", track.artistName ?: "", userStats.apiPreference, "play") }"""

replacement_grid = """                LazyVerticalGrid(
                    columns = GridCells.Adaptive(minSize = 350.dp),
                    modifier = Modifier.fillMaxSize(),
                    contentPadding = PaddingValues(bottom = 100.dp)
                ) {
                    androidx.compose.foundation.lazy.grid.itemsIndexed(sState.results) { index, track ->
                        Row(
                            modifier = Modifier
                                .fillMaxWidth()
                                .clickable { viewModel.playFromRemotePlaylist(sState.results, index, userStats.apiPreference) }"""
content = content.replace(target_grid, replacement_grid)

with open("app/src/main/java/com/example/MainActivity.kt", "w") as f:
    f.write(content)
