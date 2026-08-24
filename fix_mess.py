import re

with open("app/src/main/java/com/example/ui/components/FullScreenPlayer.kt", "r") as f:
    content = f.read()

# Fix the Row block around Like button
bad_like = """                    Icon(
                        imageVector = if (isLiked) Icons.Rounded.Favorite else Icons.Rounded.FavoriteBorder, 
                        contentDescription = "Like", 
                        tint = if (isLiked) Color(0xFF1DB954) else Color.White, 
                        modifier = Modifier.size(32.dp)
                    )
                }
                }
            }

            Spacer(modifier = Modifier.height(16.dp))"""
fixed_like = """                    Icon(
                        imageVector = if (isLiked) Icons.Rounded.Favorite else Icons.Rounded.FavoriteBorder, 
                        contentDescription = "Like", 
                        tint = if (isLiked) Color(0xFF1DB954) else Color.White, 
                        modifier = Modifier.size(32.dp)
                    )
                }
            }

            Spacer(modifier = Modifier.height(16.dp))"""
content = content.replace(bad_like, fixed_like)

# Fix the Playback controls block
bad_playback = """                    Icon(
                        imageVector = if (repeatMode == Player.REPEAT_MODE_ONE) Icons.Rounded.RepeatOne else Icons.Rounded.Repeat, 
                        contentDescription = "Repeat", 
                        tint = if (repeatMode != Player.REPEAT_MODE_OFF) Color(0xFF1DB954) else Color.White.copy(alpha = 0.7f)
                    )
                }
                }
            }

            Spacer(modifier = Modifier.height(16.dp))"""
fixed_playback = """                    Icon(
                        imageVector = if (repeatMode == Player.REPEAT_MODE_ONE) Icons.Rounded.RepeatOne else Icons.Rounded.Repeat, 
                        contentDescription = "Repeat", 
                        tint = if (repeatMode != Player.REPEAT_MODE_OFF) Color(0xFF1DB954) else Color.White.copy(alpha = 0.7f)
                    )
                }
            }

            Spacer(modifier = Modifier.height(16.dp))"""
content = content.replace(bad_playback, fixed_playback)

with open("app/src/main/java/com/example/ui/components/FullScreenPlayer.kt", "w") as f:
    f.write(content)
