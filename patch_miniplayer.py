import re

with open("app/src/main/java/com/example/ui/components/MiniPlayer.kt", "r") as f:
    content = f.read()

target_signature = """fun MiniPlayer(
    controller: MediaController?,
    dominantColor: Color?,
    viewModel: MainViewModel,
    onExpand: () -> Unit
) {"""

replacement_signature = """@OptIn(androidx.compose.animation.ExperimentalSharedTransitionApi::class)
@Composable
fun MiniPlayer(
    controller: MediaController?,
    dominantColor: Color?,
    viewModel: MainViewModel,
    sharedTransitionScope: androidx.compose.animation.SharedTransitionScope,
    onExpand: () -> Unit
) {"""
content = content.replace("@Composable\n" + target_signature, replacement_signature)

target_box = """                    Box(
                        modifier = Modifier
                            .size(40.dp)
                            .clip(RoundedCornerShape(4.dp))
                            .background(Color.White.copy(alpha = 0.1f)),
                        contentAlignment = Alignment.Center
                    ) {"""

replacement_box = """                    with(sharedTransitionScope) {
                        Box(
                            modifier = Modifier
                                .size(40.dp)
                                .sharedElement(
                                    state = rememberSharedContentState(key = "album_art"),
                                    animatedVisibilityScope = this@AnimatedVisibility
                                )
                                .clip(RoundedCornerShape(4.dp))
                                .background(Color.White.copy(alpha = 0.1f)),
                            contentAlignment = Alignment.Center
                        ) {"""
content = content.replace(target_box, replacement_box)
content = content.replace("                    }\n                                        \n                    Spacer", "                    }\n                    }\n                                        \n                    Spacer")

with open("app/src/main/java/com/example/ui/components/MiniPlayer.kt", "w") as f:
    f.write(content)
