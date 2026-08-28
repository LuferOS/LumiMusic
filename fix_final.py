with open('app/src/main/java/com/example/ui/screens/ProfileScreen.kt', 'r') as f:
    lines = f.readlines()

# Remove the last line (the extra `}`)
if lines[-1].strip() == "}":
    lines = lines[:-1]

# Re-add `}` before `Column` at line 75
new_lines = []
for i, line in enumerate(lines):
    if line.strip() == "Column(" and "modifier = Modifier" in lines[i+1] and "fillMaxSize()" in lines[i+2] and "verticalScroll(" in lines[i+3]:
        new_lines.append("        }\n")
    new_lines.append(line)

with open('app/src/main/java/com/example/ui/screens/ProfileScreen.kt', 'w') as f:
    f.writelines(new_lines)

