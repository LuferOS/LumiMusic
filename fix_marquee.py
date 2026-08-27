import os

files_to_fix = [
    "app/src/main/java/com/example/MainActivity.kt",
    "app/src/main/java/com/example/ui/components/FullScreenPlayer.kt",
    "app/src/main/java/com/example/ui/components/MiniPlayer.kt",
    "app/src/main/java/com/example/ui/screens/LocalMusicScreen.kt"
]

for filepath in files_to_fix:
    with open(filepath, "r") as f:
        content = f.read()
    
    # Replace Modifier.androidx.compose.foundation.basicMarquee() with Modifier.basicMarquee()
    content = content.replace("Modifier.androidx.compose.foundation.basicMarquee()", "Modifier.basicMarquee()")
    
    # Add import if missing
    if "import androidx.compose.foundation.basicMarquee" not in content:
        content = content.replace("import androidx.compose.ui.Modifier", "import androidx.compose.ui.Modifier\nimport androidx.compose.foundation.basicMarquee")
        
    with open(filepath, "w") as f:
        f.write(content)

