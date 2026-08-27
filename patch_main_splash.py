import re

with open("app/src/main/java/com/example/MainActivity.kt", "r") as f:
    content = f.read()

target = """                  androidx.compose.animation.SharedTransitionLayout {
                    var selectedTab by remember { mutableStateOf(0) }
                    var showEqualizer by remember { mutableStateOf(false) }

                    BoxWithConstraints(modifier = Modifier.fillMaxSize()) {
                    BoxWithConstraints(modifier = Modifier.fillMaxSize()) {
                        if (!userStats.hasSeenOnboarding) {"""

replacement = """                  androidx.compose.animation.SharedTransitionLayout {
                    var selectedTab by remember { mutableStateOf(userStats.startupTab) }
                    var showEqualizer by remember { mutableStateOf(false) }
                    var showSplash by remember { mutableStateOf(true) }
                    
                    LaunchedEffect(Unit) {
                        kotlinx.coroutines.delay(2000)
                        showSplash = false
                    }

                    BoxWithConstraints(modifier = Modifier.fillMaxSize()) {
                        if (showSplash) {
                            com.example.ui.screens.SplashScreen(primaryColor = activeColor)
                        } else if (!userStats.hasSeenOnboarding) {"""

content = content.replace(target, replacement)

with open("app/src/main/java/com/example/MainActivity.kt", "w") as f:
    f.write(content)
