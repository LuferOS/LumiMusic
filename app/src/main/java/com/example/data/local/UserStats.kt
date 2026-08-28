package com.example.data.local

import androidx.room.Entity
import androidx.room.PrimaryKey

@Entity(tableName = "user_stats")
data class UserStats(
    @PrimaryKey val id: Int = 1,
    val totalListeningSeconds: Long = 0,
    val currentStreak: Int = 0,
    val lastListeningDate: Long = 0,
    val totalDownloads: Int = 0,
    val userName: String = "Lumi Listener",
    val apiPreference: String = "Both",
    val primaryColorHex: String = "#1DB954", // Spotify green default for minimalist
    val bgColorHex: String = "#121212", // Minimalist dark
    val fontPreference: String = "Default",
    val neonBorders: Boolean = false, // Disabled by default for minimalist
    val extractAlbumColor: Boolean = true,
    val transitionType: String = "Gapless",
    val transitionDuration: Int = 3,
    val hasSeenOnboarding: Boolean = false,
    val startupTab: Int = 0,
    val navOrder: String = "0,1,2",
    val playerFont: String = "Default",
    val visualizerType: String = "Ondas",
    val visualizerColor: String = "Dinámico",
    val showSpectrums: Boolean = true,
    val batterySaver: Boolean = true
)
