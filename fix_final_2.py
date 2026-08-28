with open('app/src/main/java/com/example/ui/screens/ProfileScreen.kt', 'r') as f:
    lines = f.readlines()

new_lines = []
for i, line in enumerate(lines):
    if line.strip() == "}":
        if i > 400 and i < 410 and lines[i+1].strip() == "}":
            continue
    new_lines.append(line)

with open('app/src/main/java/com/example/ui/screens/ProfileScreen.kt', 'w') as f:
    f.writelines(new_lines)
