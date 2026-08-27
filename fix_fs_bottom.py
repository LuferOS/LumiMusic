with open("app/src/main/java/com/example/ui/components/FullScreenPlayer.kt", "r") as f:
    lines = f.readlines()

# Remove the last line if it's "    }\n"
if lines[-1].strip() == "}":
    lines = lines[:-1]

# Find the end of the FullScreenPlayer function.
# FullScreenPlayer function ends just before `private fun formatTime`
for i, line in enumerate(lines):
    if "private fun formatTime" in line:
        # Insert "    }\n" before this line
        lines.insert(i, "    }\n")
        break

with open("app/src/main/java/com/example/ui/components/FullScreenPlayer.kt", "w") as f:
    f.writelines(lines)
