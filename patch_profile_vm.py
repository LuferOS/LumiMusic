import re

with open("app/src/main/java/com/example/viewmodel/ProfileViewModel.kt", "r") as f:
    content = f.read()

if "fun completeOnboarding" not in content:
    additions = """
    fun completeOnboarding() {
        viewModelScope.launch {
            dao.updateOnboardingStatus(true)
        }
    }
    
    fun clearCache(context: android.content.Context) {
        viewModelScope.launch(Dispatchers.IO) {
            try {
                val cacheDir = java.io.File(context.cacheDir, "media_cache")
                if (cacheDir.exists()) {
                    cacheDir.deleteRecursively()
                }
            } catch (e: Exception) {
                e.printStackTrace()
            }
        }
    }
"""
    content = content.replace("fun updateTransitions(type: String, duration: Int) {", additions + "\n    fun updateTransitions(type: String, duration: Int) {")
    with open("app/src/main/java/com/example/viewmodel/ProfileViewModel.kt", "w") as f:
        f.write(content)
