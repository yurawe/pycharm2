from datetime import date

from flask_bcrypt import generate_password_hash
from marshmallow import Schema, validate, fields

class LoginSchema(Schema):
    username = fields.String()
    password = fields.String()


class UserData(Schema):
    id = fields.Integer()
    username = fields.String()
    first_name = fields.String()
    last_name = fields.String()
    email = fields.String(validate=validate.Email())
    phone = fields.String()


class UserSchema(Schema):
    username = fields.String()
    first_name = fields.String()
    last_name = fields.String()
    email = fields.String(validate=validate.Email())
    phone = fields.String()
    password = fields.String()
    # password = fields.Function(
    #     deserialize=lambda obj: generate_password_hash(obj), load_only=True
    # )

class GenreData(Schema):
    id = fields.Integer()
    name = fields.String()
class GenreSchema(Schema):
    name = fields.String()

class ArtistData(Schema):
    id = fields.Integer()
    name = fields.String()
    date_of_birth = fields.Date(validate=lambda x: x <= date.today())
    country = fields.String()
class ArtistSchema(Schema):
    name = fields.String()
    date_of_birth = fields.Date(validate=lambda x: x <= date.today())
    country = fields.String()
class AlbumData(Schema):
    id = fields.Integer()
    name = fields.String()
class AlbumSchema(Schema):
    name = fields.String()

class SongData(Schema):
    id = fields.Integer()
    name = fields.String()
    length = fields.Int()
    language = fields.String()
    release_date = fields.Date()
    genre_id = fields.Integer()
    album_id = fields.Integer()
class SongSchema(Schema):
    name = fields.String()
    length = fields.Int()
    language = fields.String()
    release_date = fields.Date()
    genre_id = fields.Integer()
    album_id = fields.Integer()
class SongAllData(Schema):
    id = fields.Integer()
    name = fields.String()
    length = fields.Int()
    language = fields.String()
    release_date = fields.Date()
    genre = fields.Nested(lambda: GenreData())
    album = fields.Nested(lambda: AlbumData())




class PlaylistData(Schema):
    id = fields.Integer()
    name = fields.String()
    is_private = fields.Boolean()
    created_at = fields.Date()
    updated_at = fields.Date()
class PlaylistSchema(Schema):
    name = fields.String()
    is_private = fields.Boolean()
    created_at = fields.Date()
    updated_at = fields.Date()

class PlaylistDataToUpdate(Schema):
    name = fields.String()
    is_private = fields.Boolean()

class Artist_songData(Schema):
    artist_id = fields.Integer()
    song_id = fields.Integer()
class Artist_songAllData(Schema):
    artist = fields.Nested(lambda: ArtistData())
    song = fields.Nested(lambda: SongAllData())
class Playlist_songData(Schema):
    playlist_id = fields.Integer()
    song_id = fields.Integer()
class Playlist_songAllData(Schema):
    playlist = fields.Nested(lambda: PlaylistData())
    song = fields.Nested(lambda: SongAllData())

class User_playlistData(Schema):
    playlist_id = fields.Integer()
    user_id = fields.Integer()

class User_playlistAllData(Schema):
    playlist = fields.Nested(lambda: PlaylistData())
    user = fields.Nested(lambda: UserData())

class User_playlistWithSongsAllData(Schema):
    username = fields.String()
    playlist = fields.Nested(lambda: PlaylistData())
    songs = fields.Nested(lambda: SongAllData(), many=True)

class User_playlistUserNameData(Schema):
    owner = fields.String()
    playlist = fields.Nested(lambda: PlaylistData())