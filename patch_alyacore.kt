import com.squareup.moshi.Json

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
