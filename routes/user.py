from fastapi import APIRouter, Request, Depends
from typing import List
import spotipy
from dependencies.spotify_client import get_spotify_client, get_access_token
from pydantic import BaseModel
from shrillecho.spotify.client import SpotifyClient
from shrillecho.types.playlist_types import Playlist, PlaylistTrack

from shrillecho.types.track_types import Track
from shrillecho.utility.soundcloud_converter import SoundCloudConverter
from soundcloud import SoundCloud
import os 
from core.config import SC_CLIENT_ID

router = APIRouter()

@router.get("/me")
async def get_tracks(request: Request, sp: SpotifyClient= Depends(get_spotify_client)):
    me = await sp.me()
    print(f"[DEBUG] {me}")
    return await sp.me()

# @router.get("/liked_tracks")
# async def get_liked(request: Request, sp: spotipy.Spotify = Depends(get_spotify_client)):
#     liked_tracks: List[Track] = await fetch_liked_tracks(sp)
   ########
#     return {"len": len(liked_tracks)}
#
# class LinkModel(BaseModel):
#     uri: str

# @router.post("/playlist")
# async def get_liked(link_model: LinkModel, request: Request, sp: spotipy.Spotify = Depends(get_spotify_client)):

#     uri = link_model.uri

#     tracks: List[PlaylistTrack] =  await fetch_playlist(sp, uri)

   
#     return tracks

# class LinkModel(BaseModel):
#     link: str

# @router.post("/reccs")
# async def get_liked(link_model: LinkModel, request: Request, sp: spotipy.Spotify = Depends(get_spotify_client)):

#     l = link_model.link

#     playlist_link = radio_track(sp, l)
   
#     return {"link": playlist_link}

# @router.post("/soundcloud")
# async def get_liked(link_model: LinkModel, request: Request, sp: spotipy.Spotify = Depends(get_spotify_client), token = Depends(get_access_token)):

#     sc = SoundCloud(client_id=SC_CLIENT_ID)
#     converter = SoundCloudConverter(sc=sc, sp=sp, token=token)
#     track: Track = await converter.convert(link_model.link)

#     if track == None:
#         return {"link": "Track could not be found"}
#     else: 
#         return {"link": track.external_urls.spotify}