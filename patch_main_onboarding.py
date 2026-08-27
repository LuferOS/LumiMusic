import re

with open("app/src/main/java/com/example/MainActivity.kt", "r") as f:
    content = f.read()

target_start = "                    BoxWithConstraints(modifier = Modifier.fillMaxSize()) {"
target_end = "                                        val isWideScreen = maxWidth >= 600.dp"

replacement = """                    BoxWithConstraints(modifier = Modifier.fillMaxSize()) {
                        if (!userStats.hasSeenOnboarding) {
                            com.example.ui.screens.OnboardingScreen(
                                primaryColor = activeColor,
                                onComplete = { profileViewModel.completeOnboarding() }
                            )
                        } else {
                            val isWideScreen = maxWidth >= 600.dp"""

# Also need to close the 'else' block for Onboarding
# Find the end of BoxWithConstraints which ends right before `if (showEqualizer)`
target_equalizer = "                        if (showEqualizer) {"
replacement_equalizer = """                        } // end else
                        if (showEqualizer) {"""

content = content.replace("                        val isWideScreen = maxWidth >= 600.dp", replacement)
content = content.replace("                        if (showEqualizer) {", replacement_equalizer)

with open("app/src/main/java/com/example/MainActivity.kt", "w") as f:
    f.write(content)
