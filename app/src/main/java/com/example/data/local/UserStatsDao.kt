package com.example.data.local

import androidx.room.Dao
import androidx.room.Insert
import androidx.room.OnConflictStrategy
import androidx.room.Query
import kotlinx.coroutines.flow.Flow

@Dao
interface UserStatsDao {
    @Query("SELECT * FROM user_stats WHERE id = 1")
    fun getStats(): Flow<UserStats?>

    @Query("SELECT * FROM user_stats WHERE id = 1")
    suspend fun getStatsDirect(): UserStats?

    @Insert(onConflict = OnConflictStrategy.IGNORE)
    suspend fun insertInitial(stats: UserStats)

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insert(stats: UserStats)

    @Query("UPDATE user_stats SET totalListeningSeconds = totalListeningSeconds + :seconds WHERE id = 1")
    suspend fun addListeningTime(seconds: Long)

    @Query("UPDATE user_stats SET currentStreak = :streak, lastListeningDate = :date WHERE id = 1")
    suspend fun updateStreak(streak: Int, date: Long)
    
    @Query("UPDATE user_stats SET totalDownloads = totalDownloads + 1 WHERE id = 1")
    suspend fun incrementDownloads()
    
    @Query("UPDATE user_stats SET userName = :name, apiPreference = :apiPref WHERE id = 1")
    suspend fun updateProfile(name: String, apiPref: String)

    @Query("UPDATE user_stats SET primaryColorHex = :primary, bgColorHex = :bg, fontPreference = :font, neonBorders = :neon, extractAlbumColor = :extract WHERE id = 1")
    suspend fun updateAppearance(primary: String, bg: String, font: String, neon: Boolean, extract: Boolean)

    @Query("UPDATE user_stats SET transitionType = :type, transitionDuration = :duration WHERE id = 1")
    suspend fun updateTransitions(type: String, duration: Int)

    @Query("UPDATE user_stats SET hasSeenOnboarding = :seen WHERE id = 1")
    suspend fun updateOnboardingStatus(seen: Boolean)

    @Query("UPDATE user_stats SET startupTab = :tab, navOrder = :order, playerFont = :font, visualizerType = :vType, visualizerColor = :vColor WHERE id = 1")
    suspend fun updateCustomization(tab: Int, order: String, font: String, vType: String, vColor: String)

    @Query("UPDATE user_stats SET showSpectrums = :show WHERE id = 1")
    suspend fun updateShowSpectrums(show: Boolean)
    
    @Query("UPDATE user_stats SET batterySaver = :enabled WHERE id = 1")
    suspend fun updateBatterySaver(enabled: Boolean)
}
