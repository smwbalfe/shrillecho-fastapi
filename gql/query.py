from typing import List
from fastapi import Request
import strawberry
from auth import spotify_auth_guard
from gql.handlers import get_playlists
from strawberry.dataloader import DataLoader
from gql.input_types import PlaylistTracksInput
import gql.schema as stype
from config import redis_client
from gql.handlers import get_single_artist, get_single_track, get_playlist_tracks

@strawberry.type
class Query:
    @strawberry.field
    async def track(self, track_id: str, info: strawberry.Info) -> stype.Track:
        return await get_single_track(sp=await spotify_auth_guard(request=info.context["request"]), track_id=track_id)

    @strawberry.field
    async def artist(self, artist_id: str, info: strawberry.Info) -> stype.Artist:
        return await get_single_artist(sp=await spotify_auth_guard(request=info.context["request"]), artist_id=artist_id)

    @strawberry.field
    async def playlist(self, playlist_id: str, info: strawberry.Info) -> stype.Playlist:
        playlist_loader = info.context['playlist_loader']
        return await playlist_loader.load(playlist_id)

    @strawberry.field
    async def playlist_tracks(self, playlist_tracks_input: PlaylistTracksInput, info: strawberry.Info) -> List[stype.Track]:
         return await get_playlist_tracks(sp=await spotify_auth_guard(request=info.context["request"]), playlist_tracks_input=playlist_tracks_input)

    # @strawberry.field
    # async def current_user_playlists(self, info: strawberry.Info) -> List[stype.SimplifiedPlaylistObject]:
    #     sp: SpotifyClient = get_spotify_client(request=info.context["request"])
    #     return await sp.current_user_saved_playlists()

 

async def get_context(request: Request):

    return {"r": redis_client, "playlist_loader": DataLoader(load_fn=lambda ids: get_playlists(ids, request))}

############################

schema = strawberry.Schema(Query)