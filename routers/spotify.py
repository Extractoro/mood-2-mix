import os

import requests
from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import JSONResponse
from dotenv import load_dotenv

router = APIRouter()
load_dotenv()

SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
REDIRECT_URI = os.getenv("REDIRECT_URI")
SCOPES = "playlist-modify-public playlist-modify-private"

@router.get("/auth/link", tags=["Auth"])
async def get_spotify_auth_link():
    auth_url = (
        f'https://accounts.spotify.com/authorize'
        f'?client_id={SPOTIFY_CLIENT_ID}'
        f'&response_type=code'
        f'&redirect_uri={REDIRECT_URI}'
        f"&scope={SCOPES.replace(' ', '%20')}"
    )
    return JSONResponse(content={"url": auth_url})

@router.get("/callback", tags=["Auth"])
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