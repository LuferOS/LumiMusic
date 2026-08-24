import re

with open("app/src/main/java/com/example/ui/components/FullScreenPlayer.kt", "r") as f:
    content = f.read()

imports = """import androidx.compose.ui.platform.LocalView
import android.view.HapticFeedbackConstants"""

if "LocalView" not in content:
    content = content.replace("import androidx.compose.ui.unit.dp", "import androidx.compose.ui.unit.dp\n" + imports)

# Add LocalView inside FullScreenPlayer
target_start = """fun FullScreenPlayer(
    controller: MediaController?,
    dominantColor: Color?,
    viewModel: MainViewModel,
    onClose: () -> Unit
) {
    var isPlaying"""
    
replacement_start = """fun FullScreenPlayer(
    controller: MediaController?,
    dominantColor: Color?,
    viewModel: MainViewModel,
    onClose: () -> Unit
) {
    val view = LocalView.current
    var isPlaying"""
    
content = content.replace(target_start, replacement_start)

# Modify Slider
target_slider = """            Slider(
                value = progress,
                onValueChange = { 
                    val newPosition = (it * duration).toLong()
                    controller?.seekTo(newPosition)
                    currentPosition = newPosition
                },"""
replacement_slider = """            Slider(
                value = progress,
                onValueChange = { 
                    val newPosition = (it * duration).toLong()
                    if (Math.abs(currentPosition - newPosition) > 1000) {
                        view.performHapticFeedback(HapticFeedbackConstants.CLOCK_TICK)
                    }
                    controller?.seekTo(newPosition)
                    currentPosition = newPosition
                },"""
content = content.replace(target_slider, replacement_slider)

# Play/Pause
target_play = """.clickable { if (isPlaying) controller?.pause() else controller?.play() }"""
replacement_play = """.clickable { 
                            view.performHapticFeedback(HapticFeedbackConstants.VIRTUAL_KEY)
                            if (isPlaying) controller?.pause() else controller?.play() 
                        }"""
content = content.replace(target_play, replacement_play)

# Previous
target_prev = """IconButton(onClick = { controller?.seekToPrevious() })"""
replacement_prev = """IconButton(onClick = { 
                        view.performHapticFeedback(HapticFeedbackConstants.VIRTUAL_KEY)
                        controller?.seekToPrevious() 
                    })"""
content = content.replace(target_prev, replacement_prev)

# Next
target_next = """IconButton(onClick = { controller?.seekToNext() })"""
replacement_next = """IconButton(onClick = { 
                        view.performHapticFeedback(HapticFeedbackConstants.VIRTUAL_KEY)
                        controller?.seekToNext() 
                    })"""
content = content.replace(target_next, replacement_next)

# Shuffle
target_shuffle = """                IconButton(onClick = { 
                    controller?.shuffleModeEnabled = !isShuffle
                    isShuffle = !isShuffle
                })"""
replacement_shuffle = """                IconButton(onClick = { 
                    view.performHapticFeedback(HapticFeedbackConstants.VIRTUAL_KEY)
                    controller?.shuffleModeEnabled = !isShuffle
                    isShuffle = !isShuffle
                })"""
content = content.replace(target_shuffle, replacement_shuffle)

# Repeat
target_repeat = """                IconButton(onClick = { 
                    val nextMode = when(repeatMode) {"""
replacement_repeat = """                IconButton(onClick = { 
                    view.performHapticFeedback(HapticFeedbackConstants.VIRTUAL_KEY)
                    val nextMode = when(repeatMode) {"""
content = content.replace(target_repeat, replacement_repeat)

# Like
target_like = """                IconButton(onClick = { 
                    viewModel.toggleLike(currentUri, currentTitle, currentArtist, artworkUri?.toString())
                })"""
replacement_like = """                IconButton(onClick = { 
                    view.performHapticFeedback(HapticFeedbackConstants.VIRTUAL_KEY)
                    viewModel.toggleLike(currentUri, currentTitle, currentArtist, artworkUri?.toString())
                })"""
content = content.replace(target_like, replacement_like)

# Close
target_close = """IconButton(onClick = onClose)"""
replacement_close = """IconButton(onClick = {
                    view.performHapticFeedback(HapticFeedbackConstants.VIRTUAL_KEY)
                    onClose()
                })"""
content = content.replace(target_close, replacement_close)

with open("app/src/main/java/com/example/ui/components/FullScreenPlayer.kt", "w") as f:
    f.write(content)
