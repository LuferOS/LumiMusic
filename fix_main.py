import re

with open("app/src/main/java/com/example/MainActivity.kt", "r") as f:
    content = f.read()

# Fix double SharedTransitionLayout
content = content.replace("                  androidx.compose.animation.SharedTransitionLayout {\n                  androidx.compose.animation.SharedTransitionLayout {", "                  androidx.compose.animation.SharedTransitionLayout {")

# Fix extra closing braces
target_close = """                    }
                  }
                }
            }
        }
    }

    private fun checkAndRequestPermissions() {"""
replacement_close = """                  }
                }
            }
        }
    }

    private fun checkAndRequestPermissions() {"""
content = content.replace(target_close, replacement_close)

with open("app/src/main/java/com/example/MainActivity.kt", "w") as f:
    f.write(content)
