from dotenv import load_dotenv
from fastapi import FastAPI
from routers.mood import router as mood_router
from routers.recommend import router as recommend_router
from routers.spotify import router as spotify_router
from routers.playlist import router as playlist_router

load_dotenv()

app = FastAPI()

app.include_router(router=mood_router, prefix='/mood')
app.include_router(router=recommend_router, prefix='/recommend')
app.include_router(router=spotify_router, prefix='/spotify')
app.include_router(router=playlist_router, prefix='/playlist')