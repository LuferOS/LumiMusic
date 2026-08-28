with open("app/src/main/java/com/example/ui/screens/ProfileScreen.kt") as f:
    s = f.read()
o = s.count('{')
c = s.count('}')
print(f"Open: {o}, Close: {c}")
