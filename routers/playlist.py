import requests
from fastapi import APIRouter, Query, HTTPException, Depends, Header

from music_providers import PROVIDERS, SpotifyProvider
from schemas.enums import ProviderEnum
from schemas.schemas import PlaylistCreation, PlaylistAddition
from utils.get_spotify_token_from_header import get_spotify_token_from_header

router = APIRouter()


@router.post("/create-spotify", tags=['Spotify'])
def create_playlist(
        playlist_data: PlaylistCreation,
        provider: ProviderEnum = Query(ProviderEnum.spotify, description="Music recommendation service"),
        access_token: str = Depends(get_spotify_token_from_header),
        user_id: str = Header(..., description="Spotify user ID")
):
    try:
        if provider == ProviderEnum.spotify:
            sp = SpotifyProvider(access_token=access_token, user_id=user_id)
            playlist = sp.create_playlist_with_tracks(**playlist_data.model_dump())
            return {"playlist": playlist}

        selected = PROVIDERS.get(provider.value)
        if not selected:
            raise HTTPException(status_code=400, detail=f"Unknown provider: {provider}")

        playlist = selected.create_playlist_with_tracks(**playlist_data.model_dump())

        return {"playlist_data": playlist_data, "playlist": playlist}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/{playlist_id}/tracks", tags=['Spotify'])
def add_tracks_to_playlist(
        playlist_data: PlaylistAddition,
        provider: ProviderEnum = Query(ProviderEnum.spotify, description="Music recommendation service"),
        access_token: str = Depends(get_spotify_token_from_header),
        user_id: str = Header(..., description="Spotify user ID")
):
    try:
        if provider == ProviderEnum.spotify:
            sp = SpotifyProvider(access_token=access_token, user_id=user_id)
            spotify_ids = []

            for track in playlist_data.track_list:
                title = track.title
                artist = track.artist
                spotify_id = sp.search_track_in_spotify(title, artist, access_token)
                spotify_ids.append(spotify_id)

            response = requests.post(
                f'https://api.spotify.com/v1/playlists/{playlist_data.playlist_id}/tracks',
                headers={'Authorization': f'Bearer {access_token}'},
                json={'uris': spotify_ids}
            )

            return response.json()

        return None # //


    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
