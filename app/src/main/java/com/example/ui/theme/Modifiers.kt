package com.example.ui.theme

import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.drawBehind
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.Paint
import androidx.compose.ui.graphics.PaintingStyle
import androidx.compose.ui.graphics.drawscope.drawIntoCanvas
import androidx.compose.ui.unit.Dp
import androidx.compose.ui.unit.dp

fun Modifier.neonGlow(
    color: Color,
    cornerRadius: Dp = 24.dp,
    blurRadius: Float = 30f,
    enabled: Boolean = true
): Modifier {
    if (!enabled) return this
    
    return this.drawBehind {
        drawIntoCanvas { canvas ->
            val paint = Paint().apply {
                this.color = color.copy(alpha = 0.5f) // Adjust alpha for glow strength
                val frameworkPaint = this.asFrameworkPaint()
                frameworkPaint.maskFilter = android.graphics.BlurMaskFilter(
                    blurRadius,
                    android.graphics.BlurMaskFilter.Blur.NORMAL
                )
            }
            
            val radiusPx = cornerRadius.toPx()
            val rect = androidx.compose.ui.geometry.Rect(0f, 0f, size.width, size.height)
            
            // Draw glowing outline
            canvas.drawRoundRect(
                left = 0f,
                top = 0f,
                right = size.width,
                bottom = size.height,
                radiusX = radiusPx,
                radiusY = radiusPx,
                paint = paint
            )
        }
    }
}
