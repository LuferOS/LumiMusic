package com.example.ui.screens

import androidx.compose.foundation.background
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.rounded.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp

@Composable
fun OnboardingScreen(
    primaryColor: Color,
    onComplete: () -> Unit
) {
    var step by remember { mutableStateOf(1) }

    Box(
        modifier = Modifier
            .fillMaxSize()
            .background(Color(0xFF121212))
            .padding(24.dp),
        contentAlignment = Alignment.Center
    ) {
        androidx.compose.animation.AnimatedContent(
            targetState = step,
            label = "onboarding_step"
        ) { targetStep ->
            when (targetStep) {
                1 -> OnboardingPage(
                    title = "Bienvenido a LumiMusic",
                    subtitle = "Tu nueva experiencia musical inteligente propulsada por Alya Core.",
                    icon = Icons.Rounded.MusicNote,
                    color = primaryColor
                )
                2 -> OnboardingPage(
                    title = "Búsqueda Rápida",
                    subtitle = "Encuentra cualquier canción o pódcast al instante en la pestaña Online.",
                    icon = Icons.Rounded.Search,
                    color = primaryColor
                )
                3 -> OnboardingPage(
                    title = "Memoria Inteligente",
                    subtitle = "Descarga en caché mientras escuchas para no gastar datos móviles al repetir tu música favorita.",
                    icon = Icons.Rounded.DataSaverOn,
                    color = primaryColor
                )
                else -> OnboardingPage(
                    title = "Personalización",
                    subtitle = "Ajusta las transiciones, el crossfade y los colores de la aplicación desde tu Perfil.",
                    icon = Icons.Rounded.Palette,
                    color = primaryColor
                )
            }
        }

        // Bottom Controls
        Row(
            modifier = Modifier
                .align(Alignment.BottomCenter)
                .fillMaxWidth()
                .padding(bottom = 32.dp),
            horizontalArrangement = Arrangement.SpaceBetween,
            verticalAlignment = Alignment.CenterVertically
        ) {
            TextButton(
                onClick = onComplete,
                modifier = Modifier.padding(8.dp)
            ) {
                Text("Saltar", color = Color.White.copy(alpha = 0.5f))
            }
            
            Row(horizontalArrangement = Arrangement.Center) {
                for (i in 1..4) {
                    Box(
                        modifier = Modifier
                            .padding(4.dp)
                            .size(if (step == i) 12.dp else 8.dp)
                            .clip(CircleShape)
                            .background(if (step == i) primaryColor else Color.White.copy(alpha = 0.3f))
                    )
                }
            }
            
            Button(
                onClick = { 
                    if (step < 4) step++ else onComplete() 
                },
                colors = ButtonDefaults.buttonColors(containerColor = primaryColor, contentColor = Color.Black),
                shape = RoundedCornerShape(24.dp),
                modifier = Modifier.padding(8.dp)
            ) {
                Text(if (step < 4) "Siguiente" else "Empezar", fontWeight = FontWeight.Bold)
            }
        }
    }
}

@Composable
fun OnboardingPage(title: String, subtitle: String, icon: androidx.compose.ui.graphics.vector.ImageVector, color: Color) {
    Column(
        horizontalAlignment = Alignment.CenterHorizontally,
        verticalArrangement = Arrangement.Center,
        modifier = Modifier.padding(bottom = 80.dp)
    ) {
        Icon(
            imageVector = icon,
            contentDescription = null,
            modifier = Modifier.size(120.dp),
            tint = color
        )
        Spacer(modifier = Modifier.height(32.dp))
        Text(
            text = title,
            style = MaterialTheme.typography.headlineMedium,
            fontWeight = FontWeight.Bold,
            color = Color.White,
            textAlign = TextAlign.Center
        )
        Spacer(modifier = Modifier.height(16.dp))
        Text(
            text = subtitle,
            style = MaterialTheme.typography.bodyLarge,
            color = Color.White.copy(alpha = 0.7f),
            textAlign = TextAlign.Center
        )
    }
}
