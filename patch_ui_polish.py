import re

# 1. MainScreen.kt - Search Bar & Lists padding/corners
with open('app/src/main/java/com/example/ui/screens/MainScreen.kt', 'r') as f:
    ms_content = f.read()

# Refine search bar shape and padding
ms_content = ms_content.replace('RoundedCornerShape(32.dp)', 'RoundedCornerShape(8.dp)')
# Refine result rows
ms_content = ms_content.replace('size(56.dp)', 'size(56.dp)\n                                    .clip(RoundedCornerShape(8.dp))')
ms_content = ms_content.replace('clip(RoundedCornerShape(4.dp))', 'clip(RoundedCornerShape(8.dp))')
with open('app/src/main/java/com/example/ui/screens/MainScreen.kt', 'w') as f:
    f.write(ms_content)

# 2. LocalMusicScreen.kt - Refine lists
with open('app/src/main/java/com/example/ui/screens/LocalMusicScreen.kt', 'r') as f:
    lms_content = f.read()

lms_content = lms_content.replace('.background(Color.Black)', '.background(Color(0xFF121212))')
lms_content = lms_content.replace('size(64.dp)', 'size(56.dp)')
lms_content = lms_content.replace('clip(RoundedCornerShape(4.dp))', 'clip(RoundedCornerShape(8.dp))')
lms_content = lms_content.replace('Color(0xFF5353CE)', 'Color(0xFF1DB954)')

with open('app/src/main/java/com/example/ui/screens/LocalMusicScreen.kt', 'w') as f:
    f.write(lms_content)

# 3. ProfileScreen.kt - Enhance list items to be subtle cards
with open('app/src/main/java/com/example/ui/screens/ProfileScreen.kt', 'r') as f:
    ps_content = f.read()

ps_content = ps_content.replace('.background(Color.Black)', '.background(Color(0xFF121212))')
# Give SettingItem a subtle background when neon is false
ps_content = ps_content.replace('.padding(horizontal = 16.dp, vertical = 16.dp),', '.padding(horizontal = 16.dp, vertical = 16.dp),\n        verticalAlignment = Alignment.CenterVertically\n    ) {\n        Row(\n            modifier = Modifier.fillMaxWidth().background(Color.White.copy(alpha = 0.05f), RoundedCornerShape(12.dp)).padding(16.dp),')

with open('app/src/main/java/com/example/ui/screens/ProfileScreen.kt', 'w') as f:
    f.write(ps_content)
