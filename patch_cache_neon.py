with open("app/src/main/java/com/example/ui/screens/ProfileScreen.kt", "r") as f:
    content = f.read()

target_cache = """                SettingItem(
                    icon = Icons.Rounded.Delete,
                    title = "Limpiar Caché",
                    subtitle = "Libera espacio borrando música temporal",
                    onClick = {
                        viewModel.clearCache(context)
                        android.widget.Toast.makeText(context, "Caché limpiada correctamente", android.widget.Toast.LENGTH_SHORT).show()
                    }
                )"""
replacement_cache = """                SettingItem(
                    icon = Icons.Rounded.Delete,
                    title = "Limpiar Caché",
                    subtitle = "Libera espacio borrando música temporal",
                    applyNeon = applyNeon,
                    neonColor = dominantColor ?: Color.Gray,
                    onClick = {
                        viewModel.clearCache(context)
                        android.widget.Toast.makeText(context, "Caché limpiada correctamente", android.widget.Toast.LENGTH_SHORT).show()
                    }
                )"""
content = content.replace(target_cache, replacement_cache)

target_info = """                SettingItem(
                    icon = Icons.Rounded.Info,
                    title = "Acerca de LumiMusic",
                    subtitle = "Versión y créditos",
                    onClick = { showCreditsDialog = true }
                )"""
replacement_info = """                SettingItem(
                    icon = Icons.Rounded.Info,
                    title = "Acerca de LumiMusic",
                    subtitle = "Versión y créditos",
                    applyNeon = applyNeon,
                    neonColor = dominantColor ?: Color.White,
                    onClick = { showCreditsDialog = true }
                )"""
content = content.replace(target_info, replacement_info)

with open("app/src/main/java/com/example/ui/screens/ProfileScreen.kt", "w") as f:
    f.write(content)
