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
    val primaryColorHex: String = "#00FFFF", // Cyan neon default
    val bgColorHex: String = "#000000", // AMOLED black default
    val fontPreference: String = "Default",
    val neonBorders: Boolean = true,
    val extractAlbumColor: Boolean = true,
    val transitionType: String = "Gapless",
    val transitionDuration: Int = 3
)
