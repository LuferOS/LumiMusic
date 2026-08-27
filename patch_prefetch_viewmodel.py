with open("app/src/main/java/com/example/viewmodel/MainViewModel.kt", "r") as f:
    content = f.read()

target = """                    viewModelScope.launch(Dispatchers.IO) {
                        try {
                            val resolvedUrl = AlyaCoreApi.resolveTrackUrl(first.trackName ?: "", first.artistName ?: "", currentApiPref)
                            if (resolvedUrl.isNotEmpty()) {
                                com.example.player.PrefetchManager.prefetchUrl(getApplication<android.app.Application>(), resolvedUrl)
                            }
                        } catch(e: Exception) {
                            e.printStackTrace()
                        }
                    }"""

replacement = """                    viewModelScope.launch(Dispatchers.IO) {
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
                    }"""

content = content.replace(target, replacement)
with open("app/src/main/java/com/example/viewmodel/MainViewModel.kt", "w") as f:
    f.write(content)
