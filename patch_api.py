import re

with open("app/src/main/java/com/example/data/AlyaCoreApi.kt", "r") as f:
    content = f.read()

lyrics_models = """
@JsonClass(generateAdapter = true)
data class LyricsResponse(
    val status: Boolean,
    val creator: String?,
    val data: List<LyricsData>?
)

@JsonClass(generateAdapter = true)
data class LyricsData(
    val id: Long?,
    val title: String?,
    val artist: String?,
    val album: String?,
    val duration: Long?,
    val lyrics: String?,
    val lrc: String?
)
"""

if "LyricsResponse" not in content:
    content = content.replace("interface AlyaCoreApi", lyrics_models + "\ninterface AlyaCoreApi")

lyrics_endpoint = """
    @GET("tools/lyrics")
    suspend fun searchLyrics(
        @Query("query") query: String,
        @Query("key") key: String = "LumiBot-Alya"
    ): LyricsResponse
"""

if "searchLyrics" not in content:
    content = content.replace("companion object", lyrics_endpoint + "\n    companion object")

with open("app/src/main/java/com/example/data/AlyaCoreApi.kt", "w") as f:
    f.write(content)
