import re

def update_file(filepath):
    with open(filepath, 'r') as f:
        content = f.read()

    # Search bar shape
    content = content.replace('.clip(RoundedCornerShape(8.dp)),', '.clip(RoundedCornerShape(32.dp)),')
    
    with open(filepath, 'w') as f:
        f.write(content)

update_file('app/src/main/java/com/example/ui/screens/MainScreen.kt')
update_file('app/src/main/java/com/example/ui/screens/LocalMusicScreen.kt')
