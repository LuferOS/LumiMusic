with open('app/build.gradle.kts', 'r') as f:
    content = f.read()

content = content.replace('versionCode = 7', 'versionCode = 8')
content = content.replace('versionName = "2.0"', 'versionName = "2.1"')

with open('app/build.gradle.kts', 'w') as f:
    f.write(content)
