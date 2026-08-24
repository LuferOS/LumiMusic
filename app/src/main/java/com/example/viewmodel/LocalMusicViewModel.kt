package com.example.viewmodel

import android.content.Context
import android.provider.MediaStore
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext

data class LocalAudio(
    val id: Long,
    val title: String,
    val artist: String,
    val uri: String,
    val duration: Long,
    val dateAdded: Long
)

enum class SortOrder {
    TITLE, ARTIST, DATE_ADDED
}

class LocalMusicViewModel : ViewModel() {
    private val _localMusicList = MutableStateFlow<List<LocalAudio>>(emptyList())
    val localMusicList: StateFlow<List<LocalAudio>> = _localMusicList
    
    private val _currentSortOrder = MutableStateFlow(SortOrder.DATE_ADDED)
    val currentSortOrder: StateFlow<SortOrder> = _currentSortOrder

    fun setSortOrder(order: SortOrder, context: Context) {
        _currentSortOrder.value = order
        loadLocalMusic(context)
    }

    fun loadLocalMusic(context: Context) {
        viewModelScope.launch {
            val list = withContext(Dispatchers.IO) {
                val tempList = mutableListOf<LocalAudio>()
                val projection = arrayOf(
                    MediaStore.Audio.Media._ID,
                    MediaStore.Audio.Media.TITLE,
                    MediaStore.Audio.Media.ARTIST,
                    MediaStore.Audio.Media.DATA,
                    MediaStore.Audio.Media.DURATION,
                    MediaStore.Audio.Media.DATE_ADDED
                )
                val selection = "${MediaStore.Audio.Media.IS_MUSIC} != 0"
                
                val sortParam = when (_currentSortOrder.value) {
                    SortOrder.TITLE -> "${MediaStore.Audio.Media.TITLE} ASC"
                    SortOrder.ARTIST -> "${MediaStore.Audio.Media.ARTIST} ASC"
                    SortOrder.DATE_ADDED -> "${MediaStore.Audio.Media.DATE_ADDED} DESC"
                }
                
                context.contentResolver.query(
                    MediaStore.Audio.Media.EXTERNAL_CONTENT_URI,
                    projection,
                    selection,
                    null,
                    sortParam
                )?.use { cursor ->
                    val idColumn = cursor.getColumnIndexOrThrow(MediaStore.Audio.Media._ID)
                    val titleColumn = cursor.getColumnIndexOrThrow(MediaStore.Audio.Media.TITLE)
                    val artistColumn = cursor.getColumnIndexOrThrow(MediaStore.Audio.Media.ARTIST)
                    val dataColumn = cursor.getColumnIndexOrThrow(MediaStore.Audio.Media.DATA)
                    val durationColumn = cursor.getColumnIndexOrThrow(MediaStore.Audio.Media.DURATION)
                    val dateAddedColumn = cursor.getColumnIndexOrThrow(MediaStore.Audio.Media.DATE_ADDED)

                    while (cursor.moveToNext()) {
                        val id = cursor.getLong(idColumn)
                        val title = cursor.getString(titleColumn) ?: "Unknown"
                        val artist = cursor.getString(artistColumn) ?: "Unknown Artist"
                        val duration = cursor.getLong(durationColumn)
                        val dateAdded = cursor.getLong(dateAddedColumn)
                        val uri = android.content.ContentUris.withAppendedId(android.provider.MediaStore.Audio.Media.EXTERNAL_CONTENT_URI, id).toString()
                        tempList.add(LocalAudio(id, title, artist, uri, duration, dateAdded))
                    }
                }
                tempList
            }
            _localMusicList.value = list
        }
    }
}
