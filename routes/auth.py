import datetime
import json
from core.database import r
from core.spotify_auth import sp_oauth
from fastapi import APIRouter, Request, Response
from fastapi.responses import RedirectResponse
import httpx
import spotipy
import secrets
import hashlib

from core import config

router = APIRouter()

@router.get("/spotipy-auth")
async def spotauth(request: Request):
    referer = request.headers.get("referer")
    if referer == config.next_origin:
        sp_oauth.redirect_uri = f'{config.fast_origin}redirect'
    else:
        print("invalid origin")
        exit(1)
    
    return {"url":  sp_oauth.authenticate_url()}
   

def generate_secure_session_id():
    random_number = secrets.token_bytes(32)  
    session_id = hashlib.sha256(random_number).hexdigest()
    return session_id

@router.get("/redirect")
async def sp_redirect(code: str, response: Response):
    token_info = sp_oauth.get_access_token(code=code)
    redis_key = generate_secure_session_id()
    token_info['token_expiration_time'] = (datetime.datetime.now() + datetime.timedelta(seconds=token_info['expires_in'])).isoformat()
    r.set(redis_key, json.dumps(token_info))
    response = RedirectResponse(f"{config.next_origin}/playlist")
    response.set_cookie(key="shrillecho-biscuit", value=redis_key, secure=config.secure, samesite=config.samesite, domain=config.cookie)
    return response

   