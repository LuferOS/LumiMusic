with open("app/src/main/java/com/example/player/PlaybackService.kt", "r") as f:
    content = f.read()

import re

# We need to add DefaultRenderersFactory with TeeAudioProcessor
if "androidx.media3.exoplayer.DefaultRenderersFactory" not in content:
    content = content.replace("import androidx.media3.exoplayer.ExoPlayer", "import androidx.media3.exoplayer.ExoPlayer\nimport androidx.media3.exoplayer.DefaultRenderersFactory\nimport androidx.media3.exoplayer.audio.DefaultAudioSink\nimport androidx.media3.exoplayer.audio.TeeAudioProcessor")

target = """        val player = ExoPlayer.Builder(this)
            .setMediaSourceFactory(mediaSourceFactory)
            .setAudioAttributes(
                AudioAttributes.Builder()
                    .setContentType(C.AUDIO_CONTENT_TYPE_MUSIC)
                    .setUsage(C.USAGE_MEDIA)
                    .build(),
                true // handleAudioFocus
            )
            .setLoadControl(loadControl)
            .setHandleAudioBecomingNoisy(true)
            .build()"""

replacement = """        val teeProcessor = TeeAudioProcessor(AudioAmplituder)
        val renderersFactory = object : DefaultRenderersFactory(this) {
            override fun buildAudioSink(context: android.content.Context, enableFloatOutput: Boolean, enableAudioTrackPlaybackParams: Boolean): androidx.media3.exoplayer.audio.AudioSink {
                return DefaultAudioSink.Builder(context)
                    .setAudioProcessors(arrayOf(teeProcessor))
                    .build()
            }
        }

        val player = ExoPlayer.Builder(this, renderersFactory)
            .setMediaSourceFactory(mediaSourceFactory)
            .setAudioAttributes(
                AudioAttributes.Builder()
                    .setContentType(C.AUDIO_CONTENT_TYPE_MUSIC)
                    .setUsage(C.USAGE_MEDIA)
                    .build(),
                true // handleAudioFocus
            )
            .setLoadControl(loadControl)
            .setHandleAudioBecomingNoisy(true)
            .build()"""

content = content.replace(target, replacement)

with open("app/src/main/java/com/example/player/PlaybackService.kt", "w") as f:
    f.write(content)
