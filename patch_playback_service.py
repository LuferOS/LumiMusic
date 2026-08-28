with open('app/src/main/java/com/example/player/PlaybackService.kt', 'r') as f:
    content = f.read()

old_load_control = """        val loadControl = DefaultLoadControl.Builder()
            .setBufferDurationsMs(
                50000, // min buffer 50s
                100000, // max buffer 100s
                1500, // buffer for playback 1.5s
                2500  // buffer for playback after rebuffer 2.5s
            )
            .build()"""

new_load_control = """        val loadControl = DefaultLoadControl.Builder()
            .setBufferDurationsMs(
                50000, // min buffer 50s
                100000, // max buffer 100s
                250, // buffer for playback 0.25s (Arranque ultra rápido)
                1000  // buffer for playback after rebuffer 1.0s
            )
            .setPrioritizeTimeOverSizeThresholds(true)
            .build()"""

content = content.replace(old_load_control, new_load_control)

old_http = """        @androidx.annotation.OptIn(androidx.media3.common.util.UnstableApi::class)
        val httpDataSourceFactory = DefaultHttpDataSource.Factory().setAllowCrossProtocolRedirects(true)"""

new_http = """        @androidx.annotation.OptIn(androidx.media3.common.util.UnstableApi::class)
        val httpDataSourceFactory = DefaultHttpDataSource.Factory()
            .setAllowCrossProtocolRedirects(true)
            .setConnectTimeoutMs(8000)
            .setReadTimeoutMs(8000)"""

content = content.replace(old_http, new_http)

with open('app/src/main/java/com/example/player/PlaybackService.kt', 'w') as f:
    f.write(content)
