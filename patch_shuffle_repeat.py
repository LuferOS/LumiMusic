import re

with open("app/src/main/java/com/example/ui/components/FullScreenPlayer.kt", "r") as f:
    content = f.read()

target_shuffle = """                IconButton(onClick = { /* Shuffle */ }) {
                    Icon(Icons.Rounded.Shuffle, contentDescription = "Shuffle", tint = Color.White.copy(alpha = 0.7f))
                }"""
replacement_shuffle = """                var isShuffle by remember { mutableStateOf(controller?.shuffleModeEnabled == true) }
                IconButton(onClick = { 
                    controller?.shuffleModeEnabled = !isShuffle
                    isShuffle = !isShuffle
                }) {
                    Icon(Icons.Rounded.Shuffle, contentDescription = "Shuffle", tint = if (isShuffle) Color(0xFF1DB954) else Color.White.copy(alpha = 0.7f))
                }"""
content = content.replace(target_shuffle, replacement_shuffle)

target_repeat = """                IconButton(onClick = { /* Repeat */ }) {
                    Icon(Icons.Rounded.Repeat, contentDescription = "Repeat", tint = Color.White.copy(alpha = 0.7f))
                }"""
replacement_repeat = """                var repeatMode by remember { mutableStateOf(controller?.repeatMode ?: Player.REPEAT_MODE_OFF) }
                IconButton(onClick = { 
                    val nextMode = when(repeatMode) {
                        Player.REPEAT_MODE_OFF -> Player.REPEAT_MODE_ALL
                        Player.REPEAT_MODE_ALL -> Player.REPEAT_MODE_ONE
                        else -> Player.REPEAT_MODE_OFF
                    }
                    controller?.repeatMode = nextMode
                    repeatMode = nextMode
                }) {
                    Icon(
                        imageVector = if (repeatMode == Player.REPEAT_MODE_ONE) Icons.Rounded.RepeatOne else Icons.Rounded.Repeat, 
                        contentDescription = "Repeat", 
                        tint = if (repeatMode != Player.REPEAT_MODE_OFF) Color(0xFF1DB954) else Color.White.copy(alpha = 0.7f)
                    )
                }"""
content = content.replace(target_repeat, replacement_repeat)

with open("app/src/main/java/com/example/ui/components/FullScreenPlayer.kt", "w") as f:
    f.write(content)
