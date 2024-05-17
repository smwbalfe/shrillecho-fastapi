
from shrillecho.auth.oauth import SpotifyAuth
from .config import SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET, redirect_uri, SCOPE

# sp_oauth = SpotifyOAuth(SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, redirect_uri, scope=SCOPE, show_dialog=True)

sp_oauth = SpotifyAuth(client_id=SPOTIFY_CLIENT_ID,
                    client_secret=SPOTIFY_CLIENT_SECRET,
                    redirect_uri=redirect_uri,
                    scope=SCOPE)