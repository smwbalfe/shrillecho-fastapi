from fastapi import APIRouter, Depends
from shrillecho.api.api_client import SpotifyClient
from shrillecho.controllers.track_controller import TracksController
from shrillecho.utility.cache import invalidate_cache
from shrillecho.types.playlist_types import Playlist
from auth import spotify_auth_guard
from routes.models.playlist_models import CreatePlaylistModel

router = APIRouter()

# Get all the current users saved playlistdd

@router.get("/me/playlists")
async def get_saved_playlists(sp: SpotifyClient = Depends(spotify_auth_guard)):
    return await sp.playlists.current_user_playlists_batch()

# Create a new playlist for the user  
@router.post("/me/playlists")
async def create_user_playlist(create_playlist: CreatePlaylistModel, sp: SpotifyClient = Depends(spotify_auth_guard)):

    tracks: TracksController = await TracksController.create_from_playlist(sp=sp, playlist=create_playlist.existing_playlist_id)
    
    await tracks.load_likes()

    liked: TracksController = await tracks.get_unliked()

    await invalidate_cache('current_user_saved_playlists')

    pl: Playlist = await liked.write_tracks(name='like_filtered', user='me')

    return pl['uri']

@router.get("/me")
async def get_tracks(sp: SpotifyClient = Depends(spotify_auth_guard)):
    return await sp.users.me()


    