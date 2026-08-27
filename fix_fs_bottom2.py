with open("app/src/main/java/com/example/ui/components/FullScreenPlayer.kt", "r") as f:
    content = f.read()

target = """            Spacer(modifier = Modifier.height(24.dp))
        }
    }
}
    }
private fun formatTime(ms: Long): String {"""

replacement = """            Spacer(modifier = Modifier.height(24.dp))
        }
    }
}

private fun formatTime(ms: Long): String {"""

content = content.replace(target, replacement)
with open("app/src/main/java/com/example/ui/components/FullScreenPlayer.kt", "w") as f:
    f.write(content)
