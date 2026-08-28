with open("app/src/main/java/com/example/ui/screens/ProfileScreen.kt") as f:
    lines = f.readlines()

def check():
    depth = 0
    for i, line in enumerate(lines):
        depth += line.count('{')
        depth -= line.count('}')
        if "fun formatListeningTime" in line:
            print(f"formatListeningTime at line {i+1}, depth = {depth}")

check()
