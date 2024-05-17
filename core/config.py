from dotenv import load_dotenv
import os
from shrillecho.utility.cache import set_redis_host

load_dotenv("./.env")

SPOTIFY_CLIENT_ID = os.environ.get("SPOTIPY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.environ.get("SPOTIPY_CLIENT_SECRET")
REDIRECT_URI = None
SCOPE = os.environ.get("SCOPE")
ENV = os.environ.get("ENVIRONMENT")
SC_CLIENT_ID = os.environ.get("SC_CLIENT_ID")

print(f'ENV: {ENV}')

if ENV == "dev":
    redirect_uri = "http://localhost:8001/redirect"
    next_origin = "http://localhost:3000/"
    redis_origin = "localhost"
    fast_origin = "http://localhost:8001/"
    dorito_origin = "http://localhost:5000/"
    cookie = "localhost"
    samesite = "lax"
    secure = False
    set_redis_host(redis_origin)
elif ENV == "prod":
    redirect_uri = "https://api.shrillecho.app/redirect"
    next_origin = "https://shrillecho.app/"
    redis_origin = "redis"
    fast_origin = "https://api.shrillecho.app/"
    dorito_origin = "https://discord.shrillecho.app/"
    cookie = "shrillecho.app"
    secure = True
    samesite = 'none'
    set_redis_host(redis_origin)
    # fast_public_origin = "https://api.shrillecho.app"
    # dorito_public_origin = "https://discord.shrillecho.app"
   