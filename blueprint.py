from flask import Blueprint, request, jsonify
from marshmallow import ValidationError
from db_utils import create_entry, update_entry
from models.album import Album
from models.artist import Artist
from models.artist_song import artist_song
from models.genre import Genre
from models.playlist import Playlist
from models.playlist_song import playlist_song
from models.song import Song
from models.user import User
from models.user_playlist import user_playlist
from resp_error import errors
from models.model import Session
from schemes import UserSchema, UserData, GenreSchema, GenreData, ArtistSchema, ArtistData, PlaylistSchema, \
    PlaylistData, PlaylistDataToUpdate, SongSchema, SongData, AlbumSchema, AlbumData, SongAllData, User_playlistData, \
    Artist_songData, Artist_songAllData, Playlist_songData, Playlist_songAllData, \
    User_playlistAllData, User_playlistWithSongsAllData
from datetime import date
session = Session()

api_blueprint = Blueprint('api',__name__)

# STUDENT_ID=3
# @api_blueprint.route("/hello-world")
# def hello_world_def():
#     return f"Hello world!!!"
# @api_blueprint.route(f"/hello-world-9")
# def hello_world():
#     return f"Hello, World 9"


# USER
@api_blueprint.route("/user", methods=["POST"])
def create_user():
    json_data = request.json
    if not json_data:
        return errors.bad_request
    try:
        user_data = UserSchema().load(json_data)
    except ValidationError as err:
        return err.messages, 422
    user = session.query(User).filter_by(username=user_data["username"]).first()
    user2 = session.query(User).filter_by(email=user_data["email"]).first()
    if user:
        return errors.exists
    if user2:
        return {'error': {'code': 403, 'message': "User with this email already exists"}}, 403
    user = create_entry(User, **user_data)
    return jsonify(UserData().dump(user)), 200


@api_blueprint.route('/user/login', methods=['GET'])
def login():
    json_data = request.json
    if not json_data:
        return errors.bad_request
    try:
        data = UserSchema().load(json_data, partial=True)
    except ValidationError as err:
        return err.messages, 422
    user = session.query(User).filter_by(username=data["username"]).first()
    if not user:
        return errors.not_found
    if data['password'] == user.password:
        return {"message": "Successfully logged in"}, 200
    else:
        return {'error': {'code': 400, 'message': 'Incorrect password'}}, 400


@api_blueprint.route("/users", methods=["GET"])
def get_users():
    users_list = session.query(User).all()
    return UserData().dump(users_list, many=True), 200


@api_blueprint.route('/user/<string:username>', methods=['GET', 'PUT', 'DELETE'])
def user_username_api(username):
    user = session.query(User).filter_by(username=username).first()
    if not user:
        return errors.not_found
    if request.method == 'GET':
        return UserData().dump(user), 200
    if request.method == 'PUT':
        json_data = request.json
        if not json_data:
            return errors.bad_request
        try:
            data = UserSchema().load(json_data, partial=True)
        except ValidationError as err:
            return err.messages, 422
        for key, value in data.items():
            if key == "username":
                us = session.query(User).filter_by(username=data["username"]).first()
                if us:
                    return errors.exists
            if key == "email":
                us = session.query(User).filter_by(email=data["email"]).first()
                if us:
                    return errors.exists
        updated_user = update_entry(user, **data)
        for key, value in data.items():
            if key == "password" and len(data) == 1:
                return {"message": "Password changed successfully"}, 200
        return UserData().dump(updated_user), 200
    if request.method == 'DELETE':
        session.delete(user)
        session.commit()
        return {"message": "Deleted successfully"}, 200




@api_blueprint.route("/genre", methods=["POST", "GET"])
def genre_api():
    if request.method == 'POST':
        json_data = request.json
        if not json_data:
            return errors.bad_request
        try:
            genre_data = GenreSchema().load(json_data)
        except ValidationError as err:
            return err.messages, 422
        genre = session.query(Genre).filter_by(name=genre_data["name"]).first()
        if genre:
            return errors.exists
        new_genre = create_entry(Genre, **genre_data)
        return jsonify(GenreData().dump(new_genre))
    if request.method == 'GET':
        genre_list = session.query(Genre).all()
        return jsonify(GenreData().dump(genre_list, many=True)), 200


@api_blueprint.route('/genre/<int:genreId>', methods=['GET', 'PUT', 'DELETE'])
def group_id_api(genreId):
    gen = session.query(Genre).filter_by(id=genreId).first()
    if not gen:
        return errors.not_found
    if request.method == 'GET':
        return GenreData().dump(gen)
    if request.method == 'PUT':
        json_data = request.json
        if not json_data:
            return errors.bad_request
        try:
            data = GenreSchema().load(json_data, partial=True)
        except ValidationError as err:
            return err.messages, 422
        updated_genre = update_entry(gen, **data)
        return GenreData().dump(updated_genre)
    if request.method == 'DELETE':
        session.delete(gen)
        session.commit()
        return {"message": "Deleted successfully"}, 200


@api_blueprint.route("/album", methods=["POST", "GET"])
def album_api():
    if request.method == 'POST':
        json_data = request.json
        if not json_data:
            return errors.bad_request
        try:
            album_data = AlbumSchema().load(json_data)
        except ValidationError as err:
            return err.messages, 422
        new_album = create_entry(Album, **album_data)
        return jsonify(AlbumData().dump(new_album))
    if request.method == 'GET':
        album_list = session.query(Album).all()
        return jsonify(AlbumData().dump(album_list, many=True)), 200


@api_blueprint.route('/album/<int:albumId>', methods=['GET', 'PUT', 'DELETE'])
def album_id_api(albumId):
    alb = session.query(Album).filter_by(id=albumId).first()
    if not alb:
        return errors.not_found
    if request.method == 'GET':
        return AlbumData().dump(alb)
    if request.method == 'PUT':
        json_data = request.json
        if not json_data:
            return errors.bad_request
        try:
            data = AlbumSchema().load(json_data, partial=True)
        except ValidationError as err:
            return err.messages, 422
        for key, value in data.items():
            if key == "name":
                g = session.query(Genre).filter_by(name=data["name"]).first()
                if g:
                    return errors.exists
        updated_album = update_entry(alb, **data)
        return AlbumData().dump(updated_album)
    if request.method == 'DELETE':
        session.delete(alb)
        session.commit()
        return {"message": "Deleted successfully"}, 200
@api_blueprint.route("/artist", methods=["POST", "GET"])
def artist_api():
    if request.method == 'POST':
        json_data = request.json
        if not json_data:
            return errors.bad_request
        try:
            artist_data = ArtistSchema().load(json_data)
        except ValidationError as err:
            return err.messages, 422
        new_artist = create_entry(Artist, **artist_data)
        return jsonify(ArtistData().dump(new_artist))
    if request.method == 'GET':
        artist_list = session.query(Artist).all()
        return jsonify(ArtistData().dump(artist_list, many=True)), 200


@api_blueprint.route('/artist/<int:artistId>', methods=['GET', 'PUT', 'DELETE'])
def artist_id_api(artistId):
    art = session.query(Artist).filter_by(id=artistId).first()
    if not art:
        return errors.not_found
    if request.method == 'GET':
        return ArtistData().dump(art)
    if request.method == 'PUT':
        json_data = request.json
        if not json_data:
            return errors.bad_request
        try:
            data = ArtistSchema().load(json_data, partial=True)
        except ValidationError as err:
            return err.messages, 422
        updated_artist = update_entry(art, **data)
        return ArtistData().dump(updated_artist)
    if request.method == 'DELETE':
        session.delete(art)
        session.commit()
        return {"message": "Deleted successfully"}, 200


@api_blueprint.route("/playlist", methods=["POST", "GET"])
def playlist_api():
    if request.method == 'POST':
        json_data = request.json
        if not json_data:
            return errors.bad_request
        try:
            playlist_data = PlaylistDataToUpdate().load(json_data)
        except ValidationError as err:
            return err.messages, 422
        playlist_data.update({"updated_at": date.today()})
        playlist_data.update({"created_at": date.today()})
        new_playlist = create_entry(Playlist, **playlist_data)
        return jsonify(PlaylistData().dump(new_playlist))
    if request.method == 'GET':
        playlist_list = session.query(Playlist).all()
        for x in playlist_list:
            if x.is_private==1:
                playlist_list.remove(x)
        return jsonify(PlaylistData().dump(playlist_list, many=True)), 200


@api_blueprint.route('/playlist/<int:playlistId>', methods=['GET', 'PUT', 'DELETE'])
def playlistid_api(playlistId):
    pla = session.query(Playlist).filter_by(id=playlistId).first()
    if not pla:
        return errors.not_found
    if request.method == 'GET':
        if pla.is_private == 1:
            return {'error': {'code': 405, 'message': 'This playlist is private'}}, 405
        return PlaylistData().dump(pla)
    if request.method == 'PUT':
        json_data = request.json
        if not json_data:
            return errors.bad_request
        try:
            data = PlaylistData().load(json_data, partial=True)
        except ValidationError as err:
            return err.messages, 422
        data.update({"updated_at": date.today()})
        updated_playlist = update_entry(pla, **data)
        return PlaylistData().dump(updated_playlist)
    if request.method == 'DELETE':
        session.delete(pla)
        session.commit()
        return {"message": "Deleted successfully"}, 200



@api_blueprint.route("/songs", methods=["POST", "GET"])
def songs_api():
    if request.method == 'POST':
        json_data = request.json
        if not json_data:
            return errors.bad_request
        try:
            song_data = SongSchema().load(json_data)
        except ValidationError as err:
            return err.messages, 422
        for key, value in song_data.items():
            if key == "genre_id":
                new_gr_song = session.query(Genre).filter_by(id=song_data["genre_id"]).first()
                if not new_gr_song:
                    return {'error': {'code': 404, 'message': 'Not found genre with this id'}}, 404
            if key == "album_id":
                new_al_song = session.query(Album).filter_by(id=song_data["album_id"]).first()
                if not new_al_song:
                    return {'error': {'code': 404, 'message': 'Not found album with this id'}}, 404

        new_song = create_entry(Song, **song_data)
        return jsonify(SongAllData().dump(new_song))

    if request.method == 'GET':
        song_list = session.query(Song).all()
        return jsonify(SongData().dump(song_list, many=True)), 200


@api_blueprint.route('/songs/<int:songId>', methods=['GET', 'PUT', 'DELETE'])
def song_id_api(songId):
    son = session.query(Song).filter_by(id=songId).first()
    if not son:
        return errors.not_found
    if request.method == 'GET':
        return SongAllData().dump(son)
    if request.method == 'PUT':
        json_data = request.json
        if not json_data:
            return errors.bad_request
        try:
            data = SongSchema().load(json_data, partial=True)
        except ValidationError as err:
            return err.messages,
        for key, value in data.items():
            if key == "genre_id":
                new_gr_song = session.query(Genre).filter_by(id=data["genre_id"]).first()
                if not new_gr_song:
                    return {'error': {'code': 404, 'message': 'Not found genre with this id'}}, 404
            if key == "album_id":
                new_al_song = session.query(Album).filter_by(id=data["album_id"]).first()
                if not new_al_song:
                    return {'error': {'code': 404, 'message': 'Not found album with this id'}}, 404
        updated_song = update_entry(son, **data)
        return SongAllData().dump(updated_song)
    if request.method == 'DELETE':
        session.delete(son)
        session.commit()
        return {"message": "Deleted successfully"}, 200

@api_blueprint.route('/songs/genre/<string:genre>', methods=['GET'])
def songs_genre_api(genre):
    gn = session.query(Genre).filter_by(name=genre).first()
    if not gn:
        return errors.not_found
    song_list = session.query(Song).filter_by(genre_id=gn.id).all()
    return jsonify(SongData().dump(song_list, many=True)), 200

@api_blueprint.route('/songs/languages/<string:language>', methods=['GET'])
def songs_language_api(language):
    song_list = session.query(Song).filter_by(language=language).all()
    return jsonify(SongData().dump(song_list, many=True)), 200

@api_blueprint.route('/songs/album/<int:albumId>', methods=['GET'])
def songAlbum_id_api(albumId):
    al = session.query(Album).filter_by(id=albumId).first()
    if not al:
        return errors.not_found
    song_list = session.query(Song).filter_by(album_id=albumId).all()
    return jsonify(SongData().dump(song_list, many=True)), 200

@api_blueprint.route("/artist_song", methods=["POST", "GET"])
def artist_song_api():
    if request.method == 'POST':
        json_data = request.json
        if not json_data:
            return errors.bad_request
        try:
            artist_song_data = Artist_songData().load(json_data)
        except ValidationError as err:
            return err.messages, 422
        new_a = session.query(Artist).filter_by(id=artist_song_data["artist_id"]).first()
        if not new_a:
            return {'error': {'code': 404, 'message': 'Not found artist with this id'}}, 404
        new_s = session.query(Song).filter_by(id=artist_song_data["song_id"]).first()
        if not new_s:
            return {'error': {'code': 404, 'message': 'Not found song with this id'}}, 404
        new_a.songs.append(new_s)
        session.commit()
        artist_song_data.update({"artist": new_a})
        artist_song_data.update({"song": new_s})
        return jsonify(Artist_songAllData().dump(artist_song_data)), 200
    if request.method == 'GET':
        artist_song_list = session.query(artist_song).all()
        artist_song_data = {}
        artist_song_list_data = []
        for x in artist_song_list:
            art = session.query(Artist).filter_by(id=x.artist_id).first()
            son = session.query(Song).filter_by(id=x.song_id).first()
            artist_song_data.update({"artist": art})
            artist_song_data.update({"song": son})
            artist_song_list_data.append(artist_song_data)
        return jsonify(Artist_songAllData().dump(artist_song_list_data, many=True)), 200


@api_blueprint.route("/artist_song/artist/<int:artistId>", methods=["GET"])
def artist_songs_artist_api(artistId):
    art = session.query(Artist).filter_by(id=artistId).first()
    if not art:
        return errors.not_found
    artist_song_list = session.query(artist_song).filter_by(artist_id=artistId).all()
    artist_song_list_data_s = []
    for x in artist_song_list:
        son = session.query(Song).filter_by(id=x.song_id).first()
        artist_song_list_data_s.append(son)
    return jsonify(SongData().dump(artist_song_list_data_s, many=True)), 200


@api_blueprint.route('/artist_song/artist/<int:artistId>/song/<int:songId>', methods=['GET', 'PUT', 'DELETE'])
def artist_song_a_s_id_api(artistId, songId):
    art_song = session.query(artist_song).filter_by(artist_id=artistId, song_id=songId).first()
    if not art_song:
        return errors.not_found
    if request.method == 'GET':
        artist_song_data = {}
        art = session.query(Artist).filter_by(id=art_song.artist_id).first()
        son = session.query(Song).filter_by(id=art_song.song_id).first()
        artist_song_data.update({"artist": art})
        artist_song_data.update({"song": son})
        return jsonify(Artist_songAllData().dump(artist_song_data)), 200
    if request.method == 'PUT':
        json_data = request.json
        if not json_data:
            return errors.bad_request
        try:
            data = Artist_songData().load(json_data, partial=True)
        except ValidationError as err:
            return err.messages, 422
        for key, value in data.items():
            if key == "artist_id":
                new_a = session.query(Artist).filter_by(id=data["artist_id"]).first()
                if not new_a:
                    return {'error': {'code': 404, 'message': 'Not found artist with this id'}}, 404
            if key == "song_id":
                new_s = session.query(Song).filter_by(id=data["song_id"]).first()
                if not new_s:
                    return {'error': {'code': 404, 'message': 'Not found song with this id'}}, 404
        old_a = session.query(Artist).filter_by(id=artistId).first()
        old_s = session.query(Song).filter_by(id=songId).first()
        old_a.songs.remove(old_s)
        session.commit()
        updated_song_data = {}
        if len(data) == 2:
            new_a.songs.append(new_s)
            session.commit()
            updated_song_data.update({"artist": new_a})
            updated_song_data.update({"song": new_s})
        else:
            for key, value in data.items():
                if key == "artist_id":
                    new_a.songs.append(old_s)
                    session.commit()
                    updated_song_data.update({"artist": new_a})
                    updated_song_data.update({"song": old_s})
                if key == "song_id":
                    old_a.songs.append(new_s)
                    session.commit()
                    updated_song_data.update({"artist": old_a})
                    updated_song_data.update({"song": new_s})
        return jsonify(Artist_songAllData().dump(updated_song_data)), 200
    if request.method == 'DELETE':
        old_a = session.query(Artist).filter_by(id=artistId).first()
        old_s = session.query(Song).filter_by(id=songId).first()
        old_a.songs.remove(old_s)
        session.commit()
        return {"message": "Deleted successfully"}, 200
@api_blueprint.route("/playlist_song", methods=["POST", "GET"])
def playlist_song_api():
    if request.method == 'POST':
        json_data = request.json
        if not json_data:
            return errors.bad_request
        try:
            playlist_song_data = Playlist_songData().load(json_data)
        except ValidationError as err:
            return err.messages, 422
        new_a = session.query(Playlist).filter_by(id=playlist_song_data["playlist_id"]).first()
        if not new_a:
            return {'error': {'code': 404, 'message': 'Not found playlist with this id'}}, 404
        new_s = session.query(Song).filter_by(id=playlist_song_data["song_id"]).first()
        if not new_s:
            return {'error': {'code': 404, 'message': 'Not found song with this id'}}, 404
        new_a.songs.append(new_s)
        session.commit()
        playlist_song_data.update({"playlist": new_a})
        playlist_song_data.update({"song": new_s})
        return jsonify(Playlist_songAllData().dump(playlist_song_data)), 200
    if request.method == 'GET':
        playlist_song_list = session.query(playlist_song).all()
        playlist_song_data = {}
        playlist_song_list_data = []
        for x in playlist_song_list:
            pl = session.query(Playlist).filter_by(id=x.playlist_id).first()
            son = session.query(Song).filter_by(id=x.song_id).first()
            playlist_song_data.update({"playlist": pl})
            playlist_song_data.update({"song": son})
            if pl.is_private == 0:
                playlist_song_list_data.append(playlist_song_data)
        return jsonify(Playlist_songAllData().dump(playlist_song_list_data, many=True)), 200


@api_blueprint.route('/playlist_song/playlist/<int:playlistId>/song/<int:songId>', methods=['GET', 'PUT', 'DELETE'])
def playlist_song_a_s_id_api(playlistId, songId):
    pl_song = session.query(playlist_song).filter_by(playlist_id=playlistId, song_id=songId).first()
    if not pl_song:
        return errors.not_found
    if request.method == 'GET':
        playlist_song_data = {}
        pl = session.query(Playlist).filter_by(id=pl_song.playlist_id).first()
        if pl.is_private == 1:
            return {'error': {'code': 405, 'message': 'This playlist is private'}}, 405
        son = session.query(Song).filter_by(id=pl_song.song_id).first()
        playlist_song_data.update({"playlist": pl})
        playlist_song_data.update({"song": son})
        return jsonify(Playlist_songAllData().dump(playlist_song_data)), 200
    if request.method == 'PUT':
        json_data = request.json
        if not json_data:
            return errors.bad_request
        try:
            data = Playlist_songData().load(json_data, partial=True)
        except ValidationError as err:
            return err.messages, 422
        pl = session.query(Playlist).filter_by(id=pl_song.playlist_id).first()
        if pl.is_private == 1:
            return {'error': {'code': 405, 'message': 'This playlist is private'}}, 405
        for key, value in data.items():
            if key == "playlist_id":
                new_p = session.query(Playlist).filter_by(id=data["playlist_id"]).first()
                if not new_p:
                    return {'error': {'code': 404, 'message': 'Not found playlist with this id'}}, 404
                if new_p.is_private == 1:
                    return {'error': {'code': 405, 'message': 'New playlist is private'}}, 405
            if key == "song_id":
                new_s = session.query(Song).filter_by(id=data["song_id"]).first()
                if not new_s:
                    return {'error': {'code': 404, 'message': 'Not found song with this id'}}, 404
        old_p = session.query(Playlist).filter_by(id=playlistId).first()
        old_s = session.query(Song).filter_by(id=songId).first()
        old_p.songs.remove(old_s)
        session.commit()
        updated_song_data = {}
        if len(data) == 2:
            new_p.songs.append(new_s)
            session.commit()
            updated_song_data.update({"playlist": new_p})
            updated_song_data.update({"song": new_s})
        else:
            for key, value in data.items():
                if key == "playlist_id":
                    new_p.songs.append(old_s)
                    session.commit()
                    updated_song_data.update({"playlist": new_p})
                    updated_song_data.update({"song": old_s})
                if key == "song_id":
                    old_p.songs.append(new_s)
                    session.commit()
                    updated_song_data.update({"playlist": old_p})
                    updated_song_data.update({"song": new_s})
        return jsonify(Playlist_songAllData().dump(updated_song_data)), 200
    if request.method == 'DELETE':
        pl = session.query(Playlist).filter_by(id=pl_song.playlist_id).first()
        if pl.is_private == 1:
            return {'error': {'code': 405, 'message': 'This playlist is private'}}, 405
        old_p = session.query(Playlist).filter_by(id=playlistId).first()
        old_s = session.query(Song).filter_by(id=songId).first()
        old_p.songs.remove(old_s)
        session.commit()
        return {"message": "Deleted successfully"}, 200

@api_blueprint.route("/playlist_song/playlist/<int:playlistId>", methods=["GET"])
def playlist_songs_playlist_api(playlistId):
    pl = session.query(Playlist).filter_by(id=playlistId).first()
    if not pl:
        return errors.not_found
    if pl.is_private == 1:
        return {'error': {'code': 405, 'message': 'This playlist is private'}}, 405
    playlist_song_list = session.query(playlist_song).filter_by(playlist_id=playlistId).all()
    playlist_song_list_data_s = []
    for x in playlist_song_list:
        son = session.query(Song).filter_by(id=x.song_id).first()
        playlist_song_list_data_s.append(son)
    return jsonify(SongData().dump(playlist_song_list_data_s, many=True)), 200

@api_blueprint.route("/playlist_song/song/<int:songId>", methods=["GET"])
def playlist_songs_song_api(songId):
    son = session.query(Song).filter_by(id=songId).first()
    if not son:
        return errors.not_found
    playlist_song_list = session.query(playlist_song).filter_by(song_id=songId).all()
    playlist_song_list_data_s = []
    for x in playlist_song_list:
        pl = session.query(Playlist).filter_by(id=x.playlist_id).first()
        if pl.is_private == 0:
            playlist_song_list_data_s.append(pl)
    return jsonify(PlaylistData().dump(playlist_song_list_data_s, many=True)), 200
@api_blueprint.route("/user_playlist", methods=["POST", "GET"])
def user_playlist_api():
    if request.method == 'POST':
        json_data = request.json
        if not json_data:
            return errors.bad_request
        try:
            user_playlist_data = User_playlistData().load(json_data)
        except ValidationError as err:
            return err.messages, 422
        new_u = session.query(User).filter_by(id=user_playlist_data["user_id"]).first()
        if not new_u:
            return {'error': {'code': 404, 'message': 'Not found user with this id'}}, 404
        new_p = session.query(Playlist).filter_by(id=user_playlist_data["playlist_id"]).first()
        if not new_p:
            return {'error': {'code': 404, 'message': 'Not found playlist with this id'}}, 404
        new_u.playlists.append(new_p)
        session.commit()
        user_playlist_data.update({"user": new_u})
        user_playlist_data.update({"playlist": new_p})
        return jsonify(User_playlistAllData().dump(user_playlist_data)), 200
    if request.method == 'GET':
        user_playlist_list = session.query(user_playlist).all()
        user_playlist_data = {}
        user_playlist_list_data = []
        for x in user_playlist_list:
            us = session.query(User).filter_by(id=x.user_id).first()
            pl = session.query(Playlist).filter_by(id=x.playlist_id).first()
            user_playlist_data.update({"user": us})
            user_playlist_data.update({"playlist": pl})
            if pl.is_private == 0:
                user_playlist_list_data.append(user_playlist_data)
        return jsonify(User_playlistAllData().dump(user_playlist_list_data, many=True)), 200

@api_blueprint.route('/user_playlist/user/<int:userId>/playlist/<int:playlistId>', methods=[ 'PUT', 'DELETE'])
def user_playlist_a_s_id_api(userId, playlistId):
    us_playlist = session.query(user_playlist).filter_by(user_id=userId, playlist_id=playlistId).first()
    if not us_playlist:
        return errors.not_found
    if request.method == 'PUT':
        json_data = request.json
        if not json_data:
            return errors.bad_request
        try:
            data = User_playlistData().load(json_data, partial=True)
        except ValidationError as err:
            return err.messages, 422
        pl = session.query(Playlist).filter_by(id=us_playlist.playlist_id).first()
        if pl.is_private == 1:
            return {'error': {'code': 405, 'message': 'This playlist is private'}}, 405
        for key, value in data.items():
            if key == "user_id":
                new_u = session.query(User).filter_by(id=data["user_id"]).first()
                if not new_u:
                    return {'error': {'code': 404, 'message': 'Not found user with this id'}}, 404
            if key == "playlist_id":
                new_p = session.query(Playlist).filter_by(id=data["playlist_id"]).first()
                if not new_p:
                    return {'error': {'code': 404, 'message': 'Not found playlist with this id'}}, 404
                if new_p.is_private == 1:
                    return {'error': {'code': 405, 'message': 'New playlist is private'}}, 405
        old_u = session.query(User).filter_by(id=userId).first()
        old_p = session.query(Playlist).filter_by(id=playlistId).first()
        old_u.playlists.remove(old_p)
        session.commit()
        updated_playlist_data = {}
        if len(data) == 2:
            new_u.playlists.append(new_p)
            session.commit()
            updated_playlist_data.update({"user": new_u})
            updated_playlist_data.update({"playlist": new_p})
        else:
            for key, value in data.items():
                if key == "playlist_id":
                    old_u.playlists.append(new_p)
                    session.commit()
                    updated_playlist_data.update({"user": old_u})
                    updated_playlist_data.update({"user": new_p})
                if key == "user_id":
                    new_u.playlists.append(old_p)
                    session.commit()
                    updated_playlist_data.update({"user": new_u})
                    updated_playlist_data.update({"playlist": old_p})
        return jsonify(User_playlistAllData().dump(updated_playlist_data)), 200
    if request.method == 'DELETE':
        pl = session.query(Playlist).filter_by(id=us_playlist.playlist_id).first()
        if pl.is_private == 1:
            return {'error': {'code': 405, 'message': 'This playlist is private'}}, 405
        old_u = session.query(User).filter_by(id=userId).first()
        old_p = session.query(Playlist).filter_by(id=playlistId).first()
        old_u.playlists.remove(old_p)
        session.commit()
        return {"message": "Deleted successfully"}, 200

@api_blueprint.route("/user_playlist/<string:username>", methods=["GET"])
def playlist_songs_username_api(username):
    us = session.query(User).filter_by(username=username).first()
    if not us:
        return errors.not_found
    user_playlist_list = session.query(user_playlist).filter_by(user_id=us.id).all()
    user_playlist_list_data_s = []
    for x in user_playlist_list:
        pl = session.query(Playlist).filter_by(id=x.playlist_id).first()
        user_playlist_list_data_s.append(pl)
    return jsonify(PlaylistData().dump(user_playlist_list_data_s, many=True)), 200


@api_blueprint.route("/user_playlist/<string:username>/public", methods=["GET"])
def playlist_songs_username_public_api(username):
    us = session.query(User).filter_by(username=username).first()
    if not us:
        return errors.not_found
    user_playlist_list = session.query(user_playlist).filter_by(user_id=us.id).all()
    user_playlist_list_data_s = []
    for x in user_playlist_list:
        pl = session.query(Playlist).filter_by(id=x.playlist_id).first()
        if pl.is_private == 0:
            user_playlist_list_data_s.append(pl)
    return jsonify(PlaylistData().dump(user_playlist_list_data_s, many=True)), 200

@api_blueprint.route("/user_playlist/<string:username>/private", methods=["GET"])
def playlist_songs_username_private_api(username):
    us = session.query(User).filter_by(username=username).first()
    if not us:
        return errors.not_found
    user_playlist_list = session.query(user_playlist).filter_by(user_id=us.id).all()
    user_playlist_list_data_s = []
    for x in user_playlist_list:
        pl = session.query(Playlist).filter_by(id=x.playlist_id).first()
        if pl.is_private == 1:
            user_playlist_list_data_s.append(pl)
    return jsonify(PlaylistData().dump(user_playlist_list_data_s, many=True)), 200

# ####################test
@api_blueprint.route('/user_playlist/<string:username>/playlist/<int:playlistId>', methods=[ 'GET'])
def user_playlist_username_playlist_id_api(username, playlistId):
    us = session.query(User).filter_by(username=username).first()
    if not us:
        return errors.not_found
    us_playlist = session.query(user_playlist).filter_by(user_id=us.id, playlist_id=playlistId).first()
    if not us_playlist:
        return errors.not_found
    if request.method == 'GET':
        user_playlist_data = {}
        pl = session.query(Playlist).filter_by(id=us_playlist.playlist_id).first()
        playlist_song_list = session.query(playlist_song).filter_by(playlist_id=playlistId).all()
        playlist_song_list_data_s = []
        for x in playlist_song_list:
            son = session.query(Song).filter_by(id=x.song_id).first()
            playlist_song_list_data_s.append(son)
        user_playlist_data.update({"username": username})
        user_playlist_data.update({"playlist": pl})
        user_playlist_data.update({"songs": playlist_song_list_data_s})
        return jsonify(User_playlistWithSongsAllData().dump(user_playlist_data)), 200

@api_blueprint.route('/user_playlist/<string:username>/playlist/<int:playlistId>/song/<int:songId>', methods=['POST', 'GET', 'DELETE'])
def playlist_song_user_pl_song_id_api(username, playlistId, songId):
    us = session.query(User).filter_by(username=username).first()
    if not us:
        return errors.not_found
    us_playlist = session.query(user_playlist).filter_by(user_id=us.id, playlist_id=playlistId).first()
    if not us_playlist:
        return errors.not_found
    if request.method == 'POST':
        pl = session.query(Playlist).filter_by(id=playlistId).first()
        if not pl:
            return {'error': {'code': 404, 'message': 'Not found playlist with this id'}}, 404
        new_s = session.query(Song).filter_by(id=songId).first()
        if not new_s:
            return {'error': {'code': 404, 'message': 'Not found song with this id'}}, 404
        pl.songs.append(new_s)
        session.commit()
        playlist_song_data = {}
        playlist_song_data.update({"playlist": pl})
        playlist_song_data.update({"song": new_s})
        return jsonify(Playlist_songAllData().dump(playlist_song_data)), 200
    if request.method == 'GET':
        pl_song = session.query(playlist_song).filter_by(playlist_id=playlistId, song_id=songId).first()
        if not pl_song:
            return errors.not_found
        son = session.query(Song).filter_by(id=pl_song.song_id).first()
        return jsonify(SongAllData().dump(son)), 200
    if request.method == 'DELETE':
        old_p = session.query(Playlist).filter_by(id=playlistId).first()
        old_s = session.query(Song).filter_by(id=songId).first()
        old_p.songs.remove(old_s)
        session.commit()
        return {"message": "Deleted successfully"}, 200
