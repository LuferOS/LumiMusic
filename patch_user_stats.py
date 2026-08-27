import re

with open("app/src/main/java/com/example/data/local/UserStats.kt", "r") as f:
    content = f.read()

target = "val hasSeenOnboarding: Boolean = false"
replacement = """val hasSeenOnboarding: Boolean = false,
    val startupTab: Int = 0,
    val navOrder: String = "0,1,2",
    val playerFont: String = "Default",
    val visualizerType: String = "Ondas",
    val visualizerColor: String = "Dinámico\""""

if "startupTab" not in content:
    content = content.replace(target, replacement)
    with open("app/src/main/java/com/example/data/local/UserStats.kt", "w") as f:
        f.write(content)

with open("app/src/main/java/com/example/data/local/UserStatsDao.kt", "r") as f:
    dao = f.read()

if "updateCustomization" not in dao:
    dao = dao.replace(
        "suspend fun updateOnboardingStatus(seen: Boolean)\n}",
        "suspend fun updateOnboardingStatus(seen: Boolean)\n\n    @Query(\"UPDATE user_stats SET startupTab = :tab, navOrder = :order, playerFont = :font, visualizerType = :vType, visualizerColor = :vColor WHERE id = 1\")\n    suspend fun updateCustomization(tab: Int, order: String, font: String, vType: String, vColor: String)\n}"
    )
    with open("app/src/main/java/com/example/data/local/UserStatsDao.kt", "w") as f:
        f.write(dao)

with open("app/src/main/java/com/example/data/local/AppDatabase.kt", "r") as f:
    db = f.read()
db = re.sub(r"version = \d+", "version = 7", db)
with open("app/src/main/java/com/example/data/local/AppDatabase.kt", "w") as f:
    f.write(db)
