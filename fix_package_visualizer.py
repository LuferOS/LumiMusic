with open("app/src/main/java/com/example/ui/components/VisualizerView.kt", "r") as f:
    lines = f.readlines()

new_lines = []
imports = []
for line in lines:
    if line.startswith("import kotlinx.coroutines.launch"):
        imports.append(line)
    else:
        new_lines.append(line)

final_lines = []
for line in new_lines:
    final_lines.append(line)
    if line.startswith("package "):
        final_lines.extend(imports)

with open("app/src/main/java/com/example/ui/components/VisualizerView.kt", "w") as f:
    f.writelines(final_lines)
