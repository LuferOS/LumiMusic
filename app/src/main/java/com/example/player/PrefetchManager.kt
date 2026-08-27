package com.example.player

import android.content.Context
import androidx.media3.datasource.DataSpec
import androidx.media3.datasource.DefaultHttpDataSource
import androidx.media3.datasource.cache.CacheWriter
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext
import android.net.Uri

object PrefetchManager {
    suspend fun prefetchUrl(context: Context, url: String) {
        withContext(Dispatchers.IO) {
            try {
                val cache = PlaybackService.getCache(context)
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
                )
                
                cacheWriter.cache()
            } catch (e: Exception) {
                e.printStackTrace()
            }
        }
    }
}
