from typing import List
from fastapi import APIRouter, Depends, Request, Response, FastAPI
from pydantic import BaseModel
from shrillecho.api.api_client import SpotifyClient
from shrillecho.types.playlist_types import Playlist
from shrillecho.types.track_types import Track
from shrillecho.utility.track_utils import TrackUtils
from auth import spotify_auth_guard


router = APIRouter()

@router.get("/playlists/{playlist_id}/tracks")
async def playlist_tracks(playlist_id: str, filtered: str,  sp: SpotifyClient = Depends(spotify_auth_guard)):
    playlist_tracks : List[Track] = await sp.playlists.tracks_batch(playlist_id=playlist_id)
    return TrackUtils.clean_tracks(playlist_tracks)

@router.get("/playlists/{playlist_id}") 
async def playlist(playlist_id: str, sp: SpotifyClient = Depends(spotify_auth_guard)):
    return await sp.playlists.get(playlist_id=playlist_id)
