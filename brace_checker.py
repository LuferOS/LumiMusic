import sys

with open("app/src/main/java/com/example/MainActivity.kt", "r") as f:
    lines = f.readlines()

stack = []
for i, line in enumerate(lines):
    # Very naive brace checker (ignores comments/strings, but fine for simple analysis)
    # Let's strip comments for better accuracy
    code = line.split("//")[0]
    for char in code:
        if char == '{':
            stack.append((i + 1, line.strip()))
        elif char == '}':
            if stack:
                stack.pop()
            else:
                print(f"Extra '}}' found at line {i + 1}: {line.strip()}")

if stack:
    print("Unclosed braces:")
    for num, text in stack:
        print(f"Line {num}: {text}")
