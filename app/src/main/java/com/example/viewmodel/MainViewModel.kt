package com.example.viewmodel

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.example.data.AlyaCoreApi
import com.example.data.ITunesApi
import com.example.data.ITunesTrack
import com.example.data.LrcLibApi
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.launch

sealed class SearchState {
    object Idle : SearchState()
    object Loading : SearchState()
    data class Success(val results: List<ITunesTrack>) : SearchState()
    data class Error(val message: String) : SearchState()
}

sealed class DownloadState {
    object Idle : DownloadState()
    object Loading : DownloadState()
    data class Success(val title: String, val url: String, val thumbnail: String?) : DownloadState()
    data class Error(val message: String) : DownloadState()
}

class MainViewModel : ViewModel() {
    private val api = AlyaCoreApi.create()
    private val iTunesApi = ITunesApi.create()
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

    private val _searchState = MutableStateFlow<SearchState>(SearchState.Idle)
    val searchState: StateFlow<SearchState> = _searchState

    private val _downloadState = MutableStateFlow<DownloadState>(DownloadState.Idle)
    val downloadState: StateFlow<DownloadState> = _downloadState

    fun searchITunes(query: String) {
        if (query.isBlank()) return
        _searchState.value = SearchState.Loading
        _downloadState.value = DownloadState.Idle
        viewModelScope.launch {
            try {
                val response = iTunesApi.searchTracks(term = query)
                _searchState.value = SearchState.Success(response.results)
            } catch (e: Exception) {
                _searchState.value = SearchState.Error(e.localizedMessage ?: "Error searching tracks")
            }
        }
    }

    fun selectTrack(trackName: String, artistName: String, apiPref: String) {
        _downloadState.value = DownloadState.Loading
        val fullQuery = "$trackName $artistName"
        viewModelScope.launch {
            try {
                var success = false
                if (apiPref == "Spotify" || apiPref == "Both") {
                    try {
                        val spotRes = api.searchSpotify(query = fullQuery)
                        if (spotRes.status && spotRes.data?.downloadUrl != null) {
                            _downloadState.value = DownloadState.Success(
                                title = spotRes.data.title ?: trackName,
                                url = spotRes.data.downloadUrl,
                                thumbnail = spotRes.data.cover
                            )
                            success = true
                        }
                    } catch (e: Exception) {
                        // ignore and fallback if Both
                    }
                }
                
                if (!success && (apiPref == "YouTube" || apiPref == "Both")) {
                    try {
                        val ytRes = api.searchYouTube(query = fullQuery)
                        if (ytRes.status && ytRes.data?.downloadUrl != null) {
                            _downloadState.value = DownloadState.Success(
                                title = ytRes.data.title ?: trackName,
                                url = ytRes.data.downloadUrl,
                                thumbnail = ytRes.data.thumbnail
                            )
                            success = true
                        }
                    } catch (e: Exception) {
                        // ignore
                    }
                }
                
                if (!success) {
                    _downloadState.value = DownloadState.Error("No download URL found on selected APIs")
                }
            } catch (e: Exception) {
                _downloadState.value = DownloadState.Error(e.localizedMessage ?: "Unknown Error")
            }
        }
    }

    fun resetState() {
        _downloadState.value = DownloadState.Idle
        _searchState.value = SearchState.Idle
    }
}
