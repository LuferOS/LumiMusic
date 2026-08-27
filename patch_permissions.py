import re

with open("app/src/main/java/com/example/MainActivity.kt", "r") as f:
    content = f.read()

imports = """import android.Manifest
import android.os.Build
import androidx.core.app.ActivityCompat
import androidx.core.content.ContextCompat
import android.content.pm.PackageManager
"""

if "import android.Manifest" not in content:
    content = content.replace("import android.os.Bundle", "import android.os.Bundle\n" + imports)

target_create = "    override fun onCreate(savedInstanceState: Bundle?) {"
replace_create = """    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.TIRAMISU) {
            if (ContextCompat.checkSelfPermission(this, Manifest.permission.POST_NOTIFICATIONS) != PackageManager.PERMISSION_GRANTED) {
                ActivityCompat.requestPermissions(this, arrayOf(Manifest.permission.POST_NOTIFICATIONS), 101)
            }
        }"""
        
if "Manifest.permission.POST_NOTIFICATIONS" not in content:
    content = content.replace("    override fun onCreate(savedInstanceState: Bundle?) {\n        super.onCreate(savedInstanceState)", replace_create)

with open("app/src/main/java/com/example/MainActivity.kt", "w") as f:
    f.write(content)
