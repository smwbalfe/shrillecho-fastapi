from fastapi import APIRouter, Depends, Request, Response, FastAPI
from pydantic import BaseModel
from shrillecho.api.api_client import SpotifyClient
from auth import spotify_auth_guard

router = APIRouter()

@router.get("/artists/{artist_id}/related")
async def root(artist_id: str, sp: SpotifyClient = Depends(spotify_auth_guard)):
    return await sp.artist_related(artist=artist_id)
