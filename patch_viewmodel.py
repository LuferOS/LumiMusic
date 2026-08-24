import re

with open("app/src/main/java/com/example/viewmodel/MainViewModel.kt", "r") as f:
    content = f.read()

target = """    private val _downloadState = MutableStateFlow<DownloadState>(DownloadState.Idle)
    val downloadState: StateFlow<DownloadState> = _downloadState"""

replacement = """    private val _downloadState = MutableStateFlow<DownloadState>(DownloadState.Idle)
    val downloadState: StateFlow<DownloadState> = _downloadState

    var remotePlaylist = emptyList<com.example.api.Track>()
    var currentRemoteIndex = -1
    var currentApiPref = "Spotify"

    fun playFromRemotePlaylist(results: List<com.example.api.Track>, index: Int, apiPref: String) {
        remotePlaylist = results
        currentRemoteIndex = index
        currentApiPref = apiPref
        val track = results[index]
        selectTrack(track.trackName ?: "", track.artistName ?: "", apiPref, "play")
    }

    fun playNextRemote(): Boolean {
        if (remotePlaylist.isEmpty() || currentRemoteIndex == -1) return false
        currentRemoteIndex = (currentRemoteIndex + 1) % remotePlaylist.size
        val track = remotePlaylist[currentRemoteIndex]
        selectTrack(track.trackName ?: "", track.artistName ?: "", currentApiPref, "play")
        return true
    }

    fun playPreviousRemote(): Boolean {
        if (remotePlaylist.isEmpty() || currentRemoteIndex == -1) return false
        currentRemoteIndex = if (currentRemoteIndex - 1 < 0) remotePlaylist.size - 1 else currentRemoteIndex - 1
        val track = remotePlaylist[currentRemoteIndex]
        selectTrack(track.trackName ?: "", track.artistName ?: "", currentApiPref, "play")
        return true
    }"""

content = content.replace(target, replacement)

with open("app/src/main/java/com/example/viewmodel/MainViewModel.kt", "w") as f:
    f.write(content)
