from music_providers.spotify import SpotifyProvider  # noqa: F401
from music_providers.ytmusic import YouTubeMusicProvider

PROVIDERS = {
    "ytmusic": YouTubeMusicProvider(),
    # "deezer": DeezerMusicProvider() — потім
}
