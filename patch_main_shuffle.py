import re

with open("app/src/main/java/com/example/MainActivity.kt", "r") as f:
    content = f.read()

target = """                            if (mediaController?.mediaItemCount == 1) {
                                if (!viewModel.playNextRemote()) {
                                    viewModel.playNextRandomTrack(profileViewModel.userStats.value.apiPreference)
                                }
                            }"""

replacement = """                            if (mediaController?.mediaItemCount == 1) {
                                val isShuffle = mediaController?.shuffleModeEnabled == true
                                val repeatMode = mediaController?.repeatMode ?: androidx.media3.common.Player.REPEAT_MODE_OFF
                                if (!viewModel.playNextRemote(isShuffle, repeatMode)) {
                                    viewModel.playNextRandomTrack(profileViewModel.userStats.value.apiPreference)
                                }
                            }"""

content = content.replace(target, replacement)

with open("app/src/main/java/com/example/MainActivity.kt", "w") as f:
    f.write(content)
