import re

with open("app/src/main/java/com/example/MainActivity.kt", "r") as f:
    content = f.read()

# Remove onStart and onStop
start_idx = content.find("    override fun onStart() {")
end_idx = content.find("    private fun checkAndRequestPermissions() {")
if start_idx != -1 and end_idx != -1:
    content = content[:start_idx] + content[end_idx:]

start_idx2 = content.find("    override fun onStop() {")
end_idx2 = content.find("}", start_idx2 + 20)
if start_idx2 != -1 and end_idx2 != -1:
    content = content[:start_idx2] + content[end_idx2+1:]

# Add initialization to onCreate
init_code = """
        val sessionToken = androidx.media3.session.SessionToken(this, android.content.ComponentName(this, com.example.player.PlaybackService::class.java))
        controllerFuture = androidx.media3.session.MediaController.Builder(this, sessionToken).buildAsync()
        controllerFuture?.addListener(
            {
                mediaController = controllerFuture?.get()
            },
            com.google.common.util.concurrent.MoreExecutors.directExecutor()
        )
"""
content = content.replace("        setContent {", init_code + "\n        setContent {")

# Add onDestroy
destroy_code = """
    override fun onDestroy() {
        super.onDestroy()
        controllerFuture?.let { androidx.media3.session.MediaController.releaseFuture(it) }
    }
"""
content = content[:content.rfind("}")] + destroy_code + "\n}"

with open("app/src/main/java/com/example/MainActivity.kt", "w") as f:
    f.write(content)
