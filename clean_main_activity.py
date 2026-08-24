import re

with open("app/src/main/java/com/example/MainActivity.kt", "r") as f:
    content = f.read()

# First, fix the extra braces before MainScreen.
# The class MainActivity ends before MainScreen.
# Wait, I see:
#     private fun checkAndRequestPermissions() {
#     ...
#     }
#     
#     }
# }
# Let's fix that block.
bad_block = """        if (ContextCompat.checkSelfPermission(this, permission) == PackageManager.PERMISSION_GRANTED) {
            localMusicViewModel.loadLocalMusic(this)
        } else {
            requestPermissionLauncher.launch(permission)
        }
    }

    }
}"""
good_block = """        if (ContextCompat.checkSelfPermission(this, permission) == PackageManager.PERMISSION_GRANTED) {
            localMusicViewModel.loadLocalMusic(this)
        } else {
            requestPermissionLauncher.launch(permission)
        }
    }
"""

content = content.replace(bad_block, good_block)

# Now find the end of the file where onDestroy is, and move it inside MainActivity.
# Remove it from the end:
end_str = """    override fun onDestroy() {
        super.onDestroy()
        controllerFuture?.let { androidx.media3.session.MediaController.releaseFuture(it) }
    }
}"""
if content.endswith(end_str) or end_str in content:
    content = content.replace(end_str, "}") # close the file properly? No, MainScreen is at the end. Wait, `}` at the very end belongs to MainScreen!
    
# Let's just strip the end_str and put `}` because MainScreen ends with `}`.
content = content.replace(end_str, "")

# Now inject onDestroy at the end of MainActivity class.
# The class MainActivity ends right before `@OptIn(ExperimentalMaterial3Api::class)`.
main_screen_annotation = "@OptIn(ExperimentalMaterial3Api::class)"
class_end_idx = content.find(main_screen_annotation)

destroy_in_class = """
    override fun onDestroy() {
        super.onDestroy()
        controllerFuture?.let { androidx.media3.session.MediaController.releaseFuture(it) }
    }
}

"""
content = content[:class_end_idx] + destroy_in_class + content[class_end_idx:]

# Also ensure `clickable` is imported.
if "import androidx.compose.foundation.clickable" not in content:
    content = content.replace("import androidx.compose.foundation.layout.*", "import androidx.compose.foundation.layout.*\nimport androidx.compose.foundation.clickable")

with open("app/src/main/java/com/example/MainActivity.kt", "w") as f:
    f.write(content)
