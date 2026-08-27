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
import kotlinx.coroutines.async

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
    data class Append(val title: String, val url: String, val thumbnail: String?) : DownloadState()
    data class Error(val message: String) : DownloadState()
}



data class UpdateInfo(
    val isAvailable: Boolean = false,
    val newVersion: String = "",
    val updateUrl: String = "",
    val releaseNotes: String = ""
)

class MainViewModel(application: Application) : AndroidViewModel(application) {
    private val likedTrackDao = AppDatabase.getDatabase(application).likedTrackDao()
    
    val likedTracks = likedTrackDao.getAllLikedTracks()
        .stateIn(viewModelScope, SharingStarted.Lazily, emptyList())

    private val _updateInfo = MutableStateFlow(UpdateInfo())
    val updateInfo: StateFlow<UpdateInfo> = _updateInfo

    init {
        checkForUpdates()
    }

    private fun isNewerVersion(latest: String, current: String): Boolean {
        val lParts = latest.split(".").mapNotNull { it.toIntOrNull() }
        val cParts = current.split(".").mapNotNull { it.toIntOrNull() }
        val maxLength = maxOf(lParts.size, cParts.size)
        for (i in 0 until maxLength) {
            val l = lParts.getOrElse(i) { 0 }
            val c = cParts.getOrElse(i) { 0 }
            if (l > c) return true
            if (l < c) return false
        }
        return false
    }

    fun checkForUpdates() {
        viewModelScope.launch(Dispatchers.IO) {
            try {
                val owner = "LuferOS" 
                val repo = "LumiMusic" 
                
                val release = com.example.data.GitHubApi.service.getLatestRelease(owner, repo)
                val currentVersionName = com.example.BuildConfig.VERSION_NAME
                
                val latestVersion = release.tagName.removePrefix("v").removePrefix("V")
                val currentVersion = currentVersionName.removePrefix("v").removePrefix("V")
                
                if (isNewerVersion(latestVersion, currentVersion)) {
                    _updateInfo.value = UpdateInfo(
                        isAvailable = true,
                        newVersion = release.tagName,
                        updateUrl = release.htmlUrl,
                        releaseNotes = release.body ?: "Nueva versión detectada"
                    )
                }
            } catch (e: Exception) {
                e.printStackTrace()
            }
        }
    }

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
        viewModelScope.launch(Dispatchers.IO) {
            try {
                val deferredResult = kotlinx.coroutines.CompletableDeferred<Pair<String?, List<LrcLine>?>>()
                val fails = java.util.concurrent.atomic.AtomicInteger(0)
                
                launch(Dispatchers.IO) {
                    try {
                        val response = api.searchLyrics(query = "$trackName $artistName")
                        if (response.status && response.data != null && response.data.isNotEmpty()) {
                            val first = response.data.first()
                            val plain = first.lyrics ?: "No lyrics available"
                            val parsedLrc = if (!first.lrc.isNullOrBlank()) LrcParser.parse(first.lrc) else null
                            deferredResult.complete(plain to parsedLrc)
                        } else if (fails.incrementAndGet() == 2) {
                            deferredResult.complete("No lyrics found" to null)
                        }
                    } catch (e: Exception) {
                        if (fails.incrementAndGet() == 2) deferredResult.complete("Failed to load lyrics" to null)
                    }
                }
                
                launch(Dispatchers.IO) {
                    try {
                        val response = lrcLibApi.searchLyrics(trackName = trackName, artistName = artistName)
                        if (response.isNotEmpty()) {
                            val first = response.first()
                            val plain = first.plainLyrics ?: "No lyrics available"
                            val parsedLrc = if (!first.syncedLyrics.isNullOrBlank()) LrcParser.parse(first.syncedLyrics) else null
                            deferredResult.complete(plain to parsedLrc)
                        } else if (fails.incrementAndGet() == 2) {
                            deferredResult.complete("No lyrics found" to null)
                        }
                    } catch (e: Exception) {
                        if (fails.incrementAndGet() == 2) deferredResult.complete("Failed to load lyrics" to null)
                    }
                }
                
                val result = deferredResult.await()
                _lyricsState.value = result.first
                _lrcState.value = result.second
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

    private var prefetchJob: kotlinx.coroutines.Job? = null

    fun playFromRemotePlaylist(results: List<ITunesTrack>, index: Int, apiPref: String) {
        remotePlaylist = results
        currentRemoteIndex = index
        currentApiPref = apiPref
        val track = results[index]
        selectTrack(track.trackName ?: "", track.artistName ?: "", apiPref, "play")
        
        prefetchJob?.cancel()
        prefetchJob = viewModelScope.launch(Dispatchers.IO) {
            val scope = this
            kotlinx.coroutines.delay(1000)
            val prefetchDeferreds = (1..5).mapNotNull { i ->
                val nextIndex = index + i
                if (nextIndex < results.size) {
                    val nextTrack = results[nextIndex]
                    val fullQuery = "${nextTrack.trackName} ${nextTrack.artistName}"
                    
                    scope.async(Dispatchers.IO) {
                        var url: String? = null
                        var thumb: String? = null
                        
                        if (apiPref == "Ambos") {
                            val deferredResult = kotlinx.coroutines.CompletableDeferred<Pair<String?, String?>>()
                            val fails = java.util.concurrent.atomic.AtomicInteger(0)
                            scope.launch(Dispatchers.IO) {
                                try {
                                    val ytRes = api.searchYouTube(query = fullQuery)
                                    if (ytRes.status && ytRes.data?.downloadUrl != null) deferredResult.complete(ytRes.data.downloadUrl to ytRes.data.thumbnail)
                                    else if (fails.incrementAndGet() == 2) deferredResult.complete(null to null)
                                } catch(e: Exception) { if (fails.incrementAndGet() == 2) deferredResult.complete(null to null) }
                            }
                            scope.launch(Dispatchers.IO) {
                                try {
                                    val spotRes = api.searchSpotify(query = fullQuery)
                                    if (spotRes.status && spotRes.data?.downloadUrl != null) deferredResult.complete(spotRes.data.downloadUrl to spotRes.data.cover)
                                    else if (fails.incrementAndGet() == 2) deferredResult.complete(null to null)
                                } catch(e: Exception) { if (fails.incrementAndGet() == 2) deferredResult.complete(null to null) }
                            }
                            val res = deferredResult.await()
                            url = res.first
                            thumb = res.second
                        } else if (apiPref == "YouTube") {
                            try {
                                val ytRes = api.searchYouTube(query = fullQuery)
                                if (ytRes.status) { url = ytRes.data?.downloadUrl; thumb = ytRes.data?.thumbnail }
                            } catch (e: Exception) {}
                        } else {
                            try {
                                val spotRes = api.searchSpotify(query = fullQuery)
                                if (spotRes.status) { url = spotRes.data?.downloadUrl; thumb = spotRes.data?.cover }
                            } catch (e: Exception) {}
                        }
                        
                        if (url != null) DownloadState.Append(nextTrack.trackName ?: "", url, thumb) else null
                    }
                } else null
            }
            
            for (deferred in prefetchDeferreds) {
                val state = deferred.await()
                if (state != null) {
                    _downloadState.value = state
                    kotlinx.coroutines.delay(100)
                }
            }
        }
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
                if (response.results.isNotEmpty()) {
                    _searchState.value = SearchState.Success(response.results)
                } else {
                    // Fallback to YouTube and Spotify concurrently
                    val deferredResult = kotlinx.coroutines.CompletableDeferred<ITunesTrack?>()
                    val fails = java.util.concurrent.atomic.AtomicInteger(0)
                    
                    launch(Dispatchers.IO) {
                        try {
                            val ytRes = api.searchYouTube(query = query)
                            if (ytRes.status && ytRes.data != null) {
                                deferredResult.complete(ITunesTrack(
                                    trackName = ytRes.data.title ?: query,
                                    artistName = ytRes.data.author ?: "YouTube",
                                    artworkUrl100 = ytRes.data.thumbnail
                                ))
                            } else if (fails.incrementAndGet() == 2) deferredResult.complete(null)
                        } catch (e: Exception) { if (fails.incrementAndGet() == 2) deferredResult.complete(null) }
                    }
                    
                    launch(Dispatchers.IO) {
                        try {
                            val spotRes = api.searchSpotify(query = query)
                            if (spotRes.status && spotRes.data != null) {
                                deferredResult.complete(ITunesTrack(
                                    trackName = spotRes.data.title ?: query,
                                    artistName = spotRes.data.artist ?: "Spotify",
                                    artworkUrl100 = spotRes.data.cover
                                ))
                            } else if (fails.incrementAndGet() == 2) deferredResult.complete(null)
                        } catch(e: Exception) { if (fails.incrementAndGet() == 2) deferredResult.complete(null) }
                    }
                    
                    val fallbackTrack = deferredResult.await()
                    if (fallbackTrack != null) {
                        _searchState.value = SearchState.Success(listOf(fallbackTrack))
                    } else {
                        _searchState.value = SearchState.Success(emptyList())
                    }
                }
                
                // Prefetch first result in background to accelerate playback
                if (response.results.isNotEmpty()) {
                    val first = response.results.first()
                    viewModelScope.launch(Dispatchers.IO) {
                        try {
                            val fullQuery = "${first.trackName} ${first.artistName}"
                            val url = if (currentApiPref == "Spotify") {
                                api.searchSpotify(query = fullQuery).data?.downloadUrl
                            } else {
                                api.searchYouTube(query = fullQuery).data?.downloadUrl
                            }
                            if (url != null) {
                                com.example.player.PrefetchManager.prefetchUrl(getApplication<android.app.Application>(), url)
                            }
                        } catch(e: Exception) {
                            e.printStackTrace()
                        }
                    }
                }
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
                suspend fun fetchYouTube(): DownloadState.Success? = withContext(Dispatchers.IO) {
                    try {
                        val ytRes = api.searchYouTube(query = fullQuery)
                        if (ytRes.status && ytRes.data?.downloadUrl != null) {
                            return@withContext DownloadState.Success(
                                title = ytRes.data.title ?: trackName,
                                url = ytRes.data.downloadUrl,
                                thumbnail = ytRes.data.thumbnail,
                                action = action
                            )
                        }
                    } catch (e: Exception) {}
                    return@withContext null
                }

                suspend fun fetchSpotify(): DownloadState.Success? = withContext(Dispatchers.IO) {
                    try {
                        val spotRes = api.searchSpotify(query = fullQuery)
                        if (spotRes.status && spotRes.data?.downloadUrl != null) {
                            return@withContext DownloadState.Success(
                                title = spotRes.data.title ?: trackName,
                                url = spotRes.data.downloadUrl,
                                thumbnail = spotRes.data.cover,
                                action = action
                            )
                        }
                    } catch (e: Exception) {}
                    return@withContext null
                }

                var finalState: DownloadState.Success? = null

                if (apiPref == "YouTube") {
                    finalState = fetchYouTube()
                } else if (apiPref == "Spotify") {
                    finalState = fetchSpotify()
                } else {
                    // Ambos: get the fastest successful response using parallel fetching
                    val deferredResult = kotlinx.coroutines.CompletableDeferred<DownloadState.Success?>()
                    val fails = java.util.concurrent.atomic.AtomicInteger(0)
                    
                    launch(Dispatchers.IO) {
                        val res = fetchYouTube()
                        if (res != null) deferredResult.complete(res) 
                        else if (fails.incrementAndGet() == 2) deferredResult.complete(null)
                    }
                    launch(Dispatchers.IO) {
                        val res = fetchSpotify()
                        if (res != null) deferredResult.complete(res) 
                        else if (fails.incrementAndGet() == 2) deferredResult.complete(null)
                    }
                    finalState = deferredResult.await()
                }

                if (finalState != null) {
                    _downloadState.value = finalState
                } else {
                    _downloadState.value = DownloadState.Error("Error al obtener la canción. Intenta nuevamente.")
                }
            } catch (e: Exception) {
                _downloadState.value = DownloadState.Error(e.localizedMessage ?: "Unknown Error")
            }
        }
    }

    fun playNextRandomTrack(apiPref: String) {
        viewModelScope.launch(Dispatchers.IO) {
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
                    val deferredResult = kotlinx.coroutines.CompletableDeferred<ITunesTrack?>()
                    val fails = java.util.concurrent.atomic.AtomicInteger(0)
                    
                    launch(Dispatchers.IO) {
                        try {
                            val ytRes = api.searchYouTube(query = query)
                            if (ytRes.status && ytRes.data != null) {
                                deferredResult.complete(ITunesTrack(
                                    trackName = ytRes.data.title ?: query,
                                    artistName = ytRes.data.author ?: "YouTube",
                                    artworkUrl100 = ytRes.data.thumbnail
                                ))
                            } else if (fails.incrementAndGet() == 2) deferredResult.complete(null)
                        } catch (e: Exception) { if (fails.incrementAndGet() == 2) deferredResult.complete(null) }
                    }
                    
                    launch(Dispatchers.IO) {
                        try {
                            val spotRes = api.searchSpotify(query = query)
                            if (spotRes.status && spotRes.data != null) {
                                deferredResult.complete(ITunesTrack(
                                    trackName = spotRes.data.title ?: query,
                                    artistName = spotRes.data.artist ?: "Spotify",
                                    artworkUrl100 = spotRes.data.cover
                                ))
                            } else if (fails.incrementAndGet() == 2) deferredResult.complete(null)
                        } catch(e: Exception) { if (fails.incrementAndGet() == 2) deferredResult.complete(null) }
                    }
                    
                    val fallbackTrack = deferredResult.await()
                    if (fallbackTrack != null) {
                        selectTrack(fallbackTrack.trackName ?: "", fallbackTrack.artistName ?: "", apiPref, "play")
                    } else {
                        _searchState.value = SearchState.Error("No random tracks found")
                    }
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
