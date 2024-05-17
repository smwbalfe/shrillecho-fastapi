# import graphene
# from graphene import Field

# class ExternalUrls(graphene.ObjectType):
#     spotify = graphene.String()

# class ExternalIds(graphene.ObjectType):
#     isrc = graphene.String()
#     ean = graphene.String()
#     upc = graphene.String()

# class Followers(graphene.ObjectType):
#     total = graphene.Int()
#     href = graphene.String()

# class Policies(graphene.ObjectType):
#     opt_in_trial_premium_only_market = graphene.Boolean()

# class Copyright(graphene.ObjectType):
#     text = graphene.String()
#     type = graphene.String()

# class ExplicitContent(graphene.ObjectType):
#     filter_enabled = graphene.Boolean()
#     filter_locked = graphene.Boolean()

# class Image(graphene.ObjectType):
#     url = graphene.String()
#     height = graphene.Int()
#     width = graphene.Int()

# class UserProfile(graphene.ObjectType):
#     display_name = graphene.String()
#     external_urls = graphene.Field(ExternalUrls)
#     followers = graphene.Field(Followers)
#     href = graphene.String()
#     id = graphene.String()
#     images = graphene.List(Image)
#     type = graphene.String()
#     uri = graphene.String()


# class Restrictions(graphene.ObjectType):
#     reason = graphene.String()

# class AddedBy(graphene.ObjectType):
#     external_urls = Field(ExternalUrls)
#     followers = Field(Followers)
#     href = graphene.String()
#     id = graphene.String()
#     type = graphene.String()
#     uri = graphene.String()

# class ArtistForAlbum(graphene.ObjectType):
#     external_urls = Field(ExternalUrls)
#     href = graphene.String()
#     id = graphene.String()
#     name = graphene.String()
#     type = graphene.String()
#     uri = graphene.String()

# class LinkedFrom(graphene.ObjectType):
#     external_urls = Field(ExternalUrls)
#     href = graphene.String()
#     id = graphene.String()
#     type = graphene.String()
#     uri = graphene.String()

# class Owner(graphene.ObjectType):
#     external_urls = Field(ExternalUrls)
#     followers = Field(Followers)
#     href = graphene.String()
#     id = graphene.String()
#     type = graphene.String()
#     uri = graphene.String()
#     display_name = graphene.String()

# #g
# class Artist(graphene.ObjectType):
#     external_urls = Field(ExternalUrls)
#     followers = Field(Followers)
#     genres = graphene.List(graphene.String)
#     href = graphene.String()
#     id = graphene.String()
#     images = graphene.List(Image)
#     name = graphene.String()
#     popularity = graphene.Int()
#     type = graphene.String()
#     uri = graphene.String()

# class SimplifiedTrack(graphene.ObjectType):
#     artists = graphene.List(Artist)
#     available_markets = graphene.List(graphene.String)
#     disc_number = graphene.Int()
#     duration_ms = graphene.Int()
#     explicit = graphene.Boolean()
#     external_urls = Field(ExternalUrls)
#     href = graphene.String()
#     id = graphene.String()
#     is_playable = graphene.Boolean()
#     linked_from = Field(LinkedFrom)
#     restrictions = Field(Restrictions)
#     name = graphene.String()
#     preview_url = graphene.String()
#     track_number = graphene.Int()
#     type = graphene.String()
#     uri = graphene.String()
#     is_local = graphene.Boolean()

# class SimplifiedPlaylistObject(graphene.ObjectType):
#     collaborative = graphene.Boolean()
#     description = graphene.String()
#     external_urls = Field(ExternalUrls)
#     href = graphene.String()
#     id = graphene.String()
#     images = graphene.List(Image)
#     name = graphene.String()
#     # owner = Field(UserProfile)
#     public = graphene.Boolean()
#     snapshot_id = graphene.String()
#     # tracks = Field(TrackInfo)
#     type = graphene.String()
#     uri = graphene.String()

# class AlbumTracks(graphene.ObjectType):
#     href = graphene.String()
#     limit = graphene.Int()
#     next = graphene.String()
#     offset = graphene.Int()
#     previous = graphene.String()
#     total = graphene.Int()
#     items = graphene.List(SimplifiedTrack)

# class Album(graphene.ObjectType):
#     album_type = graphene.String()
#     total_tracks = graphene.Int()
#     available_markets = graphene.List(graphene.String)
#     external_urls = Field(ExternalUrls)
#     href = graphene.String()
#     id = graphene.String()
#     images = graphene.List(Image)
#     name = graphene.String()
#     release_date = graphene.String()
#     release_date_precision = graphene.String()
#     restrictions = Field(Restrictions)
#     type = graphene.String()
#     uri = graphene.String()
#     artists = graphene.List(Artist)
#     tracks = Field(AlbumTracks)
#     copyrights = graphene.List(Copyright)
#     external_ids = Field(ExternalIds)
#     genres = graphene.List(graphene.String)
#     label = graphene.String()
#     popularity = graphene.Int()

# class SeveralAlbums(graphene.ObjectType):
#     albums = graphene.List(Album)

# class SimpleArtist(graphene.ObjectType):
#     external_urls = Field(ExternalUrls)
#     href = graphene.String()
#     id = graphene.String()
#     name = graphene.String()
#     type = graphene.String()
#     uri = graphene.String()

# # track augmente
# class Track(graphene.ObjectType):
#     album = Field(Album)
#     artists = graphene.List(Artist)
#     available_markets = graphene.List(graphene.String)
#     disc_number = graphene.Int()
#     duration_ms = graphene.Int()
#     explicit = graphene.Boolean()
#     external_urls = Field(ExternalUrls)
#     external_ids = Field(ExternalIds)
#     href = graphene.String()
#     id = graphene.String()
#     is_playable = graphene.Boolean()
#     linked_from = Field(LinkedFrom)
#     restrictions = Field(Restrictions)
#     name = graphene.String()
#     preview_url = graphene.String()
#     track_number = graphene.Int()
#     type = graphene.String()
#     uri = graphene.String()
#     is_local = graphene.Boolean()
#     liked = graphene.Boolean()

# class PlaylistTrack(graphene.ObjectType):
#     added_at = graphene.String()
#     added_by = Field(AddedBy)
#     is_local = graphene.Boolean()
#     track = Field(Track)

# class PlaylistTracks(graphene.ObjectType):
#     href = graphene.String()
#     limit = graphene.Int()
#     next = graphene.String()
#     offset = graphene.Int()
#     previous = graphene.String()
#     total = graphene.Int()
#     items = graphene.List(PlaylistTrack)

# class Playlist(graphene.ObjectType):
#     collaborative = graphene.Boolean()
#     description = graphene.String()
#     external_urls = Field(ExternalUrls)
#     followers = Field(Followers)
#     href = graphene.String()
#     id = graphene.String()
#     images = graphene.List(Image)
#     name = graphene.String()
#     owner = Field(Owner)
#     public = graphene.Boolean()
#     snapshot_id = graphene.String()
#     tracks = Field(PlaylistTracks)
#     type = graphene.String()
#     uri = graphene.String()

# class SeveralTracks(graphene.ObjectType):
#     items = graphene.List(Track)

# class SavedTrack(graphene.ObjectType):
#     added_at = graphene.String()
#     track = Field(Track)

# class CurrentUserProfile(graphene.ObjectType):
#     country = graphene.String()
#     display_name = graphene.String()
#     email = graphene.String()
#     explicit_content = Field(ExplicitContent)
#     external_urls = Field(ExternalUrls)
#     followers = Field(Followers)
#     href = graphene.String()
#     id = graphene.String()
#     images = graphene.List(Image)
#     product = graphene.String()
#     type = graphene.String()
#     uri = graphene.String()

# class UserProfile(graphene.ObjectType):
#     display_name = graphene.String()
#     external_urls = Field(ExternalUrls)
#     followers = Field(Followers)
#     href = graphene.String()
#     id = graphene.String()
#     images = graphene.List(Image)
#     type = graphene.String()
#     uri = graphene.String()

# class SavedTracks(graphene.ObjectType):
#     href = graphene.String()
#     limit = graphene.Int()
#     next = graphene.String()
#     offset = graphene.Int()
#     previous = graphene.String()
#     total = graphene.Int()
#     items = graphene.List(SavedTrack)