with open("app/src/main/java/com/example/ui/components/CustomizationDialog.kt", "r") as f:
    lines = f.readlines()

new_lines = ["package com.example.ui.components\n"]
for line in lines:
    if line.startswith("package"):
        continue
    new_lines.append(line)

with open("app/src/main/java/com/example/ui/components/CustomizationDialog.kt", "w") as f:
    f.writelines(new_lines)
