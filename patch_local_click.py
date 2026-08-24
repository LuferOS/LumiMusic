import re

with open("app/src/main/java/com/example/ui/screens/LocalMusicScreen.kt", "r") as f:
    content = f.read()

old_click = """                    modifier = Modifier.clickable {
                        controller?.let {
                            it.clearMediaItems()
                            it.addMediaItem(
                                androidx.media3.common.MediaItem.Builder()
                                    .setUri(audio.uri)
                                    .setMediaMetadata(
                                        androidx.media3.common.MediaMetadata.Builder()
                                            .setTitle(audio.title)
                                            .setArtist(audio.artist)
                                            .build()
                                    )
                                    .build()
                            )
                            it.prepare()
                            it.play()
                        }
                    }"""

new_click = """                    modifier = Modifier.clickable {
                        val index = filteredList.indexOf(audio)
                        if (index != -1 && controller != null) {
                            val mediaItems = filteredList.map { track ->
                                androidx.media3.common.MediaItem.Builder()
                                    .setUri(track.uri)
                                    .setMediaMetadata(
                                        androidx.media3.common.MediaMetadata.Builder()
                                            .setTitle(track.title)
                                            .setArtist(track.artist)
                                            .build()
                                    )
                                    .build()
                            }
                            controller.setMediaItems(mediaItems)
                            controller.seekToDefaultPosition(index)
                            controller.prepare()
                            controller.play()
                        }
                    }"""

content = content.replace(old_click, new_click)

with open("app/src/main/java/com/example/ui/screens/LocalMusicScreen.kt", "w") as f:
    f.write(content)
