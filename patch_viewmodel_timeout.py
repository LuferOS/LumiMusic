import re

with open("app/src/main/java/com/example/viewmodel/MainViewModel.kt", "r") as f:
    content = f.read()

# Add withTimeoutOrNull to searchITunes
target_search = """        viewModelScope.launch {
            _searchState.value = SearchState.Loading
            try {
                val results = mutableListOf<com.example.data.Track>()"""
                
replace_search = """        viewModelScope.launch {
            _searchState.value = SearchState.Loading
            try {
                val results = mutableListOf<com.example.data.Track>()
                kotlinx.coroutines.withTimeout(15000) {"""
                
target_search_end = """                }
                
                if (results.isEmpty()) {"""
                
replace_search_end = """                } // end timeout
                }
                
                if (results.isEmpty()) {"""

content = content.replace(target_search, replace_search)
content = content.replace(target_search_end, replace_search_end)

# Add timeout error catch
target_catch = """            } catch (e: Exception) {
                _searchState.value = SearchState.Error("Error: ${e.message}")
            }"""
replace_catch = """            } catch (e: kotlinx.coroutines.TimeoutCancellationException) {
                _searchState.value = SearchState.Error("Tiempo de espera agotado. Verifica tu conexión a internet.")
            } catch (e: Exception) {
                _searchState.value = SearchState.Error("Error: ${e.message}")
            }"""
            
content = content.replace(target_catch, replace_catch)

# Also apply timeout to selectTrack (download/play API call)
target_select = """        viewModelScope.launch {
            _downloadState.value = DownloadState.Loading
            try {
                var urlToPlay: String? = null"""

replace_select = """        viewModelScope.launch {
            _downloadState.value = DownloadState.Loading
            try {
                var urlToPlay: String? = null
                kotlinx.coroutines.withTimeout(15000) {"""

target_select_end = """                if (urlToPlay != null) {
                    _downloadState.value = DownloadState.Success(urlToPlay!!, title, action, artworkUrl)"""
replace_select_end = """                } // end timeout
                
                if (urlToPlay != null) {
                    _downloadState.value = DownloadState.Success(urlToPlay!!, title, action, artworkUrl)"""
                    
content = content.replace(target_select, replace_select)
content = content.replace(target_select_end, replace_select_end)

target_select_catch = """            } catch (e: Exception) {
                _downloadState.value = DownloadState.Error("Error resolving track: ${e.message}")
            }"""
replace_select_catch = """            } catch (e: kotlinx.coroutines.TimeoutCancellationException) {
                _downloadState.value = DownloadState.Error("Tiempo de espera agotado en Alya Core.")
            } catch (e: Exception) {
                _downloadState.value = DownloadState.Error("Error resolving track: ${e.message}")
            }"""
            
content = content.replace(target_select_catch, replace_select_catch)

with open("app/src/main/java/com/example/viewmodel/MainViewModel.kt", "w") as f:
    f.write(content)
