with open('app/src/main/java/com/example/ui/screens/ProfileScreen.kt', 'r') as f:
    lines = f.readlines()

new_lines = []
skip = False
for line in lines:
    if "Row(" in line and "modifier = Modifier" in ''.join(lines):
        pass # this is just an idea
