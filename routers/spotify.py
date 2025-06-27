import os

import requests
from dotenv import load_dotenv
from fastapi import APIRouter, Query, HTTPException, Depends, Header
from fastapi.responses import JSONResponse

from gpt.mood_analyzer import analyze_mood
from music_providers import SpotifyProvider, PROVIDERS
from schemas.enums import ProviderEnum
from schemas.schemas import PlaylistCreation, PlaylistAddition, PromptData, MoodData, TrackData
from utils.get_spotify_token_from_header import get_spotify_token_from_header
from utils.spotify_list_ids import get_spotify_track_uris

router = APIRouter()
load_dotenv()

SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
REDIRECT_URI = os.getenv("REDIRECT_URI")
SCOPES = "playlist-modify-public playlist-modify-private"


@router.get("/auth/link")
async def get_spotify_auth_link():
    auth_url = (
        f'https://accounts.spotify.com/authorize'
        f'?client_id={SPOTIFY_CLIENT_ID}'
        f'&response_type=code'
        f'&redirect_uri={REDIRECT_URI}'
        f"&scope={SCOPES.replace(' ', '%20')}"
    )
    return JSONResponse(content={"url": auth_url})


@router.get("/callback")
async def spotify_callback(
        code: str = Query(..., description="Code from the callback URL"),
):
    if not code:
        raise HTTPException(status_code=400, detail="Missing authorization code")

    token_response = requests.post(
        "https://accounts.spotify.com/api/token",
        data={
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": REDIRECT_URI,
            "client_id": SPOTIFY_CLIENT_ID,
            "client_secret": SPOTIFY_CLIENT_SECRET,
        },
        headers={
            "Content-Type": "application/x-www-form-urlencoded"
        }
    )

    if token_response.status_code != 200:
        raise HTTPException(status_code=token_response.status_code, detail=token_response.text)

    tokens = token_response.json()

    user_info = requests.get(
        "https://api.spotify.com/v1/me",
        headers={
            "Authorization": f"Bearer {tokens['access_token']}"
        }
    )

    if user_info.status_code != 200:
        raise HTTPException(status_code=user_info.status_code, detail=user_info.text)

    user = user_info.json()

    return JSONResponse(content={
        "access_token": tokens["access_token"],
        "refresh_token": tokens.get("refresh_token"),
        "expires_in": tokens["expires_in"],
        "scope": tokens["scope"],
        "user_id": user["id"],
        "display_name": user.get("display_name")
    })


@router.post("/create-playlist")
def create_playlist(
        playlist_data: PlaylistCreation,
        access_token: str = Depends(get_spotify_token_from_header),
        user_id: str = Header(..., description="Spotify user ID")
):
    try:
        sp = SpotifyProvider(access_token=access_token, user_id=user_id)
        playlist = sp.create_playlist_with_tracks(**playlist_data.model_dump())
        return {"playlist": playlist}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/{playlist_id}/tracks")
def add_tracks_to_playlist(
        playlist_data: PlaylistAddition,
        access_token: str = Depends(get_spotify_token_from_header),
        user_id: str = Header(..., description="Spotify user ID")
):
    try:
        sp = SpotifyProvider(access_token=access_token, user_id=user_id)
        print(playlist_data.track_list)
        spotify_uris = get_spotify_track_uris(sp, playlist_data.track_list, access_token)

        response = requests.post(
            f'https://api.spotify.com/v1/playlists/{playlist_data.playlist_id}/tracks',
            headers={'Authorization': f'Bearer {access_token}'},
            json={'uris': spotify_uris}
        )

        return response.json()

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/prompt-to-playlist")
async def prompt_to_playlist(
        data: PromptData,
        playlist_data_creation: PlaylistCreation,
        access_token: str = Depends(get_spotify_token_from_header),
        user_id: str = Header(..., description="Spotify user ID")
):
    try:
        mood_data = await analyze_mood(data.text)
        mood_data['limit'] = data.limit
        mood_data = MoodData(**mood_data)

        selected = PROVIDERS.get(ProviderEnum.ytmusic)
        tracks_list = selected.recommend_tracks(**mood_data.model_dump())
        track_objects = [TrackData(**track) for track in tracks_list]

        sp = SpotifyProvider(access_token=access_token, user_id=user_id)
        playlist_response = sp.create_playlist_with_tracks(**playlist_data_creation.model_dump())
        playlist_id = playlist_response["id"]
        playlist_url = playlist_response["external_urls"]["spotify"]

        print(track_objects)

        spotify_uris = get_spotify_track_uris(sp, track_objects, access_token)

        requests.post(
            f'https://api.spotify.com/v1/playlists/{playlist_id}/tracks',
            headers={'Authorization': f'Bearer {access_token}'},
            json={'uris': spotify_uris}
        )

        return {"detail": "Success! Now check your Spotify library.", "playlist_url": playlist_url}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
