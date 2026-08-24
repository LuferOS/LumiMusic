package com.example.data.local

import androidx.room.Entity
import androidx.room.PrimaryKey

@Entity(tableName = "liked_tracks")
data class LikedTrack(
    @PrimaryKey
    val uri: String, // Can be local URI or remote URL
    val title: String,
    val artist: String,
    val artworkUrl: String?,
    val addedAt: Long = System.currentTimeMillis()
)
