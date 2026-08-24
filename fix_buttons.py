import re

with open("app/src/main/java/com/example/ui/components/FullScreenPlayer.kt", "r") as f:
    content = f.read()

# Replace MoreVert with a transparent Spacer to maintain center alignment
target_more = """                IconButton(onClick = { /* TODO */ }) {
                    Icon(Icons.Rounded.MoreVert, contentDescription = "More", tint = Color.White)
                }"""
replacement_more = """                Spacer(modifier = Modifier.size(48.dp)) // To balance the back button"""
content = content.replace(target_more, replacement_more)

# Remove the Bottom Action Icons entirely (Devices, Share, Queue)
target_bottom_actions = """            // Bottom Action Icons
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.SpaceBetween,
                verticalAlignment = Alignment.CenterVertically
            ) {
                IconButton(onClick = { /* Devices */ }) {
                    Icon(Icons.Rounded.Devices, contentDescription = "Devices", tint = Color.White.copy(alpha = 0.7f), modifier = Modifier.size(20.dp))
                }
                Row {
                    IconButton(onClick = { /* Share */ }) {
                        Icon(Icons.Rounded.Share, contentDescription = "Share", tint = Color.White.copy(alpha = 0.7f), modifier = Modifier.size(20.dp))
                    }
                    IconButton(onClick = { /* Queue */ }) {
                        Icon(Icons.Rounded.QueueMusic, contentDescription = "Queue", tint = Color.White.copy(alpha = 0.7f), modifier = Modifier.size(20.dp))
                    }
                }
            }

            Spacer(modifier = Modifier.height(16.dp))"""
content = content.replace(target_bottom_actions, "")

with open("app/src/main/java/com/example/ui/components/FullScreenPlayer.kt", "w") as f:
    f.write(content)
