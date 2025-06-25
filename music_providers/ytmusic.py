import random
from fastapi import HTTPException
from ytmusicapi import YTMusic
from music_providers.base import MusicProvider


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
        tracks = []

        random.shuffle(genres)

        banned_words = {
            "baby", "sleep", "therapy", "meditation", "background", "healing", "library",
            "delta waves", "focus", "relax", "raaga", "raag", "mantra", "instrumental", "study",
            "worship", "work", "dj", "royalty", "yoga", "spa", "documentary", "cafe",
            "music for", "bgm", "calm", "cleanmindsounds", "channel", "sound", "everyday",
            "backing", "track", "progression", "lesson", "loop", "beats", "guitar solo",
            "guitar backing", "storytelling", "guitar",
            "chord", "practice", "accompaniment", "vocal removed"
        }

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

            title = r["title"].lower()
            artist = r["artists"][0]["name"].lower()

            if any(
                    bad in title for bad in banned_words) or any(
                    bad in artist for bad in banned_words):
                continue

            track = {
                "videoId": video_id,
                "title": r["title"],
                "artist": r["artists"][0]["name"],
                "url": f"https://music.youtube.com/watch?v={video_id}"
            }

            tracks.append(track)
            seen_ids.add(video_id)

            if len(tracks) >= limit:
                return tracks

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
