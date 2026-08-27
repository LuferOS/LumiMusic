package com.example.player

import androidx.media3.common.audio.AudioProcessor.AudioFormat
import androidx.media3.exoplayer.audio.TeeAudioProcessor
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import java.nio.ByteBuffer

object AudioAmplituder : TeeAudioProcessor.AudioBufferSink {
    var enabled: Boolean = true

    private val _amplitude = MutableStateFlow(0f)
    val amplitude: StateFlow<Float> = _amplitude

    override fun flush(sampleRateHz: Int, channelCount: Int, encoding: Int) {
        _amplitude.value = 0f
    }

    override fun handleBuffer(buffer: ByteBuffer) {
        if (!enabled) return
        val limit = buffer.limit()
        if (limit == 0) return
        var sum = 0.0
        var count = 0
        val pos = buffer.position()
        
        // Assuming 16-bit PCM
        while (buffer.position() < limit - 1) {
            val sample = buffer.short.toDouble()
            sum += sample * sample
            count++
        }
        buffer.position(pos) // Restore position

        if (count > 0) {
            val rms = Math.sqrt(sum / count)
            // Normalize roughly (max 16-bit is 32768)
            val normalized = (rms / 32768.0).toFloat().coerceIn(0f, 1f)
            // Apply a simple smoothing or just send it directly
            _amplitude.value = normalized
        }
    }
}
