from fastapi import APIRouter, Depends, Request, Response, FastAPI
from pydantic import BaseModel
from shrillecho.api.api_client import SpotifyClient
from auth import spotify_auth_guard


router = APIRouter()

# track by id
@router.get("/track/{track_id}")
async def root(track_id: str, sp: SpotifyClient = Depends(spotify_auth_guard)):
    return await sp.tracks.one(track_id)
