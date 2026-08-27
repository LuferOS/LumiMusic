import re

with open("app/src/main/java/com/example/player/PlaybackService.kt", "r") as f:
    content = f.read()

target = """    private fun applyTransitionEffects(player: ExoPlayer) {
        serviceScope.launch {
            val stats = AppDatabase.getDatabase(this@PlaybackService).userStatsDao().getStatsDirect()
            val transitionType = stats?.transitionType ?: "Gapless"
            val durationSeconds = stats?.transitionDuration ?: 3"""

replacement = """    private var currentTransitionType = "Gapless"
    private var currentTransitionDuration = 3
    
    override fun onCreate() {
        super.onCreate()
        // Cargar configuración de transiciones una vez (y escuchar cambios en background)
        serviceScope.launch {
            AppDatabase.getDatabase(this@PlaybackService).userStatsDao().getStats().collect { stats ->
                currentTransitionType = stats?.transitionType ?: "Gapless"
                currentTransitionDuration = stats?.transitionDuration ?: 3
            }
        }"""

content = content.replace("override fun onCreate() {", replacement)

# Now remove the DB call inside applyTransitionEffects
target_apply = """    private fun applyTransitionEffects(player: ExoPlayer) {
        serviceScope.launch {
            val stats = AppDatabase.getDatabase(this@PlaybackService).userStatsDao().getStatsDirect()
            val transitionType = stats?.transitionType ?: "Gapless"
            val durationSeconds = stats?.transitionDuration ?: 3"""

replace_apply = """    private fun applyTransitionEffects(player: ExoPlayer) {
        serviceScope.launch {
            val transitionType = currentTransitionType
            val durationSeconds = currentTransitionDuration"""
            
content = content.replace(target_apply, replace_apply)

with open("app/src/main/java/com/example/player/PlaybackService.kt", "w") as f:
    f.write(content)
