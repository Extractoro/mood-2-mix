from typing import List

from pydantic import BaseModel, Field, field_validator, HttpUrl


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
    description: str = Field(
        ..., max_length=300, description="Playlist description (max 300 chars)")

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
    track_list: list[TrackData]


class MoodAnalyzeResponse(BaseModel):
    mood: str
    valence: float
    energy: float
    genres: list[str]
    query: str


class MoodAnalyzeRecommendResponse(BaseModel):
    mood: MoodAnalyzeResponse
    tracks: list[TrackData]


class RecommendResponse(BaseModel):
    mood: MoodAnalyzeResponse
    tracks: list[TrackData]


class SpotifyAuthLinkResponse(BaseModel):
    url: str


class SpotifyCallbackResponse(BaseModel):
    access_token: str
    refresh_token: str
    expires_in: int
    scope: str
    user_id: str
    display_name: str


class ExternalUrls(BaseModel):
    spotify: HttpUrl


class Playlist(BaseModel):
    collaborative: bool
    description: str
    external_urls: ExternalUrls
    href: HttpUrl
    id: str
    name: str
    type: str
    uri: str
    public: bool
    snapshot_id: str


class PlaylistCreationResponse(BaseModel):
    playlist: Playlist


class PlaylistAdditionResponse(BaseModel):
    snapshot_id: str


class PlaylistPromptToPlaylistResponse(BaseModel):
    detail: str
    playlist_url: HttpUrl
