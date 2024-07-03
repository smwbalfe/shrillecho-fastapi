from typing import Optional

from pydantic import BaseModel


class CreatePlaylistModel(BaseModel):
    name: str
    copy_existing: bool 
    existing_playlist_id: str
    filter_liked: Optional[bool] = None
 