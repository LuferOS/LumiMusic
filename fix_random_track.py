import re

with open("app/src/main/java/com/example/viewmodel/MainViewModel.kt", "r") as f:
    content = f.read()

content = content.replace("val response = api.search(term = query, limit = 25)", "val response = iTunesApi.searchTracks(term = query)")

with open("app/src/main/java/com/example/viewmodel/MainViewModel.kt", "w") as f:
    f.write(content)
