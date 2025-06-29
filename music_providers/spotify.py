import os

import requests
from dotenv import load_dotenv
from fastapi import HTTPException

from music_providers.base import MusicProvider

load_dotenv()

SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
SPOTIFY_USER_ID = os.getenv("SPOTIFY_USER_ID")


class SpotifyProvider(MusicProvider):
    def __init__(self, access_token: str, user_id: str):
        self.token = access_token
        self.user_id = user_id
        self.base_url = "https://api.spotify.com/v1"
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }

    def recommend_tracks(
            self, mood: str, genres: list[str],
            valence: float, energy: float,
            limit: int = 10
    ):
        return ("Unfortunately, Spotify does not provide the ability to recommend tracks."
                "Please, choose another provider.")

    def create_playlist_with_tracks(
            self,
            name: str,
            description: str
    ) -> str:
        try:
            data = {
                "name": name,
                "description": description,
                "public": True
            }

            response = requests.post(
                url=f'{self.base_url}/users/{self.user_id}/playlists',
                headers=self.headers,
                json=data
            )

            if response.status_code == 401:
                raise HTTPException(
                    status_code=401,
                    detail="Access token expired. Please reauthorize."
                )

            if response.status_code != 201:
                raise HTTPException(status_code=response.status_code, detail=response.json())

            return response.json()
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    def search_track_in_spotify(
            self,
            title: str,
            artist: str,
            access_token: str
    ):
        try:
            query = f'{title} {artist}'
            url = "https://api.spotify.com/v1/search"
            headers = {
                "Authorization": f"Bearer {access_token}"
            }
            params = {
                "q": query,
                "type": "track",
                "limit": 1
            }

            response = requests.get(url=url, params=params, headers=headers)

            if response.status_code == 401:
                raise HTTPException(
                    status_code=401, detail="Access token expired. Please reauthorize.")
            if response.status_code != 200:
                return None

            result = response.json()["tracks"]["items"]
            if not result:
                return None
            return result[0]["uri"]

        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
