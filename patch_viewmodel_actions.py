import re

with open("app/src/main/java/com/example/viewmodel/MainViewModel.kt", "r") as f:
    content = f.read()

# We need to change selectTrack to handle playback vs download states.
# Actually, returning the URL would be easier, but ViewModel runs async.
# Let's add an action parameter to selectTrack: `action: String = "play"`

old_select = """    fun selectTrack(trackName: String, artistName: String, apiPref: String) {"""
new_select = """    fun selectTrack(trackName: String, artistName: String, apiPref: String, action: String = "play") {"""
content = content.replace(old_select, new_select)

old_success = """                            _downloadState.value = DownloadState.Success(
                                title = spotRes.data.title ?: trackName,
                                url = spotRes.data.downloadUrl,
                                thumbnail = spotRes.data.cover
                            )
                            success = true"""
new_success = """                            _downloadState.value = DownloadState.Success(
                                title = spotRes.data.title ?: trackName,
                                url = spotRes.data.downloadUrl,
                                thumbnail = spotRes.data.cover
                            )
                            if (action == "play") {
                                // We will let the UI handle it, but maybe pass action somehow?
                            }
                            success = true"""

# Instead of changing selectTrack's internal logic, let's just make `DownloadState.Success` include the action!
