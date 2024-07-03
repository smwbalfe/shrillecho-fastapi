from fastapi import APIRouter, Depends
import spotipy
from auth import spotify_auth_guard
from shrillecho.api.api_client import SpotifyClient

#fd

router = APIRouter()

@router.get("/currently-playing")
async def pause(sp = Depends(spotify_auth_guard)):
    try:
        current_track = sp.current_playback()

        if not current_track:
            return {"message": "No track is currently playing."}

        track_name = current_track['item']['name']
        artist_name = ', '.join([artist['name'] for artist in current_track['item']['artists']])
        cover_art_url = current_track['item']['album']['images'][1]['url']

        return {
            "track_name": track_name,
            "artist_name": artist_name,
            "cover_art_url": cover_art_url,
            "progress": current_track['progress_ms']
        }

    except spotipy.exceptions.SpotifyException as e:
        return {"error": str(e)}


@router.get("/toggle-playback")
async def play(sp: SpotifyClient = Depends(spotify_auth_guard)):
    devices = sp.devices()['devices']
    id = ''
    for d in devices:
        if d['name'] == 'shrillecho-app':
            id = d['id']
    playback_state = sp.current_playback()

    if playback_state:
        if playback_state['is_playing']:
            sp.pause_playback()
        else:
            sp.start_playback()
    else:
        print("no playback state")
        sp.start_playback(device_id=id, uris=['spotify:track:6Xe6LY9gii4gyEsCx4J6vd'])

@router.get("/next")
async def skip(sp: SpotifyClient = Depends(spotify_auth_guard)):
    sp.next_track()
