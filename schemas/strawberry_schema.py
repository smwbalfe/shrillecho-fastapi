from typing import List, Optional
import strawberry

@strawberry.type
class ExternalUrls:
    spotify: str

@strawberry.type
class ExternalIds:
    isrc: str
    ean: str
    upc: str

@strawberry.type
class Followers:
    total: int
    href: str

@strawberry.type
class Policies:
    opt_in_trial_premium_only_market: bool

@strawberry.type
class Copyright:
    text: str
    type: str

@strawberry.type
class ExplicitContent:
    filter_enabled: bool
    filter_locked: bool

@strawberry.type
class Image:
    url: str
    height: int
    width: int

@strawberry.type
class UserProfile:
    display_name: str
    external_urls: ExternalUrls
    followers: Followers
    href: str
    id: str
    images: List[Image]
    type: str
    uri: str

@strawberry.type
class Restrictions:
    reason: str

@strawberry.type
class AddedBy:
    external_urls: ExternalUrls
    followers: Followers
    href: str
    id: str
    type: str
    uri: str

@strawberry.type
class ArtistForAlbum:
    external_urls: ExternalUrls
    href: str
    id: str
    name: str
    type: str
    uri: str

@strawberry.type
class LinkedFrom:
    external_urls: ExternalUrls
    href: str
    id: str
    type: str
    uri: str

@strawberry.type
class Owner:
    external_urls: ExternalUrls
    followers: Followers
    href: str
    id: str
    type: str
    uri: str
    display_name: str

@strawberry.type
class Artist:
    external_urls: ExternalUrls
    followers: Followers
    genres: List[str]
    href: str
    id: str
    images: List[Image]
    name: str
    popularity: int
    type: str
    uri: str

@strawberry.type
class SimplifiedTrack:
    artists: List[Artist]
    available_markets: List[str]
    disc_number: int
    duration_ms: int
    explicit: bool
    external_urls: ExternalUrls
    href: str
    id: str
    is_playable: bool
    linked_from: LinkedFrom
    restrictions: Restrictions
    name: str
    preview_url: str
    track_number: int
    type: str
    uri: str
    is_local: bool

@strawberry.type
class SimplifiedPlaylistObject:
    collaborative: bool
    description: str
    external_urls: ExternalUrls
    href: str
    id: str
    images: Optional[List[Image]]
    name: str
    public: bool
    snapshot_id: str
    type: str
    uri: str

@strawberry.type
class AlbumTracks:
    href: str
    limit: int
    next: str
    offset: int
    previous: str
    total: int
    items: List[SimplifiedTrack]

@strawberry.type
class Album:
    album_type: str
    total_tracks: int
    available_markets: List[str]
    external_urls: ExternalUrls
    href: str
    id: str
    images: List[Image]
    name: str
    release_date: str
    release_date_precision: str
    restrictions: Restrictions
    type: str
    uri: str
    artists: List[Artist]
    tracks: AlbumTracks
    copyrights: List[Copyright]
    external_ids: ExternalIds
    genres: List[str]
    label: str
    popularity: int

@strawberry.type
class SeveralAlbums:
    albums: List[Album]

@strawberry.type
class SimpleArtist:
    external_urls: ExternalUrls
    href: str
    id: str
    name: str
    type: str
    uri: str

@strawberry.type
class Track:
    album: Album
    artists: List[Artist]
    available_markets: List[str]
    disc_number: int
    duration_ms: int
    explicit: bool
    external_urls: ExternalUrls
    external_ids: ExternalIds
    href: str
    id: str
    is_playable: bool
    linked_from: LinkedFrom
    restrictions: Restrictions
    name: str
    preview_url: Optional[str]
    track_number: int
    type: str
    uri: str
    is_local: bool
    liked: bool

@strawberry.type
class PlaylistTrack:
    added_at: str
    added_by: AddedBy
    is_local: bool
    track: Track

@strawberry.type
class PlaylistTracks:
    href: str
    limit: int
    next: str
    offset: int
    previous: str
    total: int
    items: List[PlaylistTrack]

@strawberry.type
class Playlist:
    collaborative: bool
    description: str
    external_urls: ExternalUrls
    followers: Followers
    href: str
    id: str
    images: List[Image]
    name: str
    owner: Owner
    public: bool
    snapshot_id: str
    tracks: PlaylistTracks
    type: str
    uri: str

@strawberry.type
class SeveralTracks:
    items: List[Track]

@strawberry.type
class SavedTrack:
    added_at: str
    track: Track

@strawberry.type
class CurrentUserProfile:
    country: str
    display_name: str
    email: str
    explicit_content: ExplicitContent
    external_urls: ExternalUrls
    followers: Followers
    href: str
    id: str
    images: List[Image]
    product: str
    type: str
    uri: str

@strawberry.type
class UserProfile:
    display_name: str
    external_urls: ExternalUrls
    followers: Followers
    href: str
    id: str
    images: List[Image]
    type: str
    uri: str

@strawberry.type
class SavedTracks:
    href: str
    limit: int
    next: str
    offset: int
    previous: str
    total: int
    items: List[SavedTrack]
