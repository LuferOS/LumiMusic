with open("app/src/main/java/com/example/MainActivity.kt", "r") as f:
    content = f.read()

target = """                        if (showEqualizer) {
                            AudioSettingsBottomSheet(controller = mediaController) {
                                showEqualizer = false
                            }
                        }
                  }
                }
            }
        }
    }
    }

    }
    private fun checkAndRequestPermissions() {"""

replacement = """                        if (showEqualizer) {
                            AudioSettingsBottomSheet(controller = mediaController) {
                                showEqualizer = false
                            }
                        }
                    }
                  }
                }
            }
        }
    }

    private fun checkAndRequestPermissions() {"""
    
content = content.replace(target, replacement)
with open("app/src/main/java/com/example/MainActivity.kt", "w") as f:
    f.write(content)
