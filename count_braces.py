with open("app/src/main/java/com/example/ui/components/FullScreenPlayer.kt", "r") as f:
    content = f.read()

opened = content.count("{")
closed = content.count("}")

print(f"Opened: {opened}, Closed: {closed}")
