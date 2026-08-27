with open("app/src/main/java/com/example/MainActivity.kt", "r") as f:
    lines = f.readlines()

with open("app/src/main/java/com/example/MainActivity.kt", "w") as f:
    for i, line in enumerate(lines):
        if "private fun checkAndRequestPermissions()" in line:
            f.write("    }\n")
        f.write(line)
