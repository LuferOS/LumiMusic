with open("app/src/main/java/com/example/player/PrefetchManager.kt", "r") as f:
    content = f.read()

target = """                val cache = PlaybackService.getCache(context)
                val dataSource = DefaultHttpDataSource.Factory().createDataSource()
                val dataSpec = DataSpec(Uri.parse(url))
                
                val cacheWriter = CacheWriter(
                    cache,
                    dataSpec,
                    ByteArray(256 * 1024),
                    CacheWriter.ProgressListener { requestLength, bytesCached, newBytesCached -> 
                        // Progress ignored
                    }
                )"""

replacement = """                val cache = PlaybackService.getCache(context)
                val httpDataSourceFactory = DefaultHttpDataSource.Factory().setAllowCrossProtocolRedirects(true)
                val cacheDataSourceFactory = androidx.media3.datasource.cache.CacheDataSource.Factory()
                    .setCache(cache)
                    .setUpstreamDataSourceFactory(httpDataSourceFactory)
                    .setFlags(androidx.media3.datasource.cache.CacheDataSource.FLAG_IGNORE_CACHE_ON_ERROR)
                
                val dataSource = cacheDataSourceFactory.createDataSource()
                val dataSpec = DataSpec(Uri.parse(url))
                
                val cacheWriter = CacheWriter(
                    dataSource,
                    dataSpec,
                    ByteArray(256 * 1024),
                    CacheWriter.ProgressListener { requestLength, bytesCached, newBytesCached -> 
                        // Progress ignored
                    }
                )"""

content = content.replace(target, replacement)
with open("app/src/main/java/com/example/player/PrefetchManager.kt", "w") as f:
    f.write(content)
