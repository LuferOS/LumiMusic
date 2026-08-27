import re
with open("app/src/main/java/com/example/ui/components/MiniPlayer.kt", "r") as f:
    content = f.read()

# Add UserStats import if not present
if "import com.example.data.local.UserStats" not in content:
    content = content.replace("import com.example.viewmodel.MainViewModel", "import com.example.viewmodel.MainViewModel\nimport com.example.data.local.UserStats\nimport com.example.ui.theme.neonGlow")

content = content.replace(
    "viewModel: MainViewModel,\n    sharedTransitionScope",
    "viewModel: MainViewModel,\n    userStats: UserStats,\n    sharedTransitionScope"
)

with open("app/src/main/java/com/example/ui/components/MiniPlayer.kt", "w") as f:
    f.write(content)
