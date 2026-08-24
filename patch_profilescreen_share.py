import re

with open("app/src/main/java/com/example/ui/screens/ProfileScreen.kt", "r") as f:
    content = f.read()

old_button = """                onClick = {
                    val intent = Intent(Intent.ACTION_SEND).apply {
                        type = "text/plain"
                        putExtra(Intent.EXTRA_SUBJECT, "Check out this Music App!")
                        putExtra(Intent.EXTRA_TEXT, "Hey! Download this awesome AMOLED music player. You can export the .APK directly from AI Studio -> Settings -> Export APK!")
                    }
                    context.startActivity(Intent.createChooser(intent, "Share App"))
                },"""

new_button = """                onClick = {
                    shareApk(context)
                },"""

content = content.replace(old_button, new_button)

imports = """import androidx.core.content.FileProvider
import java.io.File
import java.io.FileInputStream
import java.io.FileOutputStream
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch"""

# Add imports after the package declaration
content = re.sub(r'(package com.example.ui.screens\n)', r'\1\n' + imports + '\n', content)

# Add the shareApk function at the end of the file
share_func = """
fun shareApk(context: android.content.Context) {
    CoroutineScope(Dispatchers.IO).launch {
        try {
            val appInfo = context.applicationInfo
            val srcFile = File(appInfo.sourceDir)
            
            val cachePath = File(context.cacheDir, "shared_apks")
            if (!cachePath.exists()) {
                cachePath.mkdirs()
            }
            
            val destFile = File(cachePath, "LumiMusic.apk")
            
            // Copy APK to cache directory
            FileInputStream(srcFile).use { input ->
                FileOutputStream(destFile).use { output ->
                    input.copyTo(output)
                }
            }
            
            // Get URI using FileProvider
            val apkUri = FileProvider.getUriForFile(
                context,
                "${context.packageName}.fileprovider",
                destFile
            )
            
            val intent = Intent(Intent.ACTION_SEND).apply {
                type = "application/vnd.android.package-archive"
                putExtra(Intent.EXTRA_STREAM, apkUri)
                addFlags(Intent.FLAG_GRANT_READ_URI_PERMISSION)
                addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
            }
            
            context.startActivity(Intent.createChooser(intent, "Share Application APK").apply {
                addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
            })
            
        } catch (e: Exception) {
            e.printStackTrace()
        }
    }
}
"""
content += share_func

with open("app/src/main/java/com/example/ui/screens/ProfileScreen.kt", "w") as f:
    f.write(content)
