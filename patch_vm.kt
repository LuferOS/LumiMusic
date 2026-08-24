    private val lrcLibApi = LrcLibApi.create()

    private val _lyricsState = MutableStateFlow<String?>("No lyrics found")
    val lyricsState: StateFlow<String?> = _lyricsState

    fun fetchLyrics(trackName: String, artistName: String) {
        _lyricsState.value = "Loading lyrics..."
        viewModelScope.launch {
            try {
                val results = lrcLibApi.searchLyrics(trackName, artistName)
                if (results.isNotEmpty()) {
                    _lyricsState.value = results.firstOrNull { it.plainLyrics != null }?.plainLyrics ?: "No plain lyrics available"
                } else {
                    _lyricsState.value = "No lyrics found"
                }
            } catch (e: Exception) {
                _lyricsState.value = "Failed to load lyrics"
            }
        }
    }
