with open("app/src/main/AndroidManifest.xml", "r") as f:
    content = f.read()

target = """        <service
            android:name=".player.PlaybackService"
            android:exported="true">"""
replace = """        <service
            android:name=".player.PlaybackService"
            android:foregroundServiceType="mediaPlayback"
            android:exported="true">"""
            
if "foregroundServiceType=\"mediaPlayback\"" not in content:
    content = content.replace(target, replace)
    with open("app/src/main/AndroidManifest.xml", "w") as f:
        f.write(content)
