import re

with open('app/src/main/java/com/example/viewmodel/MainViewModel.kt', 'r') as f:
    content = f.read()

# Replace the CompletableDeferred blocks with select expressions

# 1. searchITunes block
old_search_block = """                    val deferredResult = kotlinx.coroutines.CompletableDeferred<ITunesTrack?>()
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
                    
                    val fallbackTrack = deferredResult.await()"""

new_search_block = """                    // Fast-path racing: return the first successful result and cancel the slower one.
                    val fallbackTrack = kotlinx.coroutines.selects.select<ITunesTrack?> {
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

content = content.replace(old_search_block, new_search_block)

# 2. selectTrack block
old_select_block = """                    val deferredResult = kotlinx.coroutines.CompletableDeferred<DownloadState.Success?>()
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
                    finalState = deferredResult.await()"""

new_select_block = """                    // Fast-path racing: return the first successful result and cancel the slower one.
                    finalState = kotlinx.coroutines.selects.select<DownloadState.Success?> {
                        val ytJob = async(Dispatchers.IO) { fetchYouTube() }
                        val spotJob = async(Dispatchers.IO) { fetchSpotify() }
                        
                        ytJob.onAwait { res -> 
                            if (res != null) { spotJob.cancel(); res } 
                            else spotJob.await() 
                        }
                        spotJob.onAwait { res -> 
                            if (res != null) { ytJob.cancel(); res } 
                            else ytJob.await() 
                        }
                    }"""

content = content.replace(old_select_block, new_select_block)

with open('app/src/main/java/com/example/viewmodel/MainViewModel.kt', 'w') as f:
    f.write(content)
