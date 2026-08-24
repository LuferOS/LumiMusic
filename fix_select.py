import re

with open("app/src/main/java/com/example/viewmodel/MainViewModel.kt", "r") as f:
    content = f.read()

target = """                var success = false
                // Always try YouTube first, as it usually has the most reliable audio sources
                try {
                    val ytRes = api.searchYouTube(query = fullQuery)
                    if (ytRes.status && ytRes.data?.downloadUrl != null) {
                        _downloadState.value = DownloadState.Success(
                            title = ytRes.data.title ?: trackName,
                            url = ytRes.data.downloadUrl,
                            thumbnail = ytRes.data.thumbnail,
                            action = action
                        )
                        success = true
                    }
                } catch (e: Exception) {
                    // ignore
                }
                
                // If YouTube fails, try Spotify
                if (!success) {
                    try {
                        val spotRes = api.searchSpotify(query = fullQuery)
                        if (spotRes.status && spotRes.data?.downloadUrl != null) {
                            _downloadState.value = DownloadState.Success(
                                title = spotRes.data.title ?: trackName,
                                url = spotRes.data.downloadUrl,
                                thumbnail = spotRes.data.cover,
                                action = action
                            )
                            success = true
                        }
                    } catch (e: Exception) {
                        // ignore
                    }
                }"""

replacement = """                var success = false
                
                suspend fun tryYouTube(): Boolean {
                    try {
                        val ytRes = api.searchYouTube(query = fullQuery)
                        if (ytRes.status && ytRes.data?.downloadUrl != null) {
                            _downloadState.value = DownloadState.Success(
                                title = ytRes.data.title ?: trackName,
                                url = ytRes.data.downloadUrl,
                                thumbnail = ytRes.data.thumbnail,
                                action = action
                            )
                            return true
                        }
                    } catch (e: Exception) {}
                    return false
                }
                
                suspend fun trySpotify(): Boolean {
                    try {
                        val spotRes = api.searchSpotify(query = fullQuery)
                        if (spotRes.status && spotRes.data?.downloadUrl != null) {
                            _downloadState.value = DownloadState.Success(
                                title = spotRes.data.title ?: trackName,
                                url = spotRes.data.downloadUrl,
                                thumbnail = spotRes.data.cover,
                                action = action
                            )
                            return true
                        }
                    } catch (e: Exception) {}
                    return false
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
                }"""

content = content.replace(target, replacement)

with open("app/src/main/java/com/example/viewmodel/MainViewModel.kt", "w") as f:
    f.write(content)
