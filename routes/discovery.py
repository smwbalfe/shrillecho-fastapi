from typing import List
from fastapi import APIRouter, Depends, Request, Response, FastAPI
from pydantic import BaseModel
from shrillecho.api.api_client import SpotifyClient
from shrillecho.types.artist_types import Artist
from shrillecho.types.track_types import Track
from shrillecho.discovery.artist_crawler import ArtistCrawler
from shrillecho.controllers.artist_controller import ArtistController
from shrillecho.utility.track_utils import TrackUtils

from auth import spotify_auth_guard

router = APIRouter()

# discoveryfdss
@router.get("/discovery/related/{artist_id}")
async def root(artist_id: str, sp: SpotifyClient = Depends(spotify_auth_guard)):
    crawler = ArtistCrawler(sp=sp)
    return await crawler.bfs_related(start= await sp.artists.get(artist_id=artist_id), max_depth=3)

# given n atshd fetch a load of tracks from related artists
@router.get("/discovery/related/{artist_id}/tracks")
async def func(artist_id: str, sp: SpotifyClient = Depends(spotify_auth_guard)):
    crawler = ArtistCrawler(sp=sp)

    print("[shrillecho] crawling artists")
    artists: List[Artist] = await crawler.bfs_related(start= await sp.artists.get(artist_id=artist_id), max_depth=2)

    tracks: List[Track] = []
    for a in artists:
        print(f"fetching tracks for {a.name}")
        artist_controller = ArtistController(sp=sp, artist=a)
        artist_tracks: List[Track] = await artist_controller.get_all_tracks()
        print(len(artist_tracks))
        tracks.extend(await TrackUtils.fetch_several_tracks(sp=sp, track_ids=TrackUtils.fetch_track_ids(artist_tracks)))

    print(len(tracks))
    return tracks

