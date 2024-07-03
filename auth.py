import base64
import json
import logging
import time
from typing import Any, Dict
from urllib.parse import urlencode
import httpx
import urllib3
from fastapi import APIRouter, HTTPException, Request, Response, requests
import requests as py_request
from fastapi.responses import JSONResponse, RedirectResponse
import jwt
from shrillecho.api.api_client import SpotifyClient
from secrets import token_hex
from config import REDIRECT_URI, SCOPE, SECRET_JWT_KEY, SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET, redis_client, secure, samesite, cookie

#tx
logging.basicConfig(level=logging.WARNING, filename='app.log', filemode='a', format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

router = APIRouter()

# Utility Functionss

def generate_random_string(length: int) -> str:
    return token_hex(length // 2)

async def get_access_token(code: str) -> Dict[str, Any]:
    token_url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + base64.b64encode(f"{SPOTIFY_CLIENT_ID}:{SPOTIFY_CLIENT_SECRET}".encode()).decode(),
        "Content-Type": "application/x-www-form-urlencoded",
    }

    data = {
        "code": code,
        "redirect_uri": REDIRECT_URI,
        "grant_type": "authorization_code",
    }
    
    with httpx.Client() as client:
        response = client.post(token_url, headers=headers, data=data)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Failed to get access token, status code: {response.status_code}")


def spotify_auth_url():
    state = generate_random_string(16)
    query_params = {
        'response_type': 'code',
        'client_id': SPOTIFY_CLIENT_ID,
        'scope': SCOPE,
        'redirect_uri': REDIRECT_URI,
        'state': state
    }
   
    spotify_authorize_url = 'https://accounts.spotify.com/authorize?' + urlencode(query_params)
    return JSONResponse(content={"url": spotify_authorize_url})


def jwt_encode(payload: Dict[str, Any]) -> str:
    logger.info(f"{payload}:{SECRET_JWT_KEY}")
    return jwt.encode(payload, SECRET_JWT_KEY, algorithm="HS256")

def jwt_decode(token: str) -> dict:
    try:
        decoded_token = jwt.decode(token, SECRET_JWT_KEY, algorithms="HS256")
        return decoded_token
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

def refresh_access_token(refresh_token: str):  
    logger.info(refresh_token)
    client_creds = f"{SPOTIFY_CLIENT_ID}:{SPOTIFY_CLIENT_SECRET}"
    client_creds_b64 = base64.urlsafe_b64encode(client_creds.encode()).decode()

    refresh_url = 'https://accounts.spotify.com/api/token'

    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Authorization": f"Basic {client_creds_b64}"
    }
    body = {
        "grant_type": "refresh_token",
        "refresh_token": refresh_token
    }

    with httpx.Client() as client:
        response = client.post(refresh_url, headers=headers, data=body)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(response.status_code, response.text)

def has_expired(tokens: Dict[str, Any]) -> bool:
    expiry_time = tokens.get('expires_at')
    current_time = int(time.time())
    return current_time > expiry_time

def add_expiry_time(token: Dict[str, Any]) -> Dict[str, Any]:
    current_time = int(time.time())  
    token['expires_at'] = current_time + token.get('expires_in')
    return token

async def update_tokens(tokens: Dict[str, Any], user_id: str) -> str:
    refresh_token = tokens.get('refresh_token')
    new_tokens: Dict[str,any] = refresh_access_token(refresh_token)
    add_expiry_time(new_tokens)
    new_tokens['refresh_token'] = tokens.get('refresh_token')
    redis_client.set(user_id, json.dumps(new_tokens))
    return new_tokens.get('access_token')

async def handle_spotify_auth_redirect(code: str, response: Response):
    token_info = await get_access_token(code=code)
   

    async with httpx.AsyncClient() as client:
        headers = {
            "Authorization": f"Bearer {token_info['access_token']}"
        }
        user_profile_response = await client.get('https://api.spotify.com/v1/me', headers=headers)

        if user_profile_response.status_code != 200:
            print(user_profile_response.text, user_profile_response.status_code)
            logger.error(user_profile_response.text)

        user_profile_json = user_profile_response.json()
        print(user_profile_json)

    
    user_spotify_id = user_profile_json["id"]
    logger.info(user_spotify_id)


    jwt_ = jwt_encode({"id": user_spotify_id})
    logger.info("encoded jwt")

    add_expiry_time(token_info)

    redis_client.set(user_spotify_id, json.dumps(token_info))

    response.set_cookie(key="shrillecho-biscuit", 
                        value=jwt_, 
                        secure=False,
                        samesite="lax", 
                        domain="localhost")
    
    response = RedirectResponse(url="http://localhost:3000/")
    response.set_cookie(key="shrillecho-biscuit", 
                        value=jwt_, 
                        secure=False,
                        samesite="lax", 
                        domain="localhost")
    return response


@router.get("/spotify-auth")
async def get_spotify_auth_url():
    return spotify_auth_url()
   

@router.get("/spotify-auth-redirect")
async def get_spotify_auth_url(code: str, response: Response):
    return await handle_spotify_auth_redirect(code=code, response=response)


async def spotify_auth_guard(request: Request) -> SpotifyClient:
    jwt_token = request.cookies.get("shrillecho-biscuit")

    if not jwt_token:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    payload = jwt_decode(jwt_token)

    user_id = payload.get("id")

    tokens: Dict[str, any] = redis_client.get(user_id)

    tokens = json.loads(tokens)
    logger.error(tokens)
    access_token = tokens['access_token']

    if (has_expired(tokens)):
        access_token = await update_tokens(tokens, user_id)

    if not access_token:
        raise HTTPException(status_code=401, detail="Unauthorized")
    

    return SpotifyClient(token=tokens['access_token'])

   