package com.example.viewmodel
import android.app.Application
import androidx.lifecycle.AndroidViewModel
import com.example.data.local.AppDatabase
import com.example.data.local.LikedTrack
import kotlinx.coroutines.flow.SharingStarted
import kotlinx.coroutines.flow.stateIn

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.example.data.AlyaCoreApi
import com.example.data.ITunesApi
import com.example.data.ITunesTrack
import com.example.utils.LrcLine
import com.example.utils.LrcParser
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
    data class Success(val title: String, val url: String, val thumbnail: String?, val action: String = "play") : DownloadState()
    data class Error(val message: String) : DownloadState()
}



class MainViewModel(application: Application) : AndroidViewModel(application) {
    private val likedTrackDao = AppDatabase.getDatabase(application).likedTrackDao()
    
    val likedTracks = likedTrackDao.getAllLikedTracks()
        .stateIn(viewModelScope, SharingStarted.Lazily, emptyList())

    fun toggleLike(uri: String, title: String, artist: String, artworkUrl: String?) {
        viewModelScope.launch {
            val current = likedTracks.value.find { it.uri == uri }
            if (current != null) {
                likedTrackDao.deleteByUri(uri)
            } else {
                likedTrackDao.insertLikedTrack(LikedTrack(uri, title, artist, artworkUrl))
            }
        }
    }
    
    fun isLiked(uri: String): kotlinx.coroutines.flow.Flow<Boolean> {
        return likedTrackDao.isLiked(uri)
    }

    private val api = AlyaCoreApi.create()
    private val iTunesApi = ITunesApi.create()
    private val lrcLibApi = LrcLibApi.create()
    
    private val _lyricsState = MutableStateFlow<String?>("No lyrics found")
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
    }

    private val _searchState = MutableStateFlow<SearchState>(SearchState.Idle)
    val searchState: StateFlow<SearchState> = _searchState

    private val _downloadState = MutableStateFlow<DownloadState>(DownloadState.Idle)
    val downloadState: StateFlow<DownloadState> = _downloadState

    var remotePlaylist = emptyList<ITunesTrack>()
    var currentRemoteIndex = -1
    var currentApiPref = "Spotify"

    fun playFromRemotePlaylist(results: List<ITunesTrack>, index: Int, apiPref: String) {
        remotePlaylist = results
        currentRemoteIndex = index
        currentApiPref = apiPref
        val track = results[index]
        selectTrack(track.trackName ?: "", track.artistName ?: "", apiPref, "play")
    }

    fun playNextRemote(isShuffle: Boolean = false, repeatMode: Int = 0): Boolean {
        if (remotePlaylist.isEmpty() || currentRemoteIndex == -1) return false
        
        if (repeatMode == androidx.media3.common.Player.REPEAT_MODE_ONE) {
            // Keep same index
        } else if (isShuffle) {
            currentRemoteIndex = (remotePlaylist.indices).random()
        } else {
            currentRemoteIndex = (currentRemoteIndex + 1) % remotePlaylist.size
        }
        
        val track = remotePlaylist[currentRemoteIndex]
        selectTrack(track.trackName ?: "", track.artistName ?: "", currentApiPref, "play")
        return true
    }

    fun playPreviousRemote(isShuffle: Boolean = false, repeatMode: Int = 0): Boolean {
        if (remotePlaylist.isEmpty() || currentRemoteIndex == -1) return false
        
        if (repeatMode == androidx.media3.common.Player.REPEAT_MODE_ONE) {
            // Keep same index
        } else if (isShuffle) {
            currentRemoteIndex = (remotePlaylist.indices).random()
        } else {
            currentRemoteIndex = if (currentRemoteIndex - 1 < 0) remotePlaylist.size - 1 else currentRemoteIndex - 1
        }
        
        val track = remotePlaylist[currentRemoteIndex]
        selectTrack(track.trackName ?: "", track.artistName ?: "", currentApiPref, "play")
        return true
    }

    fun searchITunes(query: String) {
        if (query.isBlank()) return
        _searchState.value = SearchState.Loading
        _downloadState.value = DownloadState.Idle
        viewModelScope.launch {
            try {
                val response = withContext(Dispatchers.IO) { iTunesApi.searchTracks(term = query) }
                _searchState.value = SearchState.Success(response.results)
            } catch (e: Exception) {
                _searchState.value = SearchState.Error(e.localizedMessage ?: "Error searching tracks")
            }
        }
    }

    fun selectTrack(trackName: String, artistName: String, apiPref: String, action: String = "play") {
        _downloadState.value = DownloadState.Loading
        val fullQuery = "$trackName $artistName"
        viewModelScope.launch {
            try {
                var success = false
                
                suspend fun tryYouTube(): Boolean = withContext(Dispatchers.IO) {
                    try {
                        val ytRes = api.searchYouTube(query = fullQuery)
                        if (ytRes.status && ytRes.data?.downloadUrl != null) {
                            _downloadState.value = DownloadState.Success(
                                title = ytRes.data.title ?: trackName,
                                url = ytRes.data.downloadUrl,
                                thumbnail = ytRes.data.thumbnail,
                                action = action
                            )
                            return@withContext true
                        }
                    } catch (e: Exception) {}
                    return@withContext false
                }
                
                suspend fun trySpotify(): Boolean = withContext(Dispatchers.IO) {
                    try {
                        val spotRes = api.searchSpotify(query = fullQuery)
                        if (spotRes.status && spotRes.data?.downloadUrl != null) {
                            _downloadState.value = DownloadState.Success(
                                title = spotRes.data.title ?: trackName,
                                url = spotRes.data.downloadUrl,
                                thumbnail = spotRes.data.cover,
                                action = action
                            )
                            return@withContext true
                        }
                    } catch (e: Exception) {}
                    return@withContext false
                }
                
                if (apiPref == "YouTube") {
                    success = tryYouTube()
                } else if (apiPref == "Spotify") {
                    success = trySpotify()
                } else {
                    // Both: prefer YouTube, then Spotify fallback
                    success = tryYouTube()
                    if (!success) {
                        success = trySpotify()
                    }
                }
                
                if (!success) {
                    _downloadState.value = DownloadState.Error("Error al obtener la canción. Intenta nuevamente.")
                }
            } catch (e: Exception) {
                _downloadState.value = DownloadState.Error(e.localizedMessage ?: "Unknown Error")
            }
        }
    }

    fun playNextRandomTrack(apiPref: String) {
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
                val response = iTunesApi.searchTracks(term = query)
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
    }

    fun resetState() {
        _downloadState.value = DownloadState.Idle
    }
}
