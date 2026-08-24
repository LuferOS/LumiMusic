import re

with open("app/src/main/java/com/example/ui/components/FullScreenPlayer.kt", "r") as f:
    content = f.read()

# Update signature to remove `lyrics: String`
content = content.replace("""    dominantColor: Color?,
    lyrics: String,
    viewModel: MainViewModel,""", """    dominantColor: Color?,
    viewModel: MainViewModel,""")

# Update imports
imports = """import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.itemsIndexed
import androidx.compose.foundation.lazy.rememberLazyListState
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import com.example.utils.LrcLine"""

if "import com.example.utils.LrcLine" not in content:
    content = content.replace("import com.example.viewmodel.MainViewModel", imports + "\nimport com.example.viewmodel.MainViewModel")

# Add isLyricsExpanded state
target_states = """    var currentPosition by remember { mutableStateOf(0L) }
    var duration by remember { mutableStateOf(0L) }
    var artworkUri by remember { mutableStateOf<android.net.Uri?>(null) }"""

replacement_states = target_states + """
    var isLyricsExpanded by remember { mutableStateOf(false) }
    val lrcState by viewModel.lrcState.collectAsStateWithLifecycle()
    val lyricsState by viewModel.lyricsState.collectAsStateWithLifecycle()"""

content = content.replace(target_states, replacement_states)

# Update delay loop for smoother progress and lyrics
target_delay = """            if (controller?.isPlaying == true) {
                currentPosition = controller.currentPosition.coerceAtLeast(0L)
            }
            delay(1000)"""
replacement_delay = """            if (controller?.isPlaying == true) {
                currentPosition = controller.currentPosition.coerceAtLeast(0L)
            }
            delay(100) // Fast update for smooth lyrics and progress"""
content = content.replace(target_delay, replacement_delay)

# Replace the Lyrics box at the bottom
target_lyrics_box = """            Box(
                modifier = Modifier
                    .fillMaxWidth()
                    .heightIn(min = 90.dp)
                    .clip(RoundedCornerShape(16.dp))
                    .background(Color.White.copy(alpha = 0.1f))
                    .clickable { /* Future: expand lyrics */ }
                    .padding(16.dp)
            ) {
                Column {
                    Row(
                        modifier = Modifier.fillMaxWidth(),
                        horizontalArrangement = Arrangement.SpaceBetween
                    ) {
                        Text(
                            "Lyrics", 
                            style = MaterialTheme.typography.titleMedium.copy(fontWeight = FontWeight.Bold), 
                            color = Color.White
                        )
                        Row {
                            Icon(Icons.Rounded.Share, contentDescription = null, tint = Color.White, modifier = Modifier.size(18.dp))
                            Spacer(modifier = Modifier.width(16.dp))
                            Icon(Icons.Rounded.OpenInFull, contentDescription = null, tint = Color.White, modifier = Modifier.size(18.dp))
                        }
                    }
                    Spacer(modifier = Modifier.height(8.dp))
                    
                    val lyricsLines = lyrics.lines()
                    val peekLyrics = if (lyrics.isNotBlank() && lyrics != "Failed to load lyrics") {
                        lyricsLines.take(2).joinToString("\\n")
                    } else {
                        lyrics
                    }
                    Text(
                        text = peekLyrics,
                        style = MaterialTheme.typography.bodyLarge,
                        color = Color.White.copy(alpha = 0.7f),
                        maxLines = 2,
                        overflow = TextOverflow.Ellipsis
                    )
                }
            }"""

replacement_lyrics_box = """            Box(
                modifier = Modifier
                    .fillMaxWidth()
                    .heightIn(min = 90.dp)
                    .clip(RoundedCornerShape(16.dp))
                    .background(if (isLyricsExpanded) Color.Black.copy(alpha = 0.6f) else Color.White.copy(alpha = 0.1f))
                    .clickable { isLyricsExpanded = !isLyricsExpanded }
                    .padding(16.dp)
                    .weight(if (isLyricsExpanded) 1f else 0.001f, fill = false)
            ) {
                Column(modifier = Modifier.fillMaxSize()) {
                    Row(
                        modifier = Modifier.fillMaxWidth(),
                        horizontalArrangement = Arrangement.SpaceBetween,
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        Text(
                            "Lyrics", 
                            style = MaterialTheme.typography.titleMedium.copy(fontWeight = FontWeight.Bold), 
                            color = Color.White
                        )
                        Icon(
                            imageVector = if (isLyricsExpanded) Icons.Rounded.CloseFullscreen else Icons.Rounded.OpenInFull, 
                            contentDescription = "Expand", 
                            tint = Color.White, 
                            modifier = Modifier.size(18.dp)
                        )
                    }
                    Spacer(modifier = Modifier.height(16.dp))
                    
                    if (lrcState != null) {
                        val activeLineIndex by remember(currentPosition) {
                            derivedStateOf {
                                val lines = lrcState!!
                                val idx = lines.indexOfLast { it.timeMs <= currentPosition }
                                if (idx == -1) 0 else idx
                            }
                        }
                        
                        val listState = rememberLazyListState()
                        LaunchedEffect(activeLineIndex) {
                            if (isLyricsExpanded && lrcState!!.isNotEmpty()) {
                                // Smooth scroll to keep active line near center
                                val targetIdx = maxOf(0, activeLineIndex - 2)
                                listState.animateScrollToItem(targetIdx)
                            }
                        }
                        
                        LazyColumn(
                            state = listState,
                            modifier = Modifier.fillMaxSize(),
                            contentPadding = PaddingValues(bottom = if (isLyricsExpanded) 64.dp else 0.dp)
                        ) {
                            itemsIndexed(lrcState!!) { index, line ->
                                val isActive = index == activeLineIndex
                                val alpha = if (isActive) 1f else 0.4f
                                val scale = if (isActive) 1.05f else 1f
                                Text(
                                    text = line.text,
                                    style = MaterialTheme.typography.headlineSmall.copy(fontWeight = if (isActive) FontWeight.Bold else FontWeight.Medium),
                                    color = Color.White.copy(alpha = alpha),
                                    modifier = Modifier
                                        .padding(vertical = 8.dp)
                                        .graphicsLayer {
                                            scaleX = scale
                                            scaleY = scale
                                        }
                                )
                            }
                        }
                    } else {
                        val lyricsText = lyricsState ?: "Loading..."
                        val peekLyrics = if (!isLyricsExpanded && lyricsText.isNotBlank() && lyricsText != "Failed to load lyrics") {
                            lyricsText.lines().take(2).joinToString("\\n")
                        } else {
                            lyricsText
                        }
                        Text(
                            text = peekLyrics,
                            style = MaterialTheme.typography.bodyLarge,
                            color = Color.White.copy(alpha = 0.7f),
                            maxLines = if (isLyricsExpanded) Int.MAX_VALUE else 2,
                            overflow = if (isLyricsExpanded) TextOverflow.Clip else TextOverflow.Ellipsis
                        )
                    }
                }
            }"""

content = content.replace(target_lyrics_box, replacement_lyrics_box)

with open("app/src/main/java/com/example/ui/components/FullScreenPlayer.kt", "w") as f:
    f.write(content)
