with open('app/src/main/java/com/example/ui/screens/ProfileScreen.kt', 'r') as f:
    lines = f.readlines()

new_lines = []
for i, line in enumerate(lines):
    if line.strip() == "}":
        if lines[i-1].strip() == ")" and "confirmButton =" in lines[i-3]:
            new_lines.append(line)
            new_lines.append("}\n")
            continue
        if lines[i-1].strip() == "}" and lines[i-2].strip() == "}":
            # This is around line 468, we remove the extra }
            if "SettingItem" in "".join(lines[i:i+5]):
                continue
    new_lines.append(line)

with open('app/src/main/java/com/example/ui/screens/ProfileScreen.kt', 'w') as f:
    f.writelines(new_lines)
