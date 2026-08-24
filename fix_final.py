with open("app/src/main/java/com/example/MainActivity.kt", "r") as f:
    lines = f.readlines()

# Find class MainActivity : ComponentActivity() {
start_class = -1
for i, l in enumerate(lines):
    if "class MainActivity : ComponentActivity() {" in l:
        start_class = i
        break

# Find @OptIn(ExperimentalMaterial3Api::class)
start_main_screen = -1
for i, l in enumerate(lines):
    if "@OptIn(ExperimentalMaterial3Api::class)" in l:
        start_main_screen = i
        break

# Extract the class body
class_lines = lines[start_class:start_main_screen]

# Remove extra } at the end of class_lines if it has too many
# Actually, let's just assemble it properly.

new_lines = lines[:start_class] + class_lines

# Remove any onDestroy in the class_lines
# Let's just find and remove onDestroy wherever it is in the whole file
clean_lines = []
skip = False
for l in lines:
    if "override fun onDestroy()" in l:
        skip = True
    if skip and "}" in l and l.startswith("    }"):
        skip = False
        continue
    if skip and l.startswith("}"):
        skip = False
        continue
    if not skip:
        clean_lines.append(l)

# Re-evaluate start_main_screen
start_main_screen = -1
for i, l in enumerate(clean_lines):
    if "@OptIn(ExperimentalMaterial3Api::class)" in l:
        start_main_screen = i
        break

# The class MainActivity ends before start_main_screen. We need to make sure it is closed properly and has onDestroy.
class_content = clean_lines[:start_main_screen]

# Remove trailing closing braces that might be extra
while class_content[-1].strip() == "}":
    class_content.pop()

destroy_code = """
    override fun onDestroy() {
        super.onDestroy()
        controllerFuture?.let { androidx.media3.session.MediaController.releaseFuture(it) }
    }
}
"""
class_content.append(destroy_code)

final_lines = class_content + clean_lines[start_main_screen:]

# Ensure MainScreen ends properly. It should just end with a }
while final_lines[-1].strip() == "}" and final_lines[-2].strip() == "}":
    final_lines.pop()

with open("app/src/main/java/com/example/MainActivity.kt", "w") as f:
    f.writelines(final_lines)
