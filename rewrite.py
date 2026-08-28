with open('app/src/main/java/com/example/ui/screens/ProfileScreen.kt', 'r') as f:
    lines = f.readlines()

new_lines = []
for i, line in enumerate(lines):
    new_lines.append(line)
    
    # After line 402 `}`, we need to close ProfileScreen:
    if line.strip() == "}" and lines[i-1].strip() == ")" and "confirmButton =" in lines[i-3]:
        new_lines.append("}\n\n")

# Wait, the end of the file is currently depth 2 missing 2 closing braces!
# We just need to append them.
new_lines.append("}\n")
new_lines.append("}\n")

with open('app/src/main/java/com/example/ui/screens/ProfileScreen.kt', 'w') as f:
    f.writelines(new_lines)

