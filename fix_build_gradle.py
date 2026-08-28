with open('app/build.gradle.kts', 'r') as f:
    content = f.read()

content = content.replace(
    'implementation(libs.androidx.media3.session)',
    'implementation(libs.androidx.media3.session)\n  implementation(libs.androidx.media3.datasource.okhttp)'
)

with open('app/build.gradle.kts', 'w') as f:
    f.write(content)
