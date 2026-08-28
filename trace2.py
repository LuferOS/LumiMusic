with open("app/src/main/java/com/example/ui/screens/ProfileScreen.kt") as f:
    lines = f.readlines()

depth = 0
for i, line in enumerate(lines):
    # poor man's string removal so we don't count braces inside strings
    import re
    clean_line = re.sub(r'".*?"', '""', line)
    depth += clean_line.count('{')
    depth -= clean_line.count('}')
    
    if i > 390 and i < 415:
        print(f"Line {i+1} depth: {depth}: {line.strip()}")
