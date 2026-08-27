with open("app/src/main/java/com/example/ui/components/FullScreenPlayer.kt", "r") as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if "private fun formatTime" in line:
        if lines[i-1].strip() == "}":
            lines.pop(i-1)
        break

with open("app/src/main/java/com/example/ui/components/FullScreenPlayer.kt", "w") as f:
    f.writelines(lines)
