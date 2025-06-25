from fastapi import APIRouter, Query, HTTPException

from schemas.schemas import PromptRequest
from gpt.mood_analyzer import analyze_mood
from music_providers import PROVIDERS
from schemas.enums import ProviderEnum
from schemas.schemas import PromptData
router = APIRouter()


@router.post("/analyze", tags=['Mood'])
async def analyze(prompt: PromptRequest):
    return await analyze_mood(prompt.text)


@router.post("/analyze-and-recommend", tags=['Mood'])
async def analyze_and_recommend(
        data: PromptData,
        provider: ProviderEnum = Query(..., description="Music recommendation service")
):
    try:
        mood_data = await analyze_mood(data.text)

        selected = PROVIDERS.get(provider.value)
        if not selected:
            raise HTTPException(status_code=400, detail=f"Unknown provider: {provider}")

        tracks = selected.recommend_tracks(**mood_data, limit=data.limit)
        return {"mood": mood_data, "tracks": tracks}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
