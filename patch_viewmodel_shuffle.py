import re

with open("app/src/main/java/com/example/viewmodel/MainViewModel.kt", "r") as f:
    content = f.read()

target = """    fun playNextRemote(): Boolean {
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

replacement = """    fun playNextRemote(isShuffle: Boolean = false, repeatMode: Int = 0): Boolean {
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
    }"""

content = content.replace(target, replacement)

with open("app/src/main/java/com/example/viewmodel/MainViewModel.kt", "w") as f:
    f.write(content)
