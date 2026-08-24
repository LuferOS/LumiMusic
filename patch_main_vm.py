import re

with open("app/src/main/java/com/example/viewmodel/MainViewModel.kt", "r") as f:
    content = f.read()

target = """    private val _lyricsState = MutableStateFlow<String?>("No lyrics found")
    val lyricsState: StateFlow<String?> = _lyricsState

    fun fetchLyrics(trackName: String, artistName: String) {
        _lyricsState.value = "Loading lyrics..."
        viewModelScope.launch {
            try {
                val response = api.searchLyrics(query = "$trackName $artistName")
                if (response.status && response.data != null && response.data.isNotEmpty()) {
                    _lyricsState.value = response.data.first().lyrics ?: "No lyrics available"
                } else {
                    _lyricsState.value = "No lyrics found"
                }
            } catch (e: Exception) {
                _lyricsState.value = "Failed to load lyrics"
            }
        }
    }"""

replacement = """    private val _lyricsState = MutableStateFlow<String?>("No lyrics found")
    val lyricsState: StateFlow<String?> = _lyricsState
    
    private val _lrcState = MutableStateFlow<List<LrcLine>?>(null)
    val lrcState: StateFlow<List<LrcLine>?> = _lrcState

    fun fetchLyrics(trackName: String, artistName: String) {
        _lyricsState.value = "Loading lyrics..."
        _lrcState.value = null
        viewModelScope.launch {
            try {
                val response = api.searchLyrics(query = "$trackName $artistName")
                if (response.status && response.data != null && response.data.isNotEmpty()) {
                    val first = response.data.first()
                    _lyricsState.value = first.lyrics ?: "No lyrics available"
                    if (!first.lrc.isNullOrBlank()) {
                        _lrcState.value = LrcParser.parse(first.lrc)
                    }
                } else {
                    _lyricsState.value = "No lyrics found"
                }
            } catch (e: Exception) {
                _lyricsState.value = "Failed to load lyrics"
            }
        }
    }"""

content = content.replace(target, replacement)

# ensure LrcLine and LrcParser imports are there
if "import com.example.utils.LrcLine" not in content:
    content = content.replace("import com.example.data.LrcLibApi", "import com.example.utils.LrcLine\nimport com.example.utils.LrcParser\nimport com.example.data.LrcLibApi")

with open("app/src/main/java/com/example/viewmodel/MainViewModel.kt", "w") as f:
    f.write(content)
