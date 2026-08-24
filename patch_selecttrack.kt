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
