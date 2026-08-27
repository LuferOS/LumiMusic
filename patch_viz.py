with open("app/src/main/java/com/example/ui/components/VisualizerView.kt", "r") as f:
    content = f.read()

# Make sure we have Stroke and StrokeJoin imported
if "import androidx.compose.ui.graphics.drawscope.Stroke" not in content:
    content = content.replace("import androidx.compose.ui.graphics.StrokeCap", "import androidx.compose.ui.graphics.StrokeCap\nimport androidx.compose.ui.graphics.StrokeJoin\nimport androidx.compose.ui.graphics.drawscope.Stroke\nimport androidx.compose.ui.graphics.Path\nimport androidx.compose.ui.graphics.Brush")

target_canvas = """    Canvas(modifier = modifier.fillMaxWidth().height(100.dp)) {
        val width = size.width
        val height = size.height
        val barWidth = width / (barCount * 1.5f)
        val spacing = (width - (barWidth * barCount)) / (barCount + 1)
        
        for (i in 0 until animatedHeights.size) {
            val barHeight = animatedHeights[i].value * height
            val x = spacing + (i * (barWidth + spacing))
            
            when (visualizerType) {
                "Bloques" -> {
                    // Draw discrete blocks instead of continuous lines
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
                "Ondas" -> {
                    // Draw a continuous curve or rounded bars
                    drawLine(
                        color = primaryColor,
                        start = Offset(x + barWidth/2, height),
                        end = Offset(x + barWidth/2, height - barHeight),
                        strokeWidth = barWidth,
                        cap = StrokeCap.Round
                    )
                }
                else -> {
                    // Default bars
                    drawRect(
                        color = primaryColor,
                        topLeft = Offset(x, height - barHeight),
                        size = Size(barWidth, barHeight)
                    )
                }
            }
        }
    }"""

replacement_canvas = """    Canvas(modifier = modifier.fillMaxWidth().height(100.dp)) {
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
    }"""

content = content.replace(target_canvas, replacement_canvas)

with open("app/src/main/java/com/example/ui/components/VisualizerView.kt", "w") as f:
    f.write(content)
