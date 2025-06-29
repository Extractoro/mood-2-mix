import pytest
from httpx import AsyncClient
from httpx._transports.asgi import ASGITransport
from fastapi import status
from unittest.mock import patch
from main import app


@pytest.mark.asyncio
async def test_create_spotify_playlist():
    transport = ASGITransport(app=app)
    headers = {
        "Authorization": "Bearer test_token",
        "user-id": "test_user"
    }

    playlist_data = {
        "name": "Test Playlist",
        "description": "Created in test"
    }

    mock_response = {
        "id": "playlist123",
        "name": "Test Playlist",
        "description": "Created in test",
        "collaborative": False,
        "external_urls": {"spotify": "https://open.spotify.com/playlist/playlist123"},
        "href": "https://api.spotify.com/v1/playlists/playlist123",
        "type": "playlist",
        "uri": "spotify:playlist:playlist123",
        "public": True,
        "snapshot_id": "mock_snapshot_id"
    }

    with patch("music_providers.spotify.requests.post") as mock_post:
        mock_post.return_value.status_code = 201
        mock_post.return_value.json.return_value = mock_response

        async with AsyncClient(transport=transport, base_url="http://test") as ac:
            response = await ac.post(
                "/spotify/create-playlist", headers=headers, json=playlist_data)

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "playlist" in data
    assert data["playlist"]["id"] == "playlist123"
