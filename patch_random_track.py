import re

with open("app/src/main/java/com/example/viewmodel/MainViewModel.kt", "r") as f:
    content = f.read()

random_method = """    fun playNextRandomTrack(apiPref: String) {
        viewModelScope.launch {
            val randomQueries = listOf("Pop Hits 2024", "LoFi beats", "Top 50 Global", "Rock Classics", "Synthwave", "Chill Vibes", "Viral hits")
            var query = randomQueries.random()
            
            val liked = likedTracks.value
            if (liked.isNotEmpty()) {
                val randomLiked = liked.random()
                // Use the artist of a liked song as a seed for random
                query = "${randomLiked.artist} songs"
            }
            
            // Search iTunes for this random query, pick a random track, then select it.
            _searchState.value = SearchState.Loading
            try {
                val response = itunesApi.search(term = query, limit = 25)
                if (response.results.isNotEmpty()) {
                    val track = response.results.random()
                    selectTrack(track.trackName ?: "", track.artistName ?: "", apiPref, "play")
                } else {
                    _searchState.value = SearchState.Error("No random tracks found")
                }
            } catch (e: Exception) {
                _searchState.value = SearchState.Error("Failed to fetch random track")
            }
        }
    }"""

# Insert before resetState()
content = content.replace("    fun resetState() {", random_method + "\n\n    fun resetState() {")

with open("app/src/main/java/com/example/viewmodel/MainViewModel.kt", "w") as f:
    f.write(content)
