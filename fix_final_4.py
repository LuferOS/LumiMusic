with open('app/src/main/java/com/example/ui/screens/ProfileScreen.kt', 'r') as f:
    lines = f.readlines()

new_lines = []
for i, line in enumerate(lines):
    if line.strip() == "}" and lines[i+1].strip() == "@Composable" and "fun SettingItem" in lines[i+2]:
        continue
    new_lines.append(line)

with open('app/src/main/java/com/example/ui/screens/ProfileScreen.kt', 'w') as f:
    f.writelines(new_lines)
