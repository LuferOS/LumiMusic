with open("app/src/main/java/com/example/ui/components/FullScreenPlayer.kt", "r") as f:
    lines = f.readlines()

# Remove the `}` at the very end if it is there
if lines[-1].strip() == "}":
    lines = lines[:-1]

# Make sure we have 4 closing braces before `formatTime`
for i, line in enumerate(lines):
    if "private fun formatTime" in line:
        # Check previous lines to see how many closing braces we have.
        # Let's just insert one more `}` before it.
        lines.insert(i, "}\n")
        break

with open("app/src/main/java/com/example/ui/components/FullScreenPlayer.kt", "w") as f:
    f.writelines(lines)

