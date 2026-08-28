with open('gradle/libs.versions.toml', 'r') as f:
    lines = f.readlines()

with open('gradle/libs.versions.toml', 'w') as f:
    for line in lines:
        if 'androidx-media3-datasource-okhttp' in line:
            continue
        if '[plugins]' in line:
            f.write('androidx-media3-datasource-okhttp = { group = "androidx.media3", name = "media3-datasource-okhttp", version.ref = "media3" }\n\n')
        f.write(line)
