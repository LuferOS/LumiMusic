with open('app/src/main/java/com/example/ui/components/FullScreenPlayer.kt', 'r') as f:
    content = f.read()

old_slider = """            Slider(
                value = progress,
                onValueChange = { 
                    val newPosition = (it * duration).toLong()
                    if (Math.abs(currentPosition - newPosition) > 1000) {
                        view.performHapticFeedback(HapticFeedbackConstants.CLOCK_TICK)
                    }
                    controller?.seekTo(newPosition)
                    currentPosition = newPosition
                },
                modifier = Modifier
                    .fillMaxWidth()
                    .height(24.dp),"""

new_slider = """            Slider(
                value = progress,
                onValueChange = { 
                    val newPosition = (it * duration).toLong()
                    if (Math.abs(currentPosition - newPosition) > 1000) {
                        view.performHapticFeedback(HapticFeedbackConstants.CLOCK_TICK)
                    }
                    controller?.seekTo(newPosition)
                    currentPosition = newPosition
                },
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(horizontal = 8.dp)
                    .height(24.dp),"""

content = content.replace(old_slider, new_slider)

with open('app/src/main/java/com/example/ui/components/FullScreenPlayer.kt', 'w') as f:
    f.write(content)
