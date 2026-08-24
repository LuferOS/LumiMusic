package com.example.data

import retrofit2.http.GET
import retrofit2.http.Query
import retrofit2.Retrofit
import retrofit2.converter.moshi.MoshiConverterFactory
import com.squareup.moshi.JsonClass
import com.squareup.moshi.Json

@JsonClass(generateAdapter = true)
data class AudioResponse(
    val status: Boolean,
    val creator: String?,
    val data: AudioData?
)

@JsonClass(generateAdapter = true)
data class AudioData(
    val title: String?,
    val author: String?,
    val thumbnail: String?,
    @Json(name = "dl") val downloadUrl: String?
)

@JsonClass(generateAdapter = true)
data class SpotifyResponse(
    val status: Boolean,
    val data: SpotifyData?
)

@JsonClass(generateAdapter = true)
data class SpotifyData(
    val title: String?,
    val artist: String?,
    val cover: String?,
    @Json(name = "dl") val downloadUrl: String?
)

interface AlyaCoreApi {
    @GET("dl/spotifyplay")
    suspend fun searchSpotify(
        @Query("query") query: String,
        @Query("key") key: String = "LumiBot-alya"
    ): SpotifyResponse
    
    @GET("dl/youtubeplayv2")
    suspend fun searchYouTube(
        @Query("query") query: String,
        @Query("type") type: String = "mp3",
        @Query("quality") quality: String = "auto",
        @Query("key") key: String = "LumiBot-alya"
    ): AudioResponse

    companion object {
        const val BASE_URL = "https://api.alyacore.xyz/"
        fun create(): AlyaCoreApi {
            val retrofit = Retrofit.Builder()
                .baseUrl(BASE_URL)
                .addConverterFactory(MoshiConverterFactory.create())
                .build()
            return retrofit.create(AlyaCoreApi::class.java)
        }
    }
}
