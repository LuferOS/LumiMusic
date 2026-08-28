import re

with open('app/src/main/java/com/example/ui/screens/ProfileScreen.kt', 'r') as f:
    content = f.read()

old_tf = """                    OutlinedTextField(
                        value = newName,
                        onValueChange = { newName = it },
                        label = { Text("Nombre de usuario") },
                        modifier = Modifier.fillMaxWidth()
                    )"""

new_tf = """                    TextField(
                        value = newName,
                        onValueChange = { newName = it },
                        label = { Text("Nombre de usuario", color = Color.White.copy(alpha=0.6f)) },
                        modifier = Modifier.fillMaxWidth().clip(RoundedCornerShape(32.dp)),
                        colors = TextFieldDefaults.colors(
                            focusedContainerColor = Color(0xFF242424),
                            unfocusedContainerColor = Color(0xFF242424),
                            focusedIndicatorColor = Color.Transparent,
                            unfocusedIndicatorColor = Color.Transparent,
                            focusedTextColor = Color.White,
                            unfocusedTextColor = Color.White,
                            cursorColor = Color.White
                        )
                    )"""

content = content.replace(old_tf, new_tf)

with open('app/src/main/java/com/example/ui/screens/ProfileScreen.kt', 'w') as f:
    f.write(content)
