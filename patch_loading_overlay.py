import re

with open("app/src/main/java/com/example/MainActivity.kt", "r") as f:
    content = f.read()

target = """                        CircularProgressIndicator(color = dominantColor ?: MaterialTheme.colorScheme.primary)
                        Spacer(modifier = Modifier.height(24.dp))
                        Text(
                            text = loadingQuote,
                            color = MaterialTheme.colorScheme.onSurface,
                            textAlign = TextAlign.Center,
                            style = MaterialTheme.typography.bodyLarge
                        )
                    }
                }
            } else if (dlState is com.example.viewmodel.DownloadState.Error) {"""

replace = """                        CircularProgressIndicator(color = dominantColor ?: MaterialTheme.colorScheme.primary)
                        Spacer(modifier = Modifier.height(24.dp))
                        Text(
                            text = loadingQuote,
                            color = MaterialTheme.colorScheme.onSurface,
                            textAlign = TextAlign.Center,
                            style = MaterialTheme.typography.bodyLarge
                        )
                        Spacer(modifier = Modifier.height(16.dp))
                        TextButton(onClick = { viewModel.resetState() }) {
                            Text("Cancelar", color = MaterialTheme.colorScheme.error)
                        }
                    }
                }
            } else if (dlState is com.example.viewmodel.DownloadState.Error) {"""
            
content = content.replace(target, replace)
with open("app/src/main/java/com/example/MainActivity.kt", "w") as f:
    f.write(content)
