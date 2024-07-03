from strawberry.field_extensions import InputMutationExtension
import strawberry

from auth import spotify_auth_guard
from gql.handlers import create_spotify_playlist
from gql.input_types import PlaylistTracksInput


@strawberry.type
class Mutation:
   @strawberry.mutation()
   async def create_playlist(self, playlist_create_input: PlaylistTracksInput, info: strawberry.Info) -> str:
      await create_spotify_playlist(await spotify_auth_guard(request=info.context["request"]), name="test", playlist_tracks_input=playlist_create_input)
      return "1"