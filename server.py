import logging
from aiodataloader import DataLoader
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import strawberry
from gql.mutation import Mutation
from gql.query import Query, get_context
from routes import track, playback, me, playlist, artist, discovery
import auth as auth
from strawberry.fastapi import GraphQLRouter
from config import redis_client

app = FastAPI(debug=True)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins="http://localhost:3000",
    allow_methods=["*"]
)

app.include_router(playback.router)
app.include_router(track.router)
app.include_router(me.router)
app.include_router(playlist.router)
app.include_router(artist.router)
app.include_router(discovery.router)
app.include_router(auth.router)

schema = strawberry.Schema(query=Query, mutation=Mutation)
graphql_app = GraphQLRouter(schema, context_getter=get_context)
app.include_router(graphql_app, prefix="/graphql")
                            


