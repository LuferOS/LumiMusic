package com.example.data

import retrofit2.http.GET
import retrofit2.http.Query
import retrofit2.Retrofit
import retrofit2.converter.moshi.MoshiConverterFactory
import com.squareup.moshi.JsonClass
import com.squareup.moshi.Json

@JsonClass(generateAdapter = true)
data class ITunesResponse(
    val resultCount: Int,
    val results: List<ITunesTrack>
)

@JsonClass(generateAdapter = true)
data class ITunesTrack(
    val trackName: String?,
    val artistName: String?,
    val artworkUrl100: String?
)

interface ITunesApi {
    @GET("search")
    suspend fun searchTracks(
        @Query("term") term: String,
        @Query("media") media: String = "music",
        @Query("limit") limit: Int = 10
    ): ITunesResponse

    companion object {
        const val BASE_URL = "https://itunes.apple.com/"
        private var instance: ITunesApi? = null
        
        fun create(): ITunesApi {
            if (instance == null) {
                val retrofit = Retrofit.Builder()
                    .baseUrl(BASE_URL)
                    .client(NetworkClient.sharedClient)
                    .addConverterFactory(MoshiConverterFactory.create())
                    .build()
                instance = retrofit.create(ITunesApi::class.java)
            }
            return instance!!
        }
    }
}
