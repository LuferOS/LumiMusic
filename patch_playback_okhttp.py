with open('app/src/main/java/com/example/player/PlaybackService.kt', 'r') as f:
    content = f.read()

old_import = "import androidx.media3.datasource.DefaultHttpDataSource"
new_import = "import androidx.media3.datasource.DefaultHttpDataSource\nimport androidx.media3.datasource.okhttp.OkHttpDataSource\nimport com.example.data.NetworkClient"

if old_import in content:
    content = content.replace(old_import, new_import)

old_http = """        @androidx.annotation.OptIn(androidx.media3.common.util.UnstableApi::class)
        val httpDataSourceFactory = DefaultHttpDataSource.Factory()
            .setAllowCrossProtocolRedirects(true)
            .setConnectTimeoutMs(8000)
            .setReadTimeoutMs(8000)"""

new_http = """        @androidx.annotation.OptIn(androidx.media3.common.util.UnstableApi::class)
        val httpDataSourceFactory = OkHttpDataSource.Factory(NetworkClient.sharedClient)"""

content = content.replace(old_http, new_http)

with open('app/src/main/java/com/example/player/PlaybackService.kt', 'w') as f:
    f.write(content)
