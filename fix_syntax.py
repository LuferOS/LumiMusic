import re

with open("app/src/main/java/com/example/viewmodel/MainViewModel.kt", "r") as f:
    content = f.read()

# Remove imports from middle and add to top
imports_to_move = """import android.app.Application
import androidx.lifecycle.AndroidViewModel
import com.example.data.local.AppDatabase
import com.example.data.local.LikedTrack
import kotlinx.coroutines.flow.SharingStarted
import kotlinx.coroutines.flow.stateIn"""

content = content.replace(imports_to_move, "")
content = content.replace("package com.example.viewmodel", "package com.example.viewmodel\n" + imports_to_move)

with open("app/src/main/java/com/example/viewmodel/MainViewModel.kt", "w") as f:
    f.write(content)

with open("app/src/main/java/com/example/ui/screens/LocalMusicScreen.kt", "r") as f:
    content = f.read()

imports_to_move_2 = """import com.example.viewmodel.MainViewModel"""
content = content.replace(imports_to_move_2, "")
content = content.replace("package com.example.ui.screens", "package com.example.ui.screens\n" + imports_to_move_2)

# Fix @Composable invocations can only happen from the context of a @Composable function in LocalMusicScreen
# I replaced `items` but maybe the parenthesis are messed up.
with open("app/src/main/java/com/example/ui/screens/LocalMusicScreen.kt", "w") as f:
    f.write(content)
