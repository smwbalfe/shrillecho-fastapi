import strawberry

@strawberry.input 
class PlaylistTracksInput:
    playlist_id: str 
    remove_liked: bool
    min_obscurity_value: int
    max_obscurity_value: int
    min_followers: int 
    max_followers: int