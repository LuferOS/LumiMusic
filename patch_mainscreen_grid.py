import re

with open("app/src/main/java/com/example/MainActivity.kt", "r") as f:
    content = f.read()

# Make sure grid imports are present
if "import androidx.compose.foundation.lazy.grid.LazyVerticalGrid" not in content:
    content = content.replace("import androidx.compose.foundation.lazy.LazyColumn", "import androidx.compose.foundation.lazy.LazyColumn\nimport androidx.compose.foundation.lazy.grid.LazyVerticalGrid\nimport androidx.compose.foundation.lazy.grid.GridCells\nimport androidx.compose.foundation.lazy.grid.items")

old_lazy_column = """            if (sState is com.example.viewmodel.SearchState.Success) {
                LazyColumn(
                    modifier = Modifier.fillMaxSize(),
                    contentPadding = PaddingValues(bottom = 100.dp)
                ) {
                    items(sState.results) { track ->"""

new_lazy_grid = """            if (sState is com.example.viewmodel.SearchState.Success) {
                LazyVerticalGrid(
                    columns = GridCells.Adaptive(minSize = 350.dp),
                    modifier = Modifier.fillMaxSize(),
                    contentPadding = PaddingValues(bottom = 100.dp)
                ) {
                    items(sState.results) { track ->"""

content = content.replace(old_lazy_column, new_lazy_grid)

with open("app/src/main/java/com/example/MainActivity.kt", "w") as f:
    f.write(content)
