with open("app/src/main/java/com/example/ui/components/VisualizerView.kt", "r") as f:
    content = f.read()

# Add imports for AudioAmplituder
if "import com.example.player.AudioAmplituder" not in content:
    content = content.replace("import androidx.compose.ui.unit.dp", "import androidx.compose.ui.unit.dp\nimport com.example.player.AudioAmplituder\nimport kotlin.math.sin")

# We want to observe amplitude
# Replace:
target_launched = """    LaunchedEffect(isPlaying, visualizerType) {
        if (isPlaying) {
            while (isActive) {
                animatedHeights.forEachIndexed { index, animatable ->
                    val isCenter = index in (barCount/3)..(barCount - barCount/3)
                    val maxVal = if (isCenter) 1f else 0.5f // center bars go higher
                    val randomTarget = Random.nextFloat() * maxVal + 0.1f
                    
                    launch {
                        animatable.animateTo(
                            targetValue = randomTarget,
                            animationSpec = tween(
                                durationMillis = Random.nextInt(200, 400),
                                easing = FastOutSlowInEasing
                            )
                        )
                    }
                }
                delay(300)
            }
        } else {
            // Flatten when paused
            animatedHeights.forEach { animatable ->
                launch {
                    animatable.animateTo(0.1f, tween(500))
                }
            }
        }
    }"""

replacement_launched = """    val amplitude by AudioAmplituder.amplitude.collectAsState(initial = 0f)

    LaunchedEffect(isPlaying, visualizerType) {
        if (isPlaying) {
            var time = 0f
            while (isActive) {
                time += 0.1f
                
                // Read current real amplitude from TeeAudioProcessor (0.0 to ~1.0)
                // Boost it visually so small beats show up well
                val currentAmp = (AudioAmplituder.amplitude.value * 3f).coerceIn(0f, 1f)
                
                animatedHeights.forEachIndexed { index, animatable ->
                    val normalizedPos = kotlin.math.abs((index - barCount / 2f) / (barCount / 2f)) // 0 at center, 1 at edges
                    
                    // Center bars react heavily to amplitude (bass/beats)
                    val beatFactor = (1f - normalizedPos) * currentAmp
                    
                    // High frequencies (edges) are more random but lower amplitude, still scaled by overall volume
                    val highFreq = Random.nextFloat() * (0.2f + normalizedPos * 0.3f) * currentAmp
                    
                    // A subtle wave for constant fluid motion even in quiet parts
                    val wave = (sin(time * 2f + index * 0.5f).toFloat() + 1f) / 2f * 0.15f
                    
                    // Combine them and ensure a minimum floor
                    val targetHeight = (beatFactor + highFreq + wave).coerceIn(0.02f, 1f)
                    
                    launch {
                        animatable.animateTo(
                            targetValue = targetHeight,
                            animationSpec = tween(
                                durationMillis = 60, // Fast update for real-time reactivity
                                easing = LinearEasing
                            )
                        )
                    }
                }
                delay(60) // approx 16 FPS for fluid animation without overwhelming compose
            }
        } else {
            // Flatten when paused
            animatedHeights.forEach { animatable ->
                launch {
                    animatable.animateTo(0.02f, tween(500))
                }
            }
        }
    }"""

content = content.replace(target_launched, replacement_launched)

with open("app/src/main/java/com/example/ui/components/VisualizerView.kt", "w") as f:
    f.write(content)
