import pytest
from httpx import AsyncClient, ASGITransport
from fastapi import status
from main import app


@pytest.mark.asyncio
async def test_analyze_endpoint():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.post(
            "/mood/analyze",
            json={"text": "I'm feeling a bit nostalgic and reflective today"})
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "mood" in data
    assert "valence" in data
    assert "energy" in data
    assert "genres" in data
    assert "query" in data


@pytest.mark.asyncio
async def test_analyze_endpoint_with_empty_text():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.post("/mood/analyze", json={"text": ""})
    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    data = response.json()
    assert "detail" in data
    assert "Empty prompt" in data["detail"]


@pytest.mark.asyncio
async def test_analyze_and_recommend_ytmusic_endpoint():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.post(
            "/mood/analyze-and-recommend?provider=ytmusic",
            json={"text": "I'm feeling a bit nostalgic and reflective today", "limit": 10})
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "mood" in data
    assert "tracks" in data
    assert isinstance(data["tracks"], list)
