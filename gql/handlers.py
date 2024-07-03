from typing import List
from shrillecho.api.api_client import SpotifyClient
from auth import spotify_auth_guard
from gql.input_types import PlaylistTracksInput
import gql.schema as stype
from shrillecho.types.track_types import Track
from shrillecho.controllers.tracks_controller import TracksController
from shrillecho.types.artist_types import Artist
from shrillecho.utility.artist_utils import ArtistUtils

############## Tracks ##############

async def get_single_track(sp: SpotifyClient, track_id: str) -> stype.Track:
    return await sp.tracks.one(track_id=track_id)

############## Artists ##############

async def get_single_artist(sp: SpotifyClient, artist_id: str) -> stype.Artist:
    return await sp.artists.get(artist_id=artist_id)


############# Playlist ##############
 
# Dataloader for spotify playlistss
async def get_playlists(ids, request):
    sp: SpotifyClient = await spotify_auth_guard(request=request)  
    return [await get_playlist(sp, playlist_id) for playlist_id in ids]

async def get_playlist(sp: SpotifyClient, playlist_id: str) -> stype.Playlist:
    return await sp.playlists.get(playlist_id=playlist_id)

async def get_playlist_tracks(sp: SpotifyClient, playlist_tracks_input: PlaylistTracksInput) -> List[stype.Track]:
  

    tracks_controller: TracksController = await TracksController.create_from_playlist(sp=sp,playlist=playlist_tracks_input.playlist_id)
    await tracks_controller.clean_tracks()
    # await tracks_controller.load_likes()
#dd
    if playlist_tracks_input.remove_liked:
        return tracks_controller.unliked_tracks
    
    tracks_controller.tracks = await ArtistUtils.expand_tracks_list_with_artists(sp=sp,tracks=tracks_controller.tracks)

    followers_tracks: List[Track] = []
    for track in tracks_controller.tracks:
        followers = track.artists[0].followers.total
        if followers < playlist_tracks_input.max_followers and followers> playlist_tracks_input.min_followers:
            followers_tracks.append(track)
        #dd
    obscure_tracks = []
    for track in followers_tracks:
        if track.popularity < playlist_tracks_input.max_obscurity_value and track.popularity > playlist_tracks_input.min_obscurity_value:
            obscure_tracks.append(track)

    return obscure_tracks

async def create_spotify_playlist(sp: SpotifyClient, playlist_tracks_input: PlaylistTracksInput, name: str):
    print("writing playlist tracks")
    my_profile = await sp.users.me()
   

    tracks_controller: TracksController = await TracksController.create_from_playlist(sp=sp,playlist=playlist_tracks_input.playlist_id)
    await tracks_controller.clean_tracks()
    # await tracks_controller.load_likes()s

    if playlist_tracks_input.remove_liked:
        return tracks_controller.unliked_tracks
    
    tracks_controller.tracks = await ArtistUtils.expand_tracks_list_with_artists(sp=sp,tracks=tracks_controller.tracks)

    # d
    followers_tracks: List[Track] = []
    for track in tracks_controller.tracks:
        followers = track.artists[0].followers.total
        if followers < playlist_tracks_input.max_followers and followers> playlist_tracks_input.min_followers:
            followers_tracks.append(track)
    #sjdss
    obscure_tracks = []
    for track in followers_tracks:
        if track.popularity < playlist_tracks_input.max_obscurity_value and track.popularity > playlist_tracks_input.min_obscurity_value:
            obscure_tracks.append(track)

    track_controller = TracksController(sp=sp, tracks=obscure_tracks)
    print(track_controller.tracks[0].name)
    for track in track_controller.tracks:
        print(track.name)
    await track_controller.write_tracks(name='test', user='me')