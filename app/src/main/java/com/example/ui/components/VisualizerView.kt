package com.example.ui.components
import kotlinx.coroutines.launch

import androidx.compose.animation.core.*
import androidx.compose.foundation.Canvas
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.geometry.Size
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.StrokeCap
import androidx.compose.ui.graphics.StrokeJoin
import androidx.compose.ui.graphics.drawscope.Stroke
import androidx.compose.ui.graphics.Path
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.unit.dp
import com.example.player.AudioAmplituder
import kotlin.math.sin
import kotlin.random.Random
import kotlinx.coroutines.delay
import kotlinx.coroutines.isActive

@Composable
fun VisualizerView(
    isPlaying: Boolean,
    visualizerType: String,
    primaryColor: Color,
    modifier: Modifier = Modifier
) {
    val barCount = if (visualizerType == "Bloques") 16 else 32
    
    // Animate 32 random values
    val animatedHeights = remember { mutableStateListOf<Animatable<Float, AnimationVector1D>>() }
    
    LaunchedEffect(barCount) {
        animatedHeights.clear()
        for (i in 0 until barCount) {
            animatedHeights.add(Animatable(0.1f))
        }
    }

    val amplitude by AudioAmplituder.amplitude.collectAsState(initial = 0f)

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
    }

    Canvas(modifier = modifier.fillMaxWidth().height(100.dp)) {
        val width = size.width
        val height = size.height
        val barWidth = width / (barCount * 1.5f)
        val spacing = (width - (barWidth * barCount)) / (barCount + 1)
        
        if (visualizerType == "Ondas") {
            val path = Path()
            var prevX = 0f
            var prevY = height
            
            for (i in 0 until animatedHeights.size) {
                val barHeight = animatedHeights[i].value * height
                val x = spacing + (i * (barWidth + spacing)) + barWidth / 2
                val y = height - barHeight
                
                if (i == 0) {
                    path.moveTo(x, y)
                } else {
                    val controlX = (prevX + x) / 2f
                    path.cubicTo(controlX, prevY, controlX, y, x, y)
                }
                prevX = x
                prevY = y
            }
            
            // Draw gradient fill
            val fillPath = Path().apply {
                addPath(path)
                lineTo(prevX, height)
                val firstX = spacing + barWidth / 2
                lineTo(firstX, height)
                close()
            }
            drawPath(
                path = fillPath,
                brush = Brush.verticalGradient(
                    colors = listOf(primaryColor.copy(alpha = 0.5f), Color.Transparent),
                    startY = 0f,
                    endY = height
                )
            )
            
            // Draw smooth line
            drawPath(
                path = path,
                color = primaryColor,
                style = Stroke(
                    width = 4.dp.toPx(),
                    cap = StrokeCap.Round,
                    join = StrokeJoin.Round
                )
            )
        } else {
            for (i in 0 until animatedHeights.size) {
                val barHeight = animatedHeights[i].value * height
                val x = spacing + (i * (barWidth + spacing))
                
                when (visualizerType) {
                    "Bloques" -> {
                        val blockHeight = barWidth * 0.8f
                        val blockSpacing = barWidth * 0.2f
                        var currentY = height
                        while (currentY > height - barHeight) {
                            drawRect(
                                color = primaryColor,
                                topLeft = Offset(x, currentY - blockHeight),
                                size = Size(barWidth, blockHeight)
                            )
                            currentY -= (blockHeight + blockSpacing)
                        }
                    }
                    else -> {
                        // "Barras"
                        drawLine(
                            color = primaryColor,
                            start = Offset(x + barWidth/2, height),
                            end = Offset(x + barWidth/2, height - barHeight),
                            strokeWidth = barWidth,
                            cap = StrokeCap.Round
                        )
                    }
                }
            }
        }
    }
}
