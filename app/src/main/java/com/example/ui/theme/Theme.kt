package com.example.ui.theme

import android.os.Build
import androidx.compose.foundation.isSystemInDarkTheme
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.darkColorScheme
import androidx.compose.material3.dynamicDarkColorScheme
import androidx.compose.material3.dynamicLightColorScheme
import androidx.compose.material3.lightColorScheme
import androidx.compose.runtime.Composable
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.platform.LocalContext

@Composable
fun MyApplicationTheme(
    primaryColorHex: String = "#00FFFF",
    bgColorHex: String = "#000000",
    fontPref: String = "Default",
    dynamicColor: Boolean = false,
    content: @Composable () -> Unit
) {
    val primaryColor = try { Color(android.graphics.Color.parseColor(primaryColorHex)) } catch(e: Exception) { Color(0xFF00FFFF) }
    val bgColor = try { Color(android.graphics.Color.parseColor(bgColorHex)) } catch(e: Exception) { Color.Black }
    
    val colorScheme = darkColorScheme(
        primary = primaryColor,
        background = bgColor,
        surface = bgColor,
        surfaceVariant = Color(0xFF1E1E1E), // Slightly lighter for cards
        onBackground = Color.White,
        onSurface = Color.White,
        onPrimary = Color.Black
    )

    MaterialTheme(
        colorScheme = colorScheme,
        typography = getTypography(fontPref),
        content = content
    )
}
