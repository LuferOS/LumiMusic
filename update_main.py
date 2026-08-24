import re

with open("app/src/main/java/com/example/MainActivity.kt", "r") as f:
    content = f.read()

target = """MyApplicationTheme(
                primaryColorHex = userStats.primaryColorHex,
                fontPref = userStats.fontPreference,
                dynamicColor = false
            ) {
                Surface(
                    modifier = Modifier.fillMaxSize(),
                    color = Color.Black
                ) {"""
replacement = """MyApplicationTheme(
                primaryColorHex = userStats.primaryColorHex,
                fontPref = userStats.fontPreference,
                dynamicColor = false
            ) {
                Surface(
                    modifier = Modifier.fillMaxSize(),
                    color = Color.Black
                ) {
                  androidx.compose.animation.SharedTransitionLayout {"""
content = content.replace(target, replacement)

target_close = """                    }
                }
            }
        }
    }

    private fun checkAndRequestPermissions() {"""
replacement_close = """                    }
                  }
                }
            }
        }
    }

    private fun checkAndRequestPermissions() {"""
content = content.replace(target_close, replacement_close)

with open("app/src/main/java/com/example/MainActivity.kt", "w") as f:
    f.write(content)
