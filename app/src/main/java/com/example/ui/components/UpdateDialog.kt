package com.example.ui.components

import android.content.Intent
import android.net.Uri
import androidx.compose.material3.AlertDialog
import androidx.compose.material3.Button
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.material3.TextButton
import androidx.compose.runtime.Composable
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.platform.LocalContext

@Composable
fun UpdateDialog(
    isAvailable: Boolean,
    newVersion: String,
    updateUrl: String,
    releaseNotes: String,
    onDismiss: () -> Unit
) {
    if (isAvailable) {
        val context = LocalContext.current
        AlertDialog(
            onDismissRequest = onDismiss,
            title = { Text("Nueva versión detectada") },
            text = { Text("Se ha detectado una nueva versión ($newVersion) en GitHub.\n\n$releaseNotes") },
            confirmButton = {
                Button(onClick = {
                    val intent = Intent(Intent.ACTION_VIEW, Uri.parse(updateUrl))
                    context.startActivity(intent)
                    onDismiss()
                }) {
                    Text("Descargar")
                }
            },
            dismissButton = {
                TextButton(onClick = onDismiss) {
                    Text("Ignorar", color = MaterialTheme.colorScheme.onSurface.copy(alpha = 0.7f))
                }
            },
            containerColor = Color(0xFF1E1E1E),
            titleContentColor = Color.White,
            textContentColor = Color.White.copy(alpha = 0.8f)
        )
    }
}
