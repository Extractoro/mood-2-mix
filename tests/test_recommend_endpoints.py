import pytest
from httpx import AsyncClient, ASGITransport
from fastapi import status
from main import app


@pytest.mark.asyncio
async def test_recommend_songs_endpoint():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.post(
            "/recommend/songs?provider=ytmusic",
            json={"mood": "elated",
                  "valence": 0.9,
                  "energy": 0.9,
                  "genres": [
                      "pop",
                      "dance",
                      "upbeat"
                  ],
                  "limit": 10,
                  "query": "celebratory upbeat pop"})
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "mood" in data
    assert "tracks" in data
    assert isinstance(data["tracks"], list)
    assert len(data["tracks"]) == 10


@pytest.mark.asyncio
async def test_recommend_songs_endpoint_with_empty_data():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.post(
            "/recommend/songs?provider=ytmusic",
            json={}
        )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    data = response.json()
    assert "detail" in data
