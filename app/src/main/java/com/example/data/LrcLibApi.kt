package com.example.data

import retrofit2.http.GET
import retrofit2.http.Query
import retrofit2.Retrofit
import retrofit2.converter.moshi.MoshiConverterFactory
import com.squareup.moshi.JsonClass

@JsonClass(generateAdapter = true)
data class LrcLibTrack(
    val id: Long,
    val trackName: String,
    val artistName: String,
    val plainLyrics: String?,
    val syncedLyrics: String?
)

interface LrcLibApi {
    @GET("api/search")
    suspend fun searchLyrics(
        @Query("track_name") trackName: String,
        @Query("artist_name") artistName: String = ""
    ): List<LrcLibTrack>

    companion object {
        const val BASE_URL = "https://lrclib.net/"
        private var instance: LrcLibApi? = null
        
        fun create(): LrcLibApi {
            if (instance == null) {
                val retrofit = Retrofit.Builder()
                    .baseUrl(BASE_URL)
                    .client(NetworkClient.sharedClient)
                    .addConverterFactory(MoshiConverterFactory.create())
                    .build()
                instance = retrofit.create(LrcLibApi::class.java)
            }
            return instance!!
        }
    }
}
