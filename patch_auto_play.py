import re

with open("app/src/main/java/com/example/MainActivity.kt", "r") as f:
    content = f.read()

target = """                mediaController = controllerFuture?.get()
            },
            com.google.common.util.concurrent.MoreExecutors.directExecutor()
        )"""

replacement = """                mediaController = controllerFuture?.get()
                mediaController?.addListener(object : androidx.media3.common.Player.Listener {
                    override fun onMediaItemTransition(mediaItem: androidx.media3.common.MediaItem?, reason: Int) {
                        super.onMediaItemTransition(mediaItem, reason)
                        if (reason == androidx.media3.common.Player.MEDIA_ITEM_TRANSITION_REASON_AUTO) {
                            // If auto-transition happened, wait and see if we have next item. If not, the player might stop.
                            // However, we want to add random tracks. 
                        }
                    }
                    
                    override fun onPlaybackStateChanged(playbackState: Int) {
                        if (playbackState == androidx.media3.common.Player.STATE_ENDED) {
                            // Queue ended, play next random
                            viewModel.playNextRandomTrack(profileViewModel.userStats.value.apiPreference)
                        }
                    }
                })
            },
            com.google.common.util.concurrent.MoreExecutors.directExecutor()
        )"""

content = content.replace(target, replacement)

with open("app/src/main/java/com/example/MainActivity.kt", "w") as f:
    f.write(content)
