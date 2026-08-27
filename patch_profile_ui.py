with open("app/src/main/java/com/example/ui/screens/ProfileScreen.kt", "r") as f:
    content = f.read()

target = """                SettingItem(
                    icon = Icons.Rounded.Share,
                    title = "Invitar a amigos",
                    subtitle = "Comparte la aplicación APK",
                    onClick = { shareApk(context) }
                )"""

replace = """                SettingItem(
                    icon = Icons.Rounded.Share,
                    title = "Invitar a amigos",
                    subtitle = "Comparte la aplicación APK",
                    onClick = { shareApk(context) }
                )
                
                SettingItem(
                    icon = Icons.Rounded.Delete,
                    title = "Limpiar Caché",
                    subtitle = "Libera espacio borrando música temporal",
                    onClick = {
                        viewModel.clearCache(context)
                        android.widget.Toast.makeText(context, "Caché limpiada correctamente", android.widget.Toast.LENGTH_SHORT).show()
                    }
                )"""

if "Limpiar Caché" not in content:
    content = content.replace(target, replace)
    
if "import androidx.compose.material.icons.rounded.Delete" not in content:
    content = content.replace("import androidx.compose.material.icons.rounded.Share", "import androidx.compose.material.icons.rounded.Share\nimport androidx.compose.material.icons.rounded.Delete")

with open("app/src/main/java/com/example/ui/screens/ProfileScreen.kt", "w") as f:
    f.write(content)
