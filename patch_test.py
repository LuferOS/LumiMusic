with open("app/src/test/java/com/example/ExampleRobolectricTest.kt", "r") as f:
    content = f.read()
content = content.replace('"My Application"', '"LumiMusic"')
with open("app/src/test/java/com/example/ExampleRobolectricTest.kt", "w") as f:
    f.write(content)
