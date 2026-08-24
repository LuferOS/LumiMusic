import re

with open("app/src/main/java/com/example/MainActivity.kt", "r") as f:
    content = f.read()

target = """                  }
                }
            }
        }
    }

    private fun checkAndRequestPermissions() {"""
replacement = """                  }
                }
            }
        }
    }
    }

    private fun checkAndRequestPermissions() {"""
content = content.replace(target, replacement)

with open("app/src/main/java/com/example/MainActivity.kt", "w") as f:
    f.write(content)
