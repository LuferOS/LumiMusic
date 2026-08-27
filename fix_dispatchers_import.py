with open("app/src/main/java/com/example/viewmodel/ProfileViewModel.kt", "r") as f:
    content = f.read()

if "import kotlinx.coroutines.Dispatchers" not in content:
    content = content.replace("import kotlinx.coroutines.launch", "import kotlinx.coroutines.launch\nimport kotlinx.coroutines.Dispatchers")
    with open("app/src/main/java/com/example/viewmodel/ProfileViewModel.kt", "w") as f:
        f.write(content)
