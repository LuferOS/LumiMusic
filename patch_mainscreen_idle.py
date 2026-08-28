import re

with open('app/src/main/java/com/example/ui/screens/MainScreen.kt', 'r') as f:
    content = f.read()

# Replace quotes
content = re.sub(
    r'val loadingQuote = remember.*?\}\.random\(\)\n\s*\}',
    'val loadingQuote = "Cargando..."',
    content,
    flags=re.DOTALL
)

# Replace idle state text
content = re.sub(
    r'"Alya Core.*?"',
    '"Cargando..."',
    content,
    flags=re.DOTALL
)

with open('app/src/main/java/com/example/ui/screens/MainScreen.kt', 'w') as f:
    f.write(content)
