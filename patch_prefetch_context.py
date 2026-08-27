with open("app/src/main/java/com/example/viewmodel/MainViewModel.kt", "r") as f:
    content = f.read()

content = content.replace(
    "com.example.player.PrefetchManager.prefetchUrl(appContext, resolvedUrl)",
    "com.example.player.PrefetchManager.prefetchUrl(getApplication<android.app.Application>(), resolvedUrl)"
)

with open("app/src/main/java/com/example/viewmodel/MainViewModel.kt", "w") as f:
    f.write(content)
