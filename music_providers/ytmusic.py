import random
from fastapi import HTTPException
from ytmusicapi import YTMusic
from music_providers.base import MusicProvider
from utils.contains_banned_word import contains_banned_word


class YouTubeMusicProvider(MusicProvider):
    def __init__(self):
        self.api = YTMusic()
        self.valid_genres = self._load_valid_genres()

    def _load_valid_genres(self) -> list[str]:
        categories = self.api.get_mood_categories()
        genres = categories.get("Genres", [])
        return [genre["title"].lower() for genre in genres]

    def recommend_tracks(
            self,
            mood: str,
            genres: list[str],
            valence: float,
            energy: float,
            limit: int = 10,
            query: str = None,
    ):
        seen_ids = set()
        seen_pairs = set()
        tracks = []

        random.shuffle(genres)

        # banned_words = {
        #     "baby", "sleep", "therapy", "meditation", "background", "healing", "library",
        #     "delta waves", "focus", "relax", "raaga", "raag", "mantra", "instrumental", "study",
        #     "worship", "work", "dj", "royalty", "yoga", "spa", "documentary", "cafe",
        #     "music for", "bgm", "calm", "cleanmindsounds", "channel", "sound", "everyday",
        #     "backing", "track", "progression", "lesson", "loop", "beats", "guitar solo",
        #     "guitar backing", "storytelling", "guitar", "jazz", 'buddha', "acoustic",
        #     "chord", "practice", "accompaniment", "vocal removed"
        # }

        def get_banned_words(valence: float, energy: float) -> set[str]:
            default_banned = {
                "karaoke", "backing", "loop", "practice", "sfx", "effect",
                "lesson", "vocal removed", "test tone", "tone", "frequency", "hz"
            }

            soft_banned = {
                "sleep", "meditation", "therapy", "instrumental", "relax",
                "binaural", "delta waves", "yoga", "spa", "sound", "calm", "guitar", "acoustic"
            }

            hard_banned = {
                "baby", "raaga", "raag", "mantra", "chant", "white noise", "library", "noise"
            }

            banned = set(default_banned)

            if energy >= 0.4:
                banned |= soft_banned
            if energy > 0.6 or valence < 0.4:
                banned |= hard_banned

            return banned

        def is_artist_blacklisted(artist: str) -> bool:
            blacklist = {
                "nature sounds", "baby sleep music", "white noise masters",
                "relaxing piano life", "meditative mind", "personal power sleep serenity"
            }
            return artist.lower().strip() in blacklist

        irrelevant_words = {
            "fitness", "nonstop", "gym", "royalty", "background", "motivational",
            "christian", "instrumental", "dj mix", "megamix", "library",
            "children", "kid", "nursery", "baby", "abc", "bounce patrol", "elmo", "happy birthday",
            "lah", "bubbles and friends", "massacaresound"
        }

        def is_irrelevant(title: str, artist: str) -> bool:
            text = f"{title} {artist}".lower()
            return any(word in text for word in irrelevant_words)

        banned_words = get_banned_words(valence, energy)

        if query:
            query = f"{query}"
        else:
            query = f"{mood} {genres[0]} {genres[1]} {genres[2]}"

        suggestions = self.api.get_search_suggestions(query)
        if suggestions:
            query = suggestions[0]

        results = self.api.search(query, filter="songs")

        for r in results:
            video_id = r.get("videoId")
            if not video_id or video_id in seen_ids:
                continue

            if "title" not in r or not r.get("artists"):
                continue

            title = r["title"].strip().lower()
            artist = r["artists"][0]["name"].strip().lower()

            if (
                    contains_banned_word(title, banned_words)
                    or contains_banned_word(artist, banned_words)
            ):
                print(f"Filtered by keyword: {title} – {artist}")
                continue

            if is_artist_blacklisted(artist):
                print(f"Filtered by artist: {artist}")
                continue

            if is_irrelevant(title, artist):
                print(f"Filtered as irrelevant: {title} – {artist}")
                continue

            if (title, artist) in seen_pairs:
                continue

            track = {
                "videoId": video_id,
                "title": r["title"],
                "artist": r["artists"][0]["name"],
                "url": f"https://music.youtube.com/watch?v={video_id}"
            }

            tracks.append(track)
            seen_ids.add(video_id)
            seen_pairs.add((title, artist))

            if len(tracks) >= limit:
                break

        return tracks

    def create_playlist_with_tracks(
            self,
            name: str,
            description: str
    ) -> str:
        raise HTTPException(
            status_code=500,
            detail="Unfortunately, Youtube Music does not provide "
                   "the ability to create playlists. "
                   "Please, choose another provider."
        )
