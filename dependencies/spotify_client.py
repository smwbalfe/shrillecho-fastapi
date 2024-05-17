import datetime
from fastapi import HTTPException, Request
import spotipy
import json
from shrillecho.spotify.client import SpotifyClient
from core.spotify_auth import sp_oauth

# internal modules
from core.database import r


def get_spotify_client(request: Request) -> SpotifyClient:

    session_id = request.cookies.get("shrillecho-biscuit")

    if not session_id:
        raise HTTPException(status_code=401, detail="Not authenticated")

    stored_tokens = r.get(session_id)

    token_json = None
    if stored_tokens:
        token_json = json.loads(stored_tokens)
    else:
        raise HTTPException(status_code=401, detail="Authentication Error, Invalid or Stale Biscuit")

    expiration_time = datetime.datetime.fromisoformat(token_json['token_expiration_time'])

    if datetime.datetime.now() >= expiration_time:
    
        new_tokens = sp_oauth.refresh_access_token(token_json['refresh_token'])

        new_tokens['token_expiration_time'] = (datetime.datetime.now() + datetime.timedelta(seconds=new_tokens['expires_in'])).isoformat()

        # If we have not been given a refresh token, we can use the old one again
        if 'refresh_token' not in new_tokens:
            new_tokens['refresh_token'] = token_json['refresh_token']

        r.set(session_id, json.dumps(new_tokens))
        return SpotifyClient(auth=new_tokens['access_token'])

    print(token_json['access_token'])
    return SpotifyClient(auth=token_json['access_token'])


# deprecated
def get_access_token(request: Request) -> spotipy.Spotify:
    session_id = request.cookies.get("shrillecho-biscuit")
    if not session_id:
        raise HTTPException(status_code=401, detail="Not authenticated")
    stored_tokens = r.get(session_id)
    token_json = None
    if stored_tokens:
        token_json = json.loads(stored_tokens)
    else:
        raise HTTPException(status_code=401, detail="Authentication Error, Invalid or Stale Biscuit")
    expiration_time = datetime.datetime.fromisoformat(token_json['token_expiration_time'])
    if datetime.datetime.now() >= expiration_time:
        new_tokens = sp_oauth.refresh_access_token(token_json['refresh_token'])
        new_tokens['token_expiration_time'] = (datetime.datetime.now() + datetime.timedelta(seconds=new_tokens['expires_in'])).isoformat()
        if 'refresh_token' not in new_tokens:
            new_tokens['refresh_token'] = token_json['refresh_token']
        r.set(session_id, json.dumps(new_tokens))
        return SpotifyClient(auth=new_tokens['access_token'])

    return token_json['access_token']