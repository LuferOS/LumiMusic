import re

with open("app/src/main/java/com/example/ui/components/FullScreenPlayer.kt", "r") as f:
    content = f.read()

target_prev = """                IconButton(onClick = { 
                        view.performHapticFeedback(HapticFeedbackConstants.VIRTUAL_KEY)
                        if ((controller?.mediaItemCount ?: 0) <= 1) {
                            viewModel.playPreviousRemote()
                        } else {
                            controller?.seekToPrevious() 
                        }
                    }) {"""

replacement_prev = """                IconButton(onClick = { 
                        view.performHapticFeedback(HapticFeedbackConstants.VIRTUAL_KEY)
                        if ((controller?.mediaItemCount ?: 0) <= 1) {
                            val isShuffle = controller?.shuffleModeEnabled == true
                            val repeatMode = controller?.repeatMode ?: Player.REPEAT_MODE_OFF
                            viewModel.playPreviousRemote(isShuffle, repeatMode)
                        } else {
                            controller?.seekToPrevious() 
                        }
                    }) {"""

content = content.replace(target_prev, replacement_prev)

target_next = """                IconButton(onClick = { 
                        view.performHapticFeedback(HapticFeedbackConstants.VIRTUAL_KEY)
                        if ((controller?.mediaItemCount ?: 0) <= 1) {
                            viewModel.playNextRemote()
                        } else {
                            controller?.seekToNext() 
                        }
                    }) {"""

replacement_next = """                IconButton(onClick = { 
                        view.performHapticFeedback(HapticFeedbackConstants.VIRTUAL_KEY)
                        if ((controller?.mediaItemCount ?: 0) <= 1) {
                            val isShuffle = controller?.shuffleModeEnabled == true
                            val repeatMode = controller?.repeatMode ?: Player.REPEAT_MODE_OFF
                            viewModel.playNextRemote(isShuffle, repeatMode)
                        } else {
                            controller?.seekToNext() 
                        }
                    }) {"""

content = content.replace(target_next, replacement_next)

with open("app/src/main/java/com/example/ui/components/FullScreenPlayer.kt", "w") as f:
    f.write(content)
