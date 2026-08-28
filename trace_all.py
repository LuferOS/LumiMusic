with open("app/src/main/java/com/example/ui/screens/ProfileScreen.kt") as f:
    lines = f.readlines()

depth = 0
for i, line in enumerate(lines):
    import re
    clean_line = re.sub(r'".*?"', '""', line)
    depth += clean_line.count('{')
    depth -= clean_line.count('}')
    if i > 50 and i < 175:
        print(f"L{i+1} D{depth}: {line.strip()}")
