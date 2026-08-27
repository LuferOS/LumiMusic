with open("app/src/main/java/com/example/viewmodel/MainViewModel.kt", "r") as f:
    content = f.read()

target = """                val response = withContext(Dispatchers.IO) { iTunesApi.searchTracks(term = query) }
                _searchState.value = SearchState.Success(response.results)"""

replacement = """                val response = withContext(Dispatchers.IO) { iTunesApi.searchTracks(term = query) }
                if (response.results.isNotEmpty()) {
                    _searchState.value = SearchState.Success(response.results)
                } else {
                    // Fallback to YouTube API directly for long names that iTunes fails to find
                    val ytRes = withContext(Dispatchers.IO) { 
                        try { api.searchYouTube(query = query) } catch(e: Exception) { null }
                    }
                    if (ytRes != null && ytRes.status && ytRes.data != null) {
                        val fakeTrack = ITunesTrack(
                            trackName = ytRes.data.title ?: query,
                            artistName = ytRes.data.author ?: "YouTube",
                            artworkUrl100 = ytRes.data.thumbnail
                        )
                        _searchState.value = SearchState.Success(listOf(fakeTrack))
                    } else {
                        val spotRes = withContext(Dispatchers.IO) {
                            try { api.searchSpotify(query = query) } catch(e: Exception) { null }
                        }
                        if (spotRes != null && spotRes.status && spotRes.data != null) {
                            val fakeTrack = ITunesTrack(
                                trackName = spotRes.data.title ?: query,
                                artistName = spotRes.data.artist ?: "Spotify",
                                artworkUrl100 = spotRes.data.cover
                            )
                            _searchState.value = SearchState.Success(listOf(fakeTrack))
                        } else {
                            _searchState.value = SearchState.Success(emptyList())
                        }
                    }
                }"""

if target in content:
    content = content.replace(target, replacement)
else:
    print("Could not find search fallback target")

with open("app/src/main/java/com/example/viewmodel/MainViewModel.kt", "w") as f:
    f.write(content)
