from dotenv import load_dotenv
import os
from shrillecho.utility.cache import set_redis_host
import redis

load_dotenv("./.env")

SPOTIFY_CLIENT_ID = os.environ.get("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.environ.get("SPOTIFY_CLIENT_SECRET")
REDIRECT_URI = os.environ.get("REDIRECT_URI")
SCOPE = os.environ.get("SCOPE")
ENV = os.environ.get("ENVIRONMENT")
SC_CLIENT_ID = os.environ.get("SC_CLIENT_ID")
SECRET_JWT_KEY = os.environ.get("SECRET_JWT")

if ENV == "dev":
    redirect_uri = "http://localhost:8001/redirect"
    next_origin = "http://localhost:3000/"
    redis_origin = "localhost"
    fast_origin = "http://localhost:8001/"
    dorito_origin = "http://localhost:5000/"
    cookie = "localhost"
    samesite = "lax"
    secure = False
elif ENV == "prod":
    redirect_uri = "https://api.shrillecho.app/redirect"
    next_origin = "https://shrillecho.app/"
    redis_origin = "redis"
    fast_origin = "https://api.shrillecho.app/"
    dorito_origin = "https://discord.shrillecho.app/"
    cookie = "shrillecho.app"
    secure = True
    samesite = 'none'
    # fast_public_origin = "https://api.shrillecho.app"

redis_client = redis.Redis(host='192.168.0.132', port=6379, db=0, decode_responses=True)