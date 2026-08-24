package com.example.player

import android.media.audiofx.Equalizer
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.update

data class EqState(
    val enabled: Boolean = false,
    val presets: List<String> = emptyList(),
    val currentPreset: Short = -1,
    val bands: List<BandState> = emptyList()
)

data class BandState(
    val index: Short,
    val centerFreqHz: Int,
    val level: Short,
    val minLevel: Short,
    val maxLevel: Short
)

object AudioEffectManager {
    private var equalizer: Equalizer? = null
    private val _eqState = MutableStateFlow(EqState())
    val eqState: StateFlow<EqState> = _eqState.asStateFlow()

    fun init(audioSessionId: Int) {
        try {
            equalizer?.release()
            equalizer = Equalizer(0, audioSessionId)
            equalizer?.enabled = true
            updateState()
        } catch (e: Exception) {
            e.printStackTrace()
        }
    }
    
    fun setEnabled(enabled: Boolean) {
        equalizer?.enabled = enabled
        _eqState.update { it.copy(enabled = enabled) }
    }

    fun setBandLevel(band: Short, level: Short) {
        equalizer?.setBandLevel(band, level)
        updateState()
    }

    fun usePreset(preset: Short) {
        equalizer?.usePreset(preset)
        updateState()
    }
    
    fun reset() {
        val eq = equalizer ?: return
        try {
            for (i in 0 until eq.numberOfBands) {
                eq.setBandLevel(i.toShort(), 0)
            }
            updateState()
        } catch (e: Exception) {}
    }

    private fun updateState() {
        val eq = equalizer ?: return
        try {
            val presets = mutableListOf<String>()
            for (i in 0 until eq.numberOfPresets) {
                presets.add(eq.getPresetName(i.toShort()))
            }
            val bands = mutableListOf<BandState>()
            val minLevel = eq.bandLevelRange[0]
            val maxLevel = eq.bandLevelRange[1]
            for (i in 0 until eq.numberOfBands) {
                val idx = i.toShort()
                bands.add(
                    BandState(
                        index = idx,
                        centerFreqHz = eq.getCenterFreq(idx) / 1000,
                        level = eq.getBandLevel(idx),
                        minLevel = minLevel,
                        maxLevel = maxLevel
                    )
                )
            }
            _eqState.update { 
                it.copy(
                    enabled = eq.enabled,
                    presets = presets,
                    currentPreset = eq.currentPreset,
                    bands = bands
                ) 
            }
        } catch (e: Exception) {}
    }

    fun release() {
        equalizer?.release()
        equalizer = null
    }
}
