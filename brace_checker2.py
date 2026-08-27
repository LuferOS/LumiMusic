import sys

with open("app/src/main/java/com/example/MainActivity.kt", "r") as f:
    lines = f.readlines()

stack = []
for i, line in enumerate(lines):
    if i == 323: # Before checkAndRequestPermissions
        print("Stack before line 324:")
        for num, text in stack:
            print(f"Line {num}: {text}")
        break

    code = line.split("//")[0]
    for char in code:
        if char == '{':
            stack.append((i + 1, line.strip()))
        elif char == '}':
            if stack:
                stack.pop()
