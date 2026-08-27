with open("app/src/main/java/com/example/ui/components/FullScreenPlayer.kt", "r") as f:
    content = f.read()

target = """fun FullScreenPlayer(
    controller: MediaController?,
    dominantColor: Color?,
    viewModel: MainViewModel,
    sharedTransitionScope: androidx.compose.animation.SharedTransitionScope,
    animatedVisibilityScope: androidx.compose.animation.AnimatedVisibilityScope,
    onClose: () -> Unit
)"""

replacement = """fun FullScreenPlayer(
    controller: MediaController?,
    dominantColor: Color?,
    viewModel: MainViewModel,
    userStats: com.example.data.local.UserStats,
    sharedTransitionScope: androidx.compose.animation.SharedTransitionScope,
    animatedVisibilityScope: androidx.compose.animation.AnimatedVisibilityScope,
    onClose: () -> Unit
)"""

content = content.replace(target, replacement)

# Now, add the visualizer to the UI
# Let's see where to put it. Maybe between the artwork and the playback controls.
target_ui = """                Spacer(modifier = Modifier.height(32.dp))
                
                // Track Info"""

replacement_ui = """                Spacer(modifier = Modifier.height(16.dp))
                
                VisualizerView(
                    isPlaying = isPlaying,
                    visualizerType = userStats.visualizerType,
                    primaryColor = if (userStats.visualizerColor == "Dinámico") (dominantColor ?: Color.White) else {
                        try { Color(android.graphics.Color.parseColor(userStats.visualizerColor)) } catch(e: Exception) { Color.White }
                    },
                    modifier = Modifier.padding(horizontal = 32.dp)
                )

                Spacer(modifier = Modifier.height(16.dp))
                
                // Track Info"""
                
content = content.replace(target_ui, replacement_ui)

with open("app/src/main/java/com/example/ui/components/FullScreenPlayer.kt", "w") as f:
    f.write(content)
