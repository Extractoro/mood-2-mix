from music_providers.spotify import SpotifyProvider
from music_providers.ytmusic import YouTubeMusicProvider

PROVIDERS = {
    "ytmusic": YouTubeMusicProvider(),
    # 'spotify': SpotifyProvider()
    # "deezer": DeezerMusicProvider() — потім
}