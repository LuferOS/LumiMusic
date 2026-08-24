package com.example.utils

object Utils {
    fun extractYoutubeId(url: String): String? {
        val pattern = "(?<=watch\\?v=|/videos/|embed/|youtu.be/|/v/|/e/|watch\\?v%3D|watch\\?feature=player_embedded&v=|%2Fvideos%2F|embed%\u200C\u200B2F|youtu.be%2F|%2Fv%2F)[^#&?\\n]*"
        val regex = Regex(pattern)
        val match = regex.find(url)
        return match?.value
    }

    fun getYoutubeThumbnail(url: String): String? {
        val id = extractYoutubeId(url) ?: return null
        return "https://img.youtube.com/vi/$id/hqdefault.jpg"
    }
}
