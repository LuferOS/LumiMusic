with open("app/src/main/java/com/example/viewmodel/MainViewModel.kt", "r") as f:
    content = f.read()

target = """    private val likedTrackDao = AppDatabase.getDatabase(application).likedTrackDao()
    
    val likedTracks = likedTrackDao.getAllLikedTracks()
        .stateIn(viewModelScope, SharingStarted.Lazily, emptyList())"""

new_code = """    private val likedTrackDao = AppDatabase.getDatabase(application).likedTrackDao()
    
    val likedTracks = likedTrackDao.getAllLikedTracks()
        .stateIn(viewModelScope, SharingStarted.Lazily, emptyList())

    private val _updateInfo = MutableStateFlow(UpdateInfo())
    val updateInfo: StateFlow<UpdateInfo> = _updateInfo

    init {
        checkForUpdates()
    }

    private fun isNewerVersion(latest: String, current: String): Boolean {
        val lParts = latest.split(".").mapNotNull { it.toIntOrNull() }
        val cParts = current.split(".").mapNotNull { it.toIntOrNull() }
        val maxLength = maxOf(lParts.size, cParts.size)
        for (i in 0 until maxLength) {
            val l = lParts.getOrElse(i) { 0 }
            val c = cParts.getOrElse(i) { 0 }
            if (l > c) return true
            if (l < c) return false
        }
        return false
    }

    fun checkForUpdates() {
        viewModelScope.launch(Dispatchers.IO) {
            try {
                val owner = "luisfernandoguzmannino" 
                val repo = "LumiMusic" 
                
                val release = com.example.data.GitHubApi.service.getLatestRelease(owner, repo)
                val currentVersionName = com.example.BuildConfig.VERSION_NAME
                
                val latestVersion = release.tagName.removePrefix("v").removePrefix("V")
                val currentVersion = currentVersionName.removePrefix("v").removePrefix("V")
                
                if (isNewerVersion(latestVersion, currentVersion)) {
                    _updateInfo.value = UpdateInfo(
                        isAvailable = true,
                        newVersion = release.tagName,
                        updateUrl = release.htmlUrl,
                        releaseNotes = release.body ?: "Nueva versión detectada"
                    )
                }
            } catch (e: Exception) {
                e.printStackTrace()
            }
        }
    }"""

if target in content:
    content = content.replace(target, new_code)
else:
    print("TARGET NOT FOUND. Trying regex...")
    import re
    content = re.sub(r'val likedTracks.*?emptyList\(\)\)', new_code.replace("    private val likedTrackDao = AppDatabase.getDatabase(application).likedTrackDao()\n    \n", ""), content, flags=re.DOTALL)

with open("app/src/main/java/com/example/viewmodel/MainViewModel.kt", "w") as f:
    f.write(content)
