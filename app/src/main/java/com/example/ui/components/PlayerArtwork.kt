package com.example.ui.components

import android.net.Uri
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.rounded.MusicNote
import androidx.compose.material3.Icon
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.draw.shadow
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.unit.dp
import coil.compose.AsyncImage
import com.example.ui.theme.neonGlow

@OptIn(androidx.compose.animation.ExperimentalSharedTransitionApi::class)
@Composable
fun PlayerArtwork(
    artworkUri: Uri?,
    dominantColor: Color?,
    neonBorders: Boolean,
    isBatterySaverOn: Boolean,
    sharedTransitionScope: androidx.compose.animation.SharedTransitionScope,
    animatedVisibilityScope: androidx.compose.animation.AnimatedVisibilityScope
) {
    with(sharedTransitionScope) {
        val baseModifier = Modifier
            .fillMaxWidth()
            .aspectRatio(1f)
            .sharedElement(
                state = rememberSharedContentState(key = "album_art"),
                animatedVisibilityScope = animatedVisibilityScope
            )
        
                val enhancedModifier = if (!isBatterySaverOn && neonBorders) {
            baseModifier.neonGlow(color = dominantColor ?: Color.White, cornerRadius = 24.dp, enabled = true)
        } else if (!isBatterySaverOn) {
            baseModifier.shadow(elevation = 24.dp, shape = RoundedCornerShape(24.dp), spotColor = dominantColor ?: Color.Black)
        } else {
            baseModifier
        }

        Box(
            modifier = enhancedModifier
                .clip(RoundedCornerShape(24.dp))
                .background(Color.White.copy(alpha = 0.1f)),
            contentAlignment = Alignment.Center
        ) {
            if (artworkUri != null) {
                AsyncImage(
                    model = artworkUri,
                    contentDescription = "Album Art",
                    contentScale = ContentScale.Crop,
                    modifier = Modifier.fillMaxSize()
                )
            } else {
                Icon(
                    imageVector = Icons.Rounded.MusicNote,
                    contentDescription = null,
                    modifier = Modifier.size(100.dp),
                    tint = Color.White.copy(alpha = 0.3f)
                )
            }
        }
    }
}
