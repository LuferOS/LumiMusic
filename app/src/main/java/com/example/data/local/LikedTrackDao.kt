package com.example.data.local

import androidx.room.Dao
import androidx.room.Delete
import androidx.room.Insert
import androidx.room.OnConflictStrategy
import androidx.room.Query
import kotlinx.coroutines.flow.Flow

@Dao
interface LikedTrackDao {
    @Query("SELECT * FROM liked_tracks ORDER BY addedAt DESC")
    fun getAllLikedTracks(): Flow<List<LikedTrack>>

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insertLikedTrack(track: LikedTrack)

    @Delete
    suspend fun deleteLikedTrack(track: LikedTrack)

    @Query("DELETE FROM liked_tracks WHERE uri = :uri")
    suspend fun deleteByUri(uri: String)

    @Query("SELECT EXISTS(SELECT 1 FROM liked_tracks WHERE uri = :uri LIMIT 1)")
    fun isLiked(uri: String): Flow<Boolean>
}
