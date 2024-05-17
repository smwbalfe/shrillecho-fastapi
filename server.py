from core import config
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from gql.queries import *
# from gql.context import get_context
from routes import auth, playback, user, discover
import logging
import strawberry
from strawberry.fastapi import GraphQLRouter

app = FastAPI(debug=True)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=config.next_origin,
    allow_methods=["*"],
)

graphql_app = GraphQLRouter(schema, context_getter=get_context)

app.include_router(auth.router)
app.include_router(playback.router)
app.include_router(user.router)
app.include_router(graphql_app, prefix="/graphql")


                            



