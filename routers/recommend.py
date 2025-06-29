from fastapi import APIRouter, Query, HTTPException

from music_providers import PROVIDERS
from schemas.enums import ProviderEnum
from schemas.schemas import MoodData, RecommendResponse

router = APIRouter()


@router.post("/songs", tags=['Recommend songs'], response_model=RecommendResponse)
def recommend_songs(
        mood_data: MoodData,
        provider: ProviderEnum = Query(..., description="Music recommendation service")
):
    try:
        selected = PROVIDERS.get(provider.value)
        if not selected:
            raise HTTPException(status_code=400, detail=f"Unknown provider: {provider}")

        tracks = selected.recommend_tracks(**mood_data.model_dump())
        return {"mood": mood_data, "tracks": tracks}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
