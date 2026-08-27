with open("app/src/main/java/com/example/viewmodel/ProfileViewModel.kt", "r") as f:
    content = f.read()

additions = """
    fun updateCustomization(tab: Int, order: String, font: String, vType: String, vColor: String) {
        viewModelScope.launch {
            dao.updateCustomization(tab, order, font, vType, vColor)
        }
    }
"""

if "updateCustomization" not in content:
    content = content.replace("fun clearCache(context: android.content.Context) {", additions + "\n    fun clearCache(context: android.content.Context) {")
    with open("app/src/main/java/com/example/viewmodel/ProfileViewModel.kt", "w") as f:
        f.write(content)
