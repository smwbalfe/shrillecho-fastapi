from typing import Any, List, Optional, Union
# from aiodataloader import DataLoader
from strawberry.dataloader import DataLoader
from fastapi import BackgroundTasks, Request, Response, WebSocket
from core.database import r
from strawberry.asgi import GraphQL

from dependencies.spotify_client import get_spotify_client
from shrillecho.spotify.client import SpotifyClient
from shrillecho.types.soundcloud_types import User



class ContextAwareDataLoader(DataLoader):
    def __init__(self, request=None):
        super().__init__()
        self.request = request

class PlaylistLoader(ContextAwareDataLoader):
    async def batch_load_fn(self, keys):
        sp: SpotifyClient = get_spotify_client(request=self.request)  
        return [await sp.playlist(playlist_id) for playlist_id in keys]

    
async def get_playlists(ids, request):
    sp: SpotifyClient = get_spotify_client(request=request)  
    return [await sp.playlist(playlist_id) for playlist_id in ids]

# class Context(object):
#     async def __call__(self, request):

#         playlist_loader = PlaylistLoader(request=request)
#         return {
#             "redis": r,
#             "request": request,
#             "background": BackgroundTasks(),
#             "playlist_loader": playlist_loader  
#         }



async def get_context(request: Request):


    return {"r": r,
            "playlist_loader": DataLoader(load_fn=lambda ids: get_playlists(ids, request))}