import re

with open("app/src/main/java/com/example/player/PlaybackService.kt", "r") as f:
    content = f.read()

target = """    override fun onDestroy() {
        mediaSession?.run {"""
replacement = """    override fun onDestroy() {
        AudioEffectManager.release()
        mediaSession?.run {"""

content = content.replace(target, replacement)

with open("app/src/main/java/com/example/player/PlaybackService.kt", "w") as f:
    f.write(content)
