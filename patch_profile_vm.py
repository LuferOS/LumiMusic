import re

with open("app/src/main/java/com/example/viewmodel/ProfileViewModel.kt", "r") as f:
    content = f.read()

func = """    fun updateTransitions(type: String, duration: Int) {
        viewModelScope.launch {
            dao.updateTransitions(type, duration)
        }
    }"""

if "updateTransitions" not in content:
    content = content.replace("    fun recordDownload() {", func + "\n\n    fun recordDownload() {")

with open("app/src/main/java/com/example/viewmodel/ProfileViewModel.kt", "w") as f:
    f.write(content)
