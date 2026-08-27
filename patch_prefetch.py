import re

with open("app/src/main/java/com/example/viewmodel/MainViewModel.kt", "r") as f:
    content = f.read()

target = """                val response = withContext(Dispatchers.IO) { iTunesApi.searchTracks(term = query) }
                _searchState.value = SearchState.Success(response.results)"""

replacement = """                val response = withContext(Dispatchers.IO) { iTunesApi.searchTracks(term = query) }
                _searchState.value = SearchState.Success(response.results)
                
                // Prefetch first result in background to accelerate playback
                if (response.results.isNotEmpty()) {
                    val first = response.results.first()
                    viewModelScope.launch(Dispatchers.IO) {
                        try {
                            val resolvedUrl = AlyaCoreApi.resolveTrackUrl(first.trackName ?: "", first.artistName ?: "", currentApiPref)
                            if (resolvedUrl.isNotEmpty()) {
                                com.example.player.PrefetchManager.prefetchUrl(appContext, resolvedUrl)
                            }
                        } catch(e: Exception) {
                            e.printStackTrace()
                        }
                    }
                }"""

content = content.replace(target, replacement)
with open("app/src/main/java/com/example/viewmodel/MainViewModel.kt", "w") as f:
    f.write(content)
