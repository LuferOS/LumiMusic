package com.example.viewmodel

import android.app.Application
import androidx.lifecycle.AndroidViewModel
import androidx.lifecycle.viewModelScope
import com.example.data.local.AppDatabase
import com.example.data.local.UserStats
import kotlinx.coroutines.flow.SharingStarted
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.map
import kotlinx.coroutines.flow.stateIn
import kotlinx.coroutines.launch
import java.util.Calendar

class ProfileViewModel(application: Application) : AndroidViewModel(application) {
    private val dao = AppDatabase.getDatabase(application).userStatsDao()

    val userStats: StateFlow<UserStats> = dao.getStats()
        .map { it ?: UserStats() }
        .stateIn(viewModelScope, SharingStarted.Lazily, UserStats())

    init {
        viewModelScope.launch {
            dao.insertInitial(UserStats())
            checkStreak()
        }
    }

    fun recordListeningTime(seconds: Long) {
        if (seconds <= 0) return
        viewModelScope.launch {
            dao.addListeningTime(seconds)
            updateStreakLogic()
        }
    }

    fun updateAppearance(primary: String, bg: String, font: String, neon: Boolean, extract: Boolean) {
        viewModelScope.launch {
            dao.updateAppearance(primary, bg, font, neon, extract)
        }
    }

    fun updateProfile(name: String, apiPref: String) {
        viewModelScope.launch {
            dao.updateProfile(name, apiPref)
        }
    }

    fun recordDownload() {
        viewModelScope.launch {
            dao.incrementDownloads()
        }
    }

    private suspend fun checkStreak() {
        val currentStats = dao.getStatsDirect() ?: return
        val today = getStartOfDay()
        val yesterday = today - 86400000L // Subtract one day in ms

        val lastDate = currentStats.lastListeningDate
        // If they haven't listened today or yesterday, streak is broken
        if (lastDate != 0L && lastDate < yesterday) {
            dao.updateStreak(0, lastDate) // Reset streak, but keep last date until they listen again
        }
    }

    private suspend fun updateStreakLogic() {
        val today = getStartOfDay()
        val yesterday = today - 86400000L

        val currentStats = dao.getStatsDirect()
        if (currentStats != null) {
            val lastDate = currentStats.lastListeningDate
            if (lastDate == today) {
                // Already counted today
            } else if (lastDate == yesterday) {
                // Consecutive day
                dao.updateStreak(currentStats.currentStreak + 1, today)
            } else {
                // Streak broken or first time
                dao.updateStreak(1, today)
            }
        }
    }

    private fun getStartOfDay(): Long {
        val calendar = Calendar.getInstance()
        calendar.set(Calendar.HOUR_OF_DAY, 0)
        calendar.set(Calendar.MINUTE, 0)
        calendar.set(Calendar.SECOND, 0)
        calendar.set(Calendar.MILLISECOND, 0)
        return calendar.timeInMillis
    }
}
