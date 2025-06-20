from typing import List

from pydantic import BaseModel, Field, field_validator


class PromptRequest(BaseModel):
    text: str


class PromptData(BaseModel):
    text: str
    limit: int = Field(10, ge=1, le=50)


class MoodData(BaseModel):
    mood: str
    valence: float = Field(0.0, ge=0, le=1)
    energy: float = Field(0.0, ge=0, le=1)
    genres: List[str]
    limit: int = Field(10, ge=1, le=50)
    query: str = Field(...)


class PlaylistCreation(BaseModel):
    name: str = Field(..., min_length=1, max_length=100, description="Playlist name (1–100 chars)")
    description: str = Field(..., max_length=300, description="Playlist description (max 300 chars)")

    @field_validator("name", "description", mode="before")
    def strip_whitespace(cls, v: str) -> str:
        return v.strip()


class TrackData(BaseModel):
    videoId: str
    title: str
    artist: str
    url: str


class PlaylistAddition(BaseModel):
    playlist_id: str = Field(..., min_length=1, max_length=100)
    track_list: List[TrackData]
