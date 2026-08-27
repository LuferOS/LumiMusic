with open("app/src/main/java/com/example/MainActivity.kt", "r") as f:
    content = f.read()

start_idx = content.find("        setContent {")
end_idx = content.find("    private fun checkAndRequestPermissions()")
print(content[start_idx:end_idx])
