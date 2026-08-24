import androidx.compose.runtime.collectAsState

// Inside MainScreen:
// val userStats by profileViewModel.userStats.collectAsState()
// viewModel.selectTrack(track.trackName ?: "", track.artistName ?: "", userStats.apiPreference)
