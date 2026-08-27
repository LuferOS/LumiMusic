with open("app/src/main/AndroidManifest.xml", "r") as f:
    content = f.read()
    
new_perms = """
    <uses-permission android:name="android.permission.FOREGROUND_SERVICE" />
    <uses-permission android:name="android.permission.FOREGROUND_SERVICE_MEDIA_PLAYBACK" />
    <uses-permission android:name="android.permission.POST_NOTIFICATIONS" />
"""

if "FOREGROUND_SERVICE_MEDIA_PLAYBACK" not in content:
    content = content.replace("<uses-permission android:name=\"android.permission.INTERNET\" />", "<uses-permission android:name=\"android.permission.INTERNET\" />\n" + new_perms)
    with open("app/src/main/AndroidManifest.xml", "w") as f:
        f.write(content)
