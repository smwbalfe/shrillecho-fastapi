from functools import wraps
from typing import Any, Callable, List
from fastapi import Request
import strawberry
from dependencies.spotify_client import get_spotify_client
from shrillecho.playlist.spotify_playlist import SpotifyPlaylist
from shrillecho.spotify.client import SpotifyClient
from strawberry.dataloader import DataLoader
import schemas.strawberry_schema as stype
from core.database import r

##### INPUTS #####
@strawberry.input 
class PlaylistQueryInput:
    playlist_id: str 
    get_non_liked: bool


########## QUERY FIELDS #########
@strawberry.type
class Query:
    @strawberry.field
    async def track(self, track_id: str, info: strawberry.Info) -> stype.Track:
        sp: SpotifyClient = get_spotify_client(request=info.context["request"])
        return await sp.track(track_id)

    @strawberry.field
    async def artist(self, artist_id: str, info: strawberry.Info) -> stype.Artist:
        sp: SpotifyClient = get_spotify_client(request=info.context["request"])
        return await sp.artist(artist_id)

    @strawberry.field
    async def playlist(self, track_query: PlaylistQueryInput, info: strawberry.Info) -> stype.Playlist:
        playlist_loader = info.context['playlist_loader']
        return await playlist_loader.load(track_query.playlist_id)

    @strawberry.field
    async def playlist_tracks(self, track_query: PlaylistQueryInput, info: strawberry.Info) -> List[stype.Track]:
        sp: SpotifyClient = get_spotify_client(request=info.context["request"])
        return await SpotifyPlaylist.get_playlist_tracks_filtered(sp, track_query.playlist_id, track_query.get_non_liked)

    @strawberry.field
    async def current_user_playlists(self, info: strawberry.Info) -> List[stype.SimplifiedPlaylistObject]:
        sp: SpotifyClient = get_spotify_client(request=info.context["request"])
        return await sp.current_user_saved_playlists()

    # @strawberry.field
    # async def artist_tracks(self, artist_id: str, info: strawberry.Info) -> List[stype.Track]:
    #     sp: SpotifyClient = get_spotify_client(request=info.context["request"])
    #     return await sp.artist_tracks(artist_id)

######### CONTEXT ##########
async def get_playlists(ids, request):
    sp: SpotifyClient = get_spotify_client(request=request)  
    return [await sp.playlist(playlist_id) for playlist_id in ids]


async def get_context(request: Request):

    return {"r": r, "playlist_loader": DataLoader(load_fn=lambda ids: get_playlists(ids, request)),
            "sp": "bum"}

############################

schema = strawberry.Schema(Query)