import re

with open("app/src/main/java/com/example/data/local/AppDatabase.kt", "r") as f:
    content = f.read()

target = """@Database(entities = [UserStats::class], version = 3, exportSchema = false)
abstract class AppDatabase : RoomDatabase() {
    abstract fun userStatsDao(): UserStatsDao"""

replacement = """@Database(entities = [UserStats::class, LikedTrack::class], version = 4, exportSchema = false)
abstract class AppDatabase : RoomDatabase() {
    abstract fun userStatsDao(): UserStatsDao
    abstract fun likedTrackDao(): LikedTrackDao"""

content = content.replace(target, replacement)

with open("app/src/main/java/com/example/data/local/AppDatabase.kt", "w") as f:
    f.write(content)
