def patch_file(filepath):
    with open(filepath, "r") as f:
        content = f.read()

    if "import com.example.utils.bouncyClick" not in content:
        content = content.replace("import androidx.compose.ui.Modifier", "import androidx.compose.ui.Modifier\nimport com.example.utils.bouncyClick")
        with open(filepath, "w") as f:
            f.write(content)

patch_file("app/src/main/java/com/example/MainActivity.kt")
patch_file("app/src/main/java/com/example/ui/screens/ProfileScreen.kt")
