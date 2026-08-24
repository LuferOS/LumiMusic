import re

# Update UserStats.kt
with open("app/src/main/java/com/example/data/local/UserStats.kt", "r") as f:
    content = f.read()
if "transitionType" not in content:
    content = content.replace(
        "val extractAlbumColor: Boolean = true",
        "val extractAlbumColor: Boolean = true,\n    val transitionType: String = \"Gapless\",\n    val transitionDuration: Int = 3"
    )
with open("app/src/main/java/com/example/data/local/UserStats.kt", "w") as f:
    f.write(content)

# Update AppDatabase.kt
with open("app/src/main/java/com/example/data/local/AppDatabase.kt", "r") as f:
    content = f.read()
content = content.replace("version = 4", "version = 5")
with open("app/src/main/java/com/example/data/local/AppDatabase.kt", "w") as f:
    f.write(content)

# Update UserStatsDao.kt
with open("app/src/main/java/com/example/data/local/UserStatsDao.kt", "r") as f:
    content = f.read()
if "updateTransitions" not in content:
    content = content.replace(
        "suspend fun updateAppearance(primary: String, bg: String, font: String, neon: Boolean, extract: Boolean)",
        "suspend fun updateAppearance(primary: String, bg: String, font: String, neon: Boolean, extract: Boolean)\n\n    @Query(\"UPDATE user_stats SET transitionType = :type, transitionDuration = :duration WHERE id = 1\")\n    suspend fun updateTransitions(type: String, duration: Int)"
    )
with open("app/src/main/java/com/example/data/local/UserStatsDao.kt", "w") as f:
    f.write(content)
