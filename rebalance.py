with open("app/src/main/java/com/example/MainActivity.kt", "r") as f:
    content = f.read()

parts = content.split("private fun checkAndRequestPermissions()")

# We want exactly 1 `}` before private fun checkAndRequestPermissions() that closes onCreate.
# Wait, let's just count open and close braces in parts[0]
opened = parts[0].count("{")
closed = parts[0].count("}")

print(f"Opened: {opened}, Closed: {closed}")
