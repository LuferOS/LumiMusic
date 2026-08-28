with open('app/src/main/java/com/example/ui/screens/ProfileScreen.kt', 'r') as f:
    lines = f.readlines()

new_lines = []
for i, line in enumerate(lines):
    if line.strip() == "@Composable" and "fun formatListeningTime" in lines[i+1]:
        new_lines.append("}\n\n")
    new_lines.append(line)

with open('app/src/main/java/com/example/ui/screens/ProfileScreen.kt', 'w') as f:
    f.writelines(new_lines)

