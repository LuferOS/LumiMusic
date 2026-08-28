import re

with open('app/src/main/java/com/example/viewmodel/MainViewModel.kt', 'r') as f:
    content = f.read()

# We need to find the exact block for the fallback in searchITunes.
# "                    val deferredResult = kotlinx.coroutines.CompletableDeferred<ITunesTrack?>()"
# down to "                    val fallbackResult = deferredResult.await()"

old_racing_search = """                    val deferredResult = kotlinx.coroutines.CompletableDeferred<ITunesTrack?>()
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
                        } catch (e: Exception) { if (fails.incrementAndGet() == 2) deferredResult.complete(null) }
                    }
                    
                    val fallbackResult = deferredResult.await()"""

new_racing_search = """                    // Fast-path racing: return the first successful result and cancel the slower one.
                    val fallbackResult = kotlinx.coroutines.selects.select<ITunesTrack?> {
                        val ytJob = async(Dispatchers.IO) {
                            try {
                                val ytRes = api.searchYouTube(query = query)
                                if (ytRes.status && ytRes.data != null) {
                                    return@async ITunesTrack(
                                        trackName = ytRes.data.title ?: query,
                                        artistName = ytRes.data.author ?: "YouTube",
                                        artworkUrl100 = ytRes.data.thumbnail
                                    )
                                }
                            } catch (e: Exception) {}
                            null
                        }
                        
                        val spotJob = async(Dispatchers.IO) {
                            try {
                                val spotRes = api.searchSpotify(query = query)
                                if (spotRes.status && spotRes.data != null) {
                                    return@async ITunesTrack(
                                        trackName = spotRes.data.title ?: query,
                                        artistName = spotRes.data.artist ?: "Spotify",
                                        artworkUrl100 = spotRes.data.cover
                                    )
                                }
                            } catch (e: Exception) {}
                            null
                        }
                        
                        ytJob.onAwait { res -> 
                            if (res != null) { spotJob.cancel(); res } 
                            else spotJob.await() 
                        }
                        spotJob.onAwait { res -> 
                            if (res != null) { ytJob.cancel(); res } 
                            else ytJob.await() 
                        }
                    }"""

if old_racing_search in content:
    content = content.replace(old_racing_search, new_racing_search)
else:
    print("WARNING: Could not find old_racing_search block.")

with open('app/src/main/java/com/example/viewmodel/MainViewModel.kt', 'w') as f:
    f.write(content)
