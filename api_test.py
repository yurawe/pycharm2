import unittest
from base64 import b64encode

from bcrypt import hashpw, gensalt
from flask import Flask
from blueprint import api_blueprint
from models import User, Genre, Album, Artist, Playlist, Song
from models.model import Session

session = Session()


class Test(unittest.TestCase):
    API_URL = "http://127.0.0.1:5000/api/music_service"
    USER_URL = "{}/user".format(API_URL)
    GENRE_URL = "{}/genre".format(API_URL)
    ALBUM_URL = "{}/album".format(API_URL)
    ARTIST_URL = "{}/artist".format(API_URL)
    PLAYLIST_URL = "{}/playlist".format(API_URL)
    SONG_URL = "{}/songs".format(API_URL)
    ARTIST_SONG_URL = "{}/artist_song".format(API_URL)
    PLAYLIST_SONG_URL = "{}/playlist_song".format(API_URL)
    USER_PLAYLIST_URL = "{}/user_playlist".format(API_URL)

    def setUp(self) -> None:
        app = Flask(__name__)
        self.app_context = app.app_context()
        self.app_context.push()
        self.client = app.test_client()
        app.register_blueprint(api_blueprint, url_prefix='/api/music_service')
        session.begin()

    def tearDown(self) -> None:
        session.close()
        self.app_context.pop()

    def request_headers_user(self):
        """Returns API request headers."""
        auth = '{0}:{1}'.format('nedstark', 'alive')
        return {
            'Accept': 'application/json',
            'Authorization': 'Basic {encoded_login}'.format(
                encoded_login=b64encode(auth.encode('utf-8')).decode('utf-8')
            )
        }

    def request_headers_user_new(self):
        """Returns API request headers."""
        auth = '{0}:{1}'.format('userforpl', '111')
        return {
            'Accept': 'application/json',
            'Authorization': 'Basic {encoded_login}'.format(
                encoded_login=b64encode(auth.encode('utf-8')).decode('utf-8')
            )
        }

    def request_headers_user_starkned67(self):
        """Returns API request headers."""
        auth = '{0}:{1}'.format('starkned6767', 'iamdead')
        return {
            'Accept': 'application/json',
            'Authorization': 'Basic {encoded_login}'.format(
                encoded_login=b64encode(auth.encode('utf-8')).decode('utf-8')
            )
        }

    def request_headers_admin(self):
        """Returns API request headers."""
        auth = '{0}:{1}'.format('admin', 'secret')
        return {
            'Accept': 'application/json',
            'Authorization': 'Basic {encoded_login}'.format(
                encoded_login=b64encode(auth.encode('utf-8')).decode('utf-8')
            )
        }

    def test_create_user(self):
        payload = {"username": "starkned6767",
                   "first_name": "Ned",
                   "last_name": "Stark",
                   "email": "stark676@gmail.com",
                   "phone": "+380464636377",
                   "password": "iamdead"
                   }

        responce = self.client.post(self.USER_URL, json=payload)
        self.assertEqual(responce.status_code, 200)

    def test2_create_user(self):  # empty json
        payload = {}
        responce = self.client.post(self.USER_URL, json=payload)
        self.assertEqual(responce.status_code, 400)

    def test3_create_user(self):  # bad email
        payload = {
            "username": "cool2username",
            "first_name": "Ned",
            "last_name": "Stark",
            "email": "stark1gmalcom",
            "phone": "+380464636377",
            "password": "24242"
        }
        responce = self.client.post(self.USER_URL, json=payload)
        self.assertEqual(responce.status_code, 422)

    def test4_create_user(self):  # existing email
        payload = {
            "username": "coolusername",
            "first_name": "Ned",
            "last_name": "Stark",
            "email": "admin@gmail.com",
            "phone": "+380464636377",
            "password": "ned123456"
        }
        responce = self.client.post(self.USER_URL, json=payload)
        self.assertEqual(responce.status_code, 403)

    def test5_create_user(self):  # existing username
        payload = {
            "username": "admin",
            "first_name": "Ned",
            "last_name": "Stark",
            "email": "stark1@gmail.com",
            "phone": "+380464636377",
            "password": "ned123456"
        }
        responce = self.client.post(self.USER_URL, json=payload)
        self.assertEqual(responce.status_code, 403)

    #
    def test1_login(self):
        payload = {
            "username": "nedstark",
            "password": "alive"
        }
        responce = self.client.get(self.USER_URL + '/login', json=payload)
        self.assertEqual(responce.status_code, 200)

    def test2_login(self):
        payload = {
            "username": "nonexisting",
            "password": "ned123456"
        }
        responce = self.client.get(self.USER_URL + '/login', json=payload)
        self.assertEqual(responce.status_code, 404)

    def test3_login(self):  # incorrect pass
        payload = {
            "username": "nedstark",
            "password": "ned1234567"
        }
        responce = self.client.get(self.USER_URL + '/login', json=payload)
        self.assertEqual(responce.status_code, 401)

    def test4_login(self):  # incorrect pass
        payload = {}
        responce = self.client.get(self.USER_URL + '/login', json=payload)
        self.assertEqual(responce.status_code, 400)

    def test_get_users(self):
        responce = self.client.get(self.USER_URL + 's', headers=self.request_headers_user())
        self.assertEqual(responce.status_code, 403)

    def test_get_users_admin(self):
        responce = self.client.get(self.USER_URL + 's', headers=self.request_headers_admin())
        self.assertEqual(responce.status_code, 200)

    def test_user_username(self):
        responce = self.client.get(self.USER_URL + '/nedstark', headers=self.request_headers_user())
        self.assertEqual(responce.status_code, 200)

    def test_put_user_success(self):
        payload = {
            "first_name": "Eddard"
        }
        response = self.client.put(self.USER_URL + '/nedstark', headers=self.request_headers_user(), json=payload)
        self.assertEqual(response.status_code, 200)

    def test_put_user_no_acc(self):
        payload = {
            "first_name": "Eddard"
        }
        response = self.client.put(self.USER_URL + '/admin', headers=self.request_headers_user(), json=payload)
        self.assertEqual(response.status_code, 403)

    def test_put_user_no_data(self):
        payload = {}
        response = self.client.put(self.USER_URL + '/nedstark', headers=self.request_headers_user(), json=payload)
        self.assertEqual(response.status_code, 400)

    def test_put_username_exists(self):
        payload = {
            "username": "admin"
        }
        response = self.client.put(self.USER_URL + '/nedstark', headers=self.request_headers_user(), json=payload)
        self.assertEqual(response.status_code, 403)

    def test_put_email_exists(self):
        payload = {
            "email": "admin@gmail.com"
        }
        response = self.client.put(self.USER_URL + '/nedstark', headers=self.request_headers_user(), json=payload)
        self.assertEqual(response.status_code, 403)

    def test_delete_user_succ(self):
        response = self.client.delete(self.USER_URL + '/starkned6767', headers=self.request_headers_user_starkned67())
        self.assertEqual(response.status_code, 200)

    def test_delete_no_acc(self):
        response = self.client.delete(self.USER_URL + '/admin', headers=self.request_headers_user())
        self.assertEqual(response.status_code, 403)

    def test_delete_not_found(self):
        response = self.client.delete(self.USER_URL + '/nonex', headers=self.request_headers_user())
        self.assertEqual(response.status_code, 404)

    def test_create_genre(self):
        payload = {"name": "kpop"}
        responce = self.client.post(self.GENRE_URL, json=payload, headers=self.request_headers_admin())
        self.assertEqual(responce.status_code, 200)

    def test_create_genre_empty(self):  # empty json
        payload = {}
        responce = self.client.post(self.GENRE_URL, json=payload, headers=self.request_headers_admin())
        self.assertEqual(responce.status_code, 400)

    def test_create_genre_no_acc(self):
        payload = {"name": "kpop"}
        responce = self.client.post(self.GENRE_URL, json=payload, headers=self.request_headers_user())
        self.assertEqual(responce.status_code, 403)

    def test_create_genre_exists(self):
        payload = {"name": "rock"}
        responce = self.client.post(self.GENRE_URL, json=payload, headers=self.request_headers_admin())
        self.assertEqual(responce.status_code, 403)

    def test_get_genre(self):
        response = self.client.get(self.GENRE_URL, headers=self.request_headers_admin())
        self.assertEqual(response.status_code, 200)

    def test_get_genre_no_auth(self):
        response = self.client.get(self.GENRE_URL)
        self.assertEqual(response.status_code, 401)

    def test_get_genre_by_id(self):
        id = '4'
        response = self.client.get(self.GENRE_URL + '/' + id, headers=self.request_headers_admin())
        self.assertEqual(response.status_code, 200)

    def test_get_genre_by_id_no_auth(self):
        id = '4'
        response = self.client.get(self.GENRE_URL + '/' + id)
        self.assertEqual(response.status_code, 401)

    def test_get_genre_by_id_notfound(self):
        response = self.client.get(self.GENRE_URL + '/6778', headers=self.request_headers_admin())
        self.assertEqual(response.status_code, 404)

    def test_put_genre(self):
        payload = {"name": "jazz"}
        response = self.client.put(self.GENRE_URL + '/pop', headers=self.request_headers_admin(), json=payload)
        self.assertEqual(response.status_code, 200)
        payload = {"name": "pop"}
        response = self.client.put(self.GENRE_URL + '/jazz', headers=self.request_headers_admin(), json=payload)

    def test_put_genre_notfound(self):
        payload = {"name": "kpop"}
        response = self.client.put(self.GENRE_URL + '/nonex', headers=self.request_headers_admin(), json=payload)
        self.assertEqual(response.status_code, 404)

    def test_put_genre_no_acc(self):
        payload = {"name": "kpop"}
        response = self.client.put(self.GENRE_URL + '/rock', headers=self.request_headers_user(), json=payload)
        self.assertEqual(response.status_code, 403)

    def test_put_genre_empty(self):
        payload = {}
        response = self.client.put(self.GENRE_URL + '/rock', headers=self.request_headers_admin(), json=payload)
        self.assertEqual(response.status_code, 400)

    def test_delete_genre(self):
        response = self.client.delete(self.GENRE_URL + '/kpop', headers=self.request_headers_admin())
        self.assertEqual(response.status_code, 200)

    def test_delete_genre_notfound(self):
        response = self.client.delete(self.GENRE_URL + '/nonex', headers=self.request_headers_admin())
        self.assertEqual(response.status_code, 404)

    def test_delete_genre_no_acc(self):
        response = self.client.delete(self.GENRE_URL + '/rock', headers=self.request_headers_user())
        self.assertEqual(response.status_code, 403)

    def test_create_album(self):
        payload = {"name": "deftones album"}
        responce = self.client.post(self.ALBUM_URL, json=payload, headers=self.request_headers_admin())
        self.assertEqual(responce.status_code, 200)

    def test_create_album_empty(self):  # empty json
        payload = {}
        responce = self.client.post(self.ALBUM_URL, json=payload, headers=self.request_headers_admin())
        self.assertEqual(responce.status_code, 400)

    def test_create_album_no_acc(self):
        payload = {"name": "deftones album"}
        responce = self.client.post(self.ALBUM_URL, json=payload, headers=self.request_headers_user())
        self.assertEqual(responce.status_code, 403)

    # def test_create_album_exists(self):
    #     payload = {"name": "x-one"}
    #     responce = self.client.post(self.ALBUM_URL, json=payload, headers=self.request_headers_admin())
    #     self.assertEqual(responce.status_code, 403)

    def test_get_album(self):
        response = self.client.get(self.ALBUM_URL, headers=self.request_headers_admin())
        self.assertEqual(response.status_code, 200)

    def test_get_album_no_auth(self):
        response = self.client.get(self.ALBUM_URL)
        self.assertEqual(response.status_code, 401)

    def test_get_album_by_id(self):
        id = '1'
        response = self.client.get(self.ALBUM_URL + '/' + id, headers=self.request_headers_admin())
        self.assertEqual(response.status_code, 200)

    def test_get_album_by_id_no_auth(self):
        id = '1'
        response = self.client.get(self.ALBUM_URL + '/' + id)
        self.assertEqual(response.status_code, 401)

    def test_get_album_by_id_notfound(self):
        response = self.client.get(self.ALBUM_URL + '/6778', headers=self.request_headers_admin())
        self.assertEqual(response.status_code, 404)

    def test_put_album(self):
        payload = {"name": "jazz"}
        response = self.client.put(self.ALBUM_URL + '/2', headers=self.request_headers_admin(), json=payload)
        self.assertEqual(response.status_code, 200)
        payload = {"name": "pop"}
        response = self.client.put(self.ALBUM_URL + '/2', headers=self.request_headers_admin(), json=payload)

    def test_put_album_notfound(self):
        payload = {"name": "kpop"}
        response = self.client.put(self.ALBUM_URL + '/5666', headers=self.request_headers_admin(), json=payload)
        self.assertEqual(response.status_code, 404)

    def test_put_album_no_acc(self):
        payload = {"name": "kpop"}
        response = self.client.put(self.ALBUM_URL + '/1', headers=self.request_headers_user(), json=payload)
        self.assertEqual(response.status_code, 403)

    def test_put_album_empty(self):
        payload = {}
        response = self.client.put(self.ALBUM_URL + '/1', headers=self.request_headers_admin(), json=payload)
        self.assertEqual(response.status_code, 400)

    def test_delete_album(self):
        alb = session.query(Album).filter_by(name='deftones album').first()
        id = str(alb.id)
        response = self.client.delete(self.ALBUM_URL + '/' + id, headers=self.request_headers_admin())
        self.assertEqual(response.status_code, 200)

    def test_delete_album_notfound(self):
        response = self.client.delete(self.ALBUM_URL + '/535355', headers=self.request_headers_admin())
        self.assertEqual(response.status_code, 404)

    def test_delete_album_no_acc(self):
        response = self.client.delete(self.ALBUM_URL + '/1', headers=self.request_headers_user())
        self.assertEqual(response.status_code, 403)

    def test_create_artist(self):
        payload = {"name": "txt", "date_of_birth": "2020-10-10", "country": "Korea"}
        responce = self.client.post(self.ARTIST_URL, json=payload, headers=self.request_headers_admin())
        self.assertEqual(responce.status_code, 200)

    def test_create_artist_empty(self):  # empty json
        payload = {}
        responce = self.client.post(self.ARTIST_URL, json=payload, headers=self.request_headers_admin())
        self.assertEqual(responce.status_code, 400)

    def test_create_artist_no_acc(self):
        payload = {"name": "txt", "date_of_birth": "2020-10-10", "country": "Korea"}
        responce = self.client.post(self.ARTIST_URL, json=payload, headers=self.request_headers_user())
        self.assertEqual(responce.status_code, 403)

    # def test_create_album_exists(self):
    #     payload = {"name": "x-one"}
    #     responce = self.client.post(self.ALBUM_URL, json=payload, headers=self.request_headers_admin())
    #     self.assertEqual(responce.status_code, 403)

    def test_get_artist(self):
        response = self.client.get(self.ARTIST_URL, headers=self.request_headers_admin())
        self.assertEqual(response.status_code, 200)

    def test_get_artist_no_auth(self):
        response = self.client.get(self.ARTIST_URL)
        self.assertEqual(response.status_code, 401)

    def test_get_artist_by_id(self):
        id = '1'
        response = self.client.get(self.ARTIST_URL + '/' + id, headers=self.request_headers_admin())
        self.assertEqual(response.status_code, 200)

    def test_get_artist_by_id_no_auth(self):
        id = '1'
        response = self.client.get(self.ARTIST_URL + '/' + id)
        self.assertEqual(response.status_code, 401)

    def test_get_artist_by_id_notfound(self):
        response = self.client.get(self.ARTIST_URL + '/6778', headers=self.request_headers_admin())
        self.assertEqual(response.status_code, 404)

    def test_put_artist(self):
        payload = {"name": "jazz"}
        response = self.client.put(self.ARTIST_URL + '/2', headers=self.request_headers_admin(), json=payload)
        self.assertEqual(response.status_code, 200)
        payload = {"name": "oneus"}
        response = self.client.put(self.ARTIST_URL + '/2', headers=self.request_headers_admin(), json=payload)

    def test_put_artist_notfound(self):
        payload = {"name": "jazz"}
        response = self.client.put(self.ARTIST_URL + '/5666', headers=self.request_headers_admin(), json=payload)
        self.assertEqual(response.status_code, 404)

    def test_put_artist_no_acc(self):
        payload = {"name": "jazz"}
        response = self.client.put(self.ARTIST_URL + '/1', headers=self.request_headers_user(), json=payload)
        self.assertEqual(response.status_code, 403)

    def test_put_artist_empty(self):
        payload = {}
        response = self.client.put(self.ARTIST_URL + '/1', headers=self.request_headers_admin(), json=payload)
        self.assertEqual(response.status_code, 400)

    def test_delete_artist(self):
        ar = session.query(Artist).filter_by(name='txt').first()
        id = str(ar.id)
        response = self.client.delete(self.ARTIST_URL + '/' + id, headers=self.request_headers_admin())
        self.assertEqual(response.status_code, 200)

    def test_delete_artist_notfound(self):
        response = self.client.delete(self.ARTIST_URL + '/535355', headers=self.request_headers_admin())
        self.assertEqual(response.status_code, 404)

    def test_delete_artist_no_acc(self):
        response = self.client.delete(self.ARTIST_URL + '/1', headers=self.request_headers_user())
        self.assertEqual(response.status_code, 403)

    def test_create_playlist(self):
        payload = {"name": "my_playlist", "is_private": False}
        responce = self.client.post(self.PLAYLIST_URL, json=payload, headers=self.request_headers_user())
        self.assertEqual(responce.status_code, 200)

    def test_create_playlist_empty(self):  # empty json
        payload = {}
        responce = self.client.post(self.PLAYLIST_URL, json=payload, headers=self.request_headers_user())
        self.assertEqual(responce.status_code, 400)

    def test_get_playlists(self):
        responce = self.client.get(self.PLAYLIST_URL, headers=self.request_headers_user())
        self.assertEqual(responce.status_code, 200)

    def test_get_playlist_by_id(self):
        response = self.client.get(self.PLAYLIST_URL + '/1', headers=self.request_headers_user_new())
        self.assertEqual(response.status_code, 200)

    def test_get_playlist_by_id_no_acc(self):
        response = self.client.get(self.PLAYLIST_URL + '/1', headers=self.request_headers_user())
        self.assertEqual(response.status_code, 403)

    def test_get_playlist_by_id_notfound(self):
        response = self.client.get(self.PLAYLIST_URL + '/10000', headers=self.request_headers_user_new())
        self.assertEqual(response.status_code, 404)

    def test_put_playlist_by_id(self):
        payload = {"name": "mychanged"}
        response = self.client.put(self.PLAYLIST_URL + '/1', headers=self.request_headers_user_new(), json=payload)
        self.assertEqual(response.status_code, 200)

    def test_put_playlist_by_id_empty(self):
        payload = {}
        response = self.client.put(self.PLAYLIST_URL + '/1', headers=self.request_headers_user_new(), json=payload)
        self.assertEqual(response.status_code, 400)

    def test_put_playlist_by_id_no_acc(self):
        payload = {"name": "mychanged"}
        response = self.client.put(self.PLAYLIST_URL + '/1', headers=self.request_headers_user(), json=payload)
        self.assertEqual(response.status_code, 403)

    def test_put_playlist_by_id_no_auth(self):
        payload = {"name": "mychanged"}
        response = self.client.put(self.PLAYLIST_URL + '/1', json=payload)
        self.assertEqual(response.status_code, 401)

    def test_delete_playlist_by_id(self):
        pl = session.query(Playlist).filter_by(name="my_playlist").first()
        id = str(pl.id)
        response = self.client.delete(self.PLAYLIST_URL + '/' + id, headers=self.request_headers_user())
        self.assertEqual(response.status_code, 200)

    def test_delete_playlist_by_id_no_acc(self):
        response = self.client.delete(self.PLAYLIST_URL + '/1', headers=self.request_headers_user())
        self.assertEqual(response.status_code, 403)

    def test_create_song(self):
        payload = {
            "name": "puma",
            "length": 3.28,
            "language": "Korean",
            "release_date": "2020-01-01",
            "genre_id": 4,
            "album_id": 1
        }
        response = self.client.post(self.SONG_URL, headers=self.request_headers_admin(), json=payload)
        self.assertEqual(response.status_code, 200)

    def test_create_song_empty(self):
        payload = {}
        response = self.client.post(self.SONG_URL, headers=self.request_headers_admin(), json=payload)
        self.assertEqual(response.status_code, 400)

    def test_create_song_no_auth(self):
        payload = {
            "name": "puma",
            "length": 3.28,
            "language": "Korean",
            "release_date": "2020-01-01",
            "genre_id": 4,
            "album_id": 1
        }
        response = self.client.post(self.SONG_URL, json=payload)
        self.assertEqual(response.status_code, 401)

    def test_create_song_no_acc(self):
        payload = {
            "name": "puma",
            "length": 3.28,
            "language": "Korean",
            "release_date": "2020-01-01",
            "genre_id": 4,
            "album_id": 1
        }
        response = self.client.post(self.SONG_URL, headers=self.request_headers_user(), json=payload)
        self.assertEqual(response.status_code, 403)

    def test_create_song_bad_album(self):
        payload = {
            "name": "puma",
            "length": 3.28,
            "language": "Korean",
            "release_date": "2020-01-01",
            "genre_id": 4,
            "album_id": 1000
        }
        response = self.client.post(self.SONG_URL, headers=self.request_headers_admin(), json=payload)
        self.assertEqual(response.status_code, 404)

    def test_create_song_bad_genre(self):
        payload = {
            "name": "puma",
            "length": 3.28,
            "language": "Korean",
            "release_date": "2020-01-01",
            "genre_id": 4000,
            "album_id": 1
        }
        response = self.client.post(self.SONG_URL, headers=self.request_headers_admin(), json=payload)
        self.assertEqual(response.status_code, 404)

    def test_get_song(self):
        response = self.client.get(self.SONG_URL, headers=self.request_headers_admin())
        self.assertEqual(response.status_code, 200)

    def test_get_song_no_auth(self):
        response = self.client.get(self.SONG_URL)
        self.assertEqual(response.status_code, 401)

    def test_get_song_by_id(self):
        response = self.client.get(self.SONG_URL + '/1', headers=self.request_headers_admin())
        self.assertEqual(response.status_code, 200)

    def test_get_song_by_id_no_auth(self):
        response = self.client.get(self.SONG_URL + '/1')
        self.assertEqual(response.status_code, 401)

    def test_get_song_by_id_notfound(self):
        response = self.client.get(self.SONG_URL + '/10000', headers=self.request_headers_admin())
        self.assertEqual(response.status_code, 404)

    def test_put_song_by_id(self):
        payload = {"name": "loser"}
        response = self.client.put(self.SONG_URL + '/1', headers=self.request_headers_admin(), json=payload)
        self.assertEqual(response.status_code, 200)

    def test_put_song_by_id_no_auth(self):
        payload = {"name": "loser"}
        response = self.client.put(self.SONG_URL + '/1', json=payload)
        self.assertEqual(response.status_code, 401)

    def test_put_song_by_id_notfound(self):
        payload = {"name": "loser"}
        response = self.client.put(self.SONG_URL + '/10000', headers=self.request_headers_admin(), json=payload)
        self.assertEqual(response.status_code, 404)

    def test_put_song_by_id_no_acc(self):
        payload = {"name": "loser"}
        response = self.client.put(self.SONG_URL + '/1', headers=self.request_headers_user(), json=payload)
        self.assertEqual(response.status_code, 403)

    def test_put_song_by_id_empty(self):
        payload = {}
        response = self.client.put(self.SONG_URL + '/1', headers=self.request_headers_admin(), json=payload)
        self.assertEqual(response.status_code, 400)

    def test_put_song_by_id_bad_album(self):
        payload = {"album_id": 10000}
        response = self.client.put(self.SONG_URL + '/1', headers=self.request_headers_admin(), json=payload)
        self.assertEqual(response.status_code, 404)

    def test_put_song_by_id_bad_genre(self):
        payload = {"genre_id": 10000}
        response = self.client.put(self.SONG_URL + '/1', headers=self.request_headers_admin(), json=payload)
        self.assertEqual(response.status_code, 404)

    def test_delete_song_by_id(self):
        song = session.query(Song).filter_by(name="puma").first()
        id = str(song.id)
        response = self.client.delete(self.SONG_URL + '/' + id, headers=self.request_headers_admin())
        self.assertEqual(response.status_code, 200)

    def test_delete_song_by_id_no_auth(self):
        payload = {"name": "loser"}
        response = self.client.delete(self.SONG_URL + '/1')
        self.assertEqual(response.status_code, 401)

    def test_delete_song_by_id_notfound(self):
        response = self.client.delete(self.SONG_URL + '/10000', headers=self.request_headers_admin())
        self.assertEqual(response.status_code, 404)

    def test_delete_song_by_id_no_acc(self):
        response = self.client.delete(self.SONG_URL + '/1', headers=self.request_headers_user())
        self.assertEqual(response.status_code, 403)

    def test_get_songs_by_genre(self):
        response = self.client.get(self.SONG_URL + '/genre/rock', headers=self.request_headers_user())
        self.assertEqual(response.status_code, 200)

    def test_get_songs_by_genre_no_auth(self):
        response = self.client.get(self.SONG_URL + '/genre/rock')
        self.assertEqual(response.status_code, 401)

    def test_get_songs_by_genre_notfound(self):
        response = self.client.get(self.SONG_URL + '/genre/nonexist', headers=self.request_headers_user())
        self.assertEqual(response.status_code, 404)

    def test_get_songs_by_language(self):
        response = self.client.get(self.SONG_URL + '/languages/Korean', headers=self.request_headers_user())
        self.assertEqual(response.status_code, 200)

    def test_get_songs_by_language_no_auth(self):
        response = self.client.get(self.SONG_URL + '/languages/Korean')
        self.assertEqual(response.status_code, 401)

    def test_get_songs_by_album(self):
        response = self.client.get(self.SONG_URL + '/album/1', headers=self.request_headers_user())
        self.assertEqual(response.status_code, 200)

    def test_get_songs_by_album_no_auth(self):
        response = self.client.get(self.SONG_URL + '/album/1')
        self.assertEqual(response.status_code, 401)

    def test_get_songs_by_album_notfound(self):
        response = self.client.get(self.SONG_URL + '/album/100000', headers=self.request_headers_user())
        self.assertEqual(response.status_code, 404)

    def test_create_artist_song(self):
        payload = {
            "artist_id": 2,
            "song_id": 1
        }
        response = self.client.post(self.ARTIST_SONG_URL, headers=self.request_headers_admin(), json=payload)
        self.assertEqual(response.status_code, 200)

    def test_create_artist_song_no_acc(self):
        payload = {
            "artist_id": 2,
            "song_id": 1
        }
        response = self.client.post(self.ARTIST_SONG_URL, headers=self.request_headers_user(), json=payload)
        self.assertEqual(response.status_code, 403)

    def test_create_artist_song_no_auth(self):
        payload = {
            "artist_id": 2,
            "song_id": 1
        }
        response = self.client.post(self.ARTIST_SONG_URL, json=payload)
        self.assertEqual(response.status_code, 401)

    def test_create_artist_song_bad_artist(self):
        payload = {
            "artist_id": 10000000,
            "song_id": 1
        }
        response = self.client.post(self.ARTIST_SONG_URL, headers=self.request_headers_admin(), json=payload)
        self.assertEqual(response.status_code, 404)

    def test_create_artist_song_bad_song(self):
        payload = {
            "artist_id": 1,
            "song_id": 1000000
        }
        response = self.client.post(self.ARTIST_SONG_URL, headers=self.request_headers_admin(), json=payload)
        self.assertEqual(response.status_code, 404)

    def test_get_artist_song(self):
        response = self.client.get(self.ARTIST_SONG_URL, headers=self.request_headers_user())
        self.assertEqual(response.status_code, 200)

    def test_get_artist_song_no_auth(self):
        response = self.client.get(self.ARTIST_SONG_URL)
        self.assertEqual(response.status_code, 401)

    def test_get_artist_song_by_artist(self):
        response = self.client.get(self.ARTIST_SONG_URL + '/artist/1', headers=self.request_headers_user())
        self.assertEqual(response.status_code, 200)

    def test_get_artist_song_by_artist_no_auth(self):
        response = self.client.get(self.ARTIST_SONG_URL + '/artist/1')
        self.assertEqual(response.status_code, 401)

    def test_get_artist_song_by_artist_notfound(self):
        response = self.client.get(self.ARTIST_SONG_URL + '/artist/10000', headers=self.request_headers_user())
        self.assertEqual(response.status_code, 404)

    def test_get_artist_song_by_artist_song(self):
        response = self.client.get(self.ARTIST_SONG_URL + '/artist/1/song/1', headers=self.request_headers_user())
        self.assertEqual(response.status_code, 200)

    def test_get_artist_song_by_artist_song_no_auth(self):
        response = self.client.get(self.ARTIST_SONG_URL + '/artist/1/song/1')
        self.assertEqual(response.status_code, 401)

    def test_get_artist_song_by_artist_song_notfound(self):
        response = self.client.get(self.ARTIST_SONG_URL + '/artist/10000/song/100', headers=self.request_headers_user())
        self.assertEqual(response.status_code, 404)

    def test_put_artist_song_by_artist_song(self):
        payload = {
            "artist_id": 1
        }
        response = self.client.put(self.ARTIST_SONG_URL + '/artist/1/song/1', headers=self.request_headers_admin(),
                                   json=payload)
        self.assertEqual(response.status_code, 200)

    def test_put_artist_song_by_artist_song_no_acc(self):
        payload = {
            "artist_id": 1
        }
        response = self.client.put(self.ARTIST_SONG_URL + '/artist/1/song/1', headers=self.request_headers_user(),
                                   json=payload)
        self.assertEqual(response.status_code, 403)

    def test_put_artist_song_by_artist_song_empty(self):
        payload = {}
        response = self.client.put(self.ARTIST_SONG_URL + '/artist/1/song/1', headers=self.request_headers_admin(),
                                   json=payload)
        self.assertEqual(response.status_code, 400)

    def test_put_artist_song_by_artist_song_bad_artist(self):
        payload = {
            "artist_id": 1000
        }
        response = self.client.put(self.ARTIST_SONG_URL + '/artist/1/song/1', headers=self.request_headers_admin(),
                                   json=payload)
        self.assertEqual(response.status_code, 404)

    def test_put_artist_song_by_artist_song_bad_song(self):
        payload = {
            "song_id": 1000
        }
        response = self.client.put(self.ARTIST_SONG_URL + '/artist/1/song/1', headers=self.request_headers_admin(),
                                   json=payload)
        self.assertEqual(response.status_code, 404)

    def test_delete_artist_song_by_artist_song(self):
        response = self.client.delete(self.ARTIST_SONG_URL + '/artist/2/song/1', headers=self.request_headers_admin())
        self.assertEqual(response.status_code, 200)

    def test_create_playlist_song(self):
        payload = {
            "playlist_id": 1,
            "song_id": 1
        }
        response = self.client.post(self.PLAYLIST_SONG_URL, headers=self.request_headers_user_new(), json=payload)
        self.assertEqual(response.status_code, 200)

    def test_create_playlist_song_no_auth(self):
        payload = {
            "playlist_id": 1,
            "song_id": 1
        }
        response = self.client.post(self.PLAYLIST_SONG_URL, json=payload)
        self.assertEqual(response.status_code, 401)

    def test_create_playlist_song_bad_playlist(self):
        payload = {
            "playlist_id": 10000000,
            "song_id": 1
        }
        response = self.client.post(self.PLAYLIST_SONG_URL, headers=self.request_headers_admin(), json=payload)
        self.assertEqual(response.status_code, 404)

    def test_create_playlist_song_bad_song(self):
        payload = {
            "playlist_id": 1,
            "song_id": 1000000
        }
        response = self.client.post(self.PLAYLIST_SONG_URL, headers=self.request_headers_admin(), json=payload)
        self.assertEqual(response.status_code, 404)

    def test_get_playlist_song(self):
        response = self.client.get(self.PLAYLIST_SONG_URL, headers=self.request_headers_user())
        self.assertEqual(response.status_code, 200)

    def test_get_playlist_song_no_auth(self):
        response = self.client.get(self.PLAYLIST_SONG_URL)
        self.assertEqual(response.status_code, 401)

    def test_get_playlist_song_by_id(self):
        response = self.client.get(self.PLAYLIST_SONG_URL + '/playlist/1/song/12', headers=self.request_headers_user_new())
        self.assertEqual(response.status_code, 200)

    def test_get_playlist_song_by_id_no_acc(self):
        response = self.client.get(self.PLAYLIST_SONG_URL + '/playlist/1/song/12', headers=self.request_headers_user())
        self.assertEqual(response.status_code, 403)

    def test_get_playlist_song_by_artist_no_auth(self):
        response = self.client.get(self.PLAYLIST_SONG_URL + '/playlist/1/song/12')
        self.assertEqual(response.status_code, 401)

    def test_get_playlist_song_by_playlist_notfound(self):
        response = self.client.get(self.PLAYLIST_SONG_URL + '/playlist/10000/song/1', headers=self.request_headers_user())
        self.assertEqual(response.status_code, 404)


    def test_get_playlist_song_by_id2(self):
        response = self.client.get(self.PLAYLIST_SONG_URL + '/playlist/1',
                                   headers=self.request_headers_user_new())
        self.assertEqual(response.status_code, 200)

    def test_get_playlist_song_by_id2_notfound(self):
        response = self.client.get(self.PLAYLIST_SONG_URL + '/playlist/1000000',
                                   headers=self.request_headers_user_new())
        self.assertEqual(response.status_code, 404)

    def test_get_playlist_song_by_id2_no_acc(self):
        response = self.client.get(self.PLAYLIST_SONG_URL + '/playlist/1',
                                   headers=self.request_headers_user())
        self.assertEqual(response.status_code, 403)

    # def test_put_playlist_song_by_playlist_song(self):
    #     payload = {
    #         "playlist_id": 1
    #     }
    #     response = self.client.put(self.PLAYLIST_SONG_URL + '/playlist/1/song/1', headers=self.request_headers_admin(),
    #                                json=payload)
    #     self.assertEqual(response.status_code, 200)
    #
    # def test_put_playlist_song_by_artist_song_no_acc(self):
    #     payload = {
    #         "playlist_id": 1
    #     }
    #     response = self.client.put(self.PLAYLIST_SONG_URL + '/playlist/1/song/1', headers=self.request_headers_user(),
    #                                json=payload)
    #     self.assertEqual(response.status_code, 403)
    #
    # def test_put_playlist_song_by_artist_song_empty(self):
    #     payload = {}
    #     response = self.client.put(self.PLAYLIST_SONG_URL + '/playlist/1/song/1', headers=self.request_headers_admin(),
    #                                json=payload)
    #     self.assertEqual(response.status_code, 400)
    #
    # def test_put_playlist_song_by_artist_song_bad_playlist(self):
    #     payload = {
    #         "playlist_id": 1000
    #     }
    #     response = self.client.put(self.PLAYLIST_SONG_URL + '/playlist/1/song/1', headers=self.request_headers_admin(),
    #                                json=payload)
    #     self.assertEqual(response.status_code, 404)
    #
    # def test_put_playlist_song_by_artist_song_bad_song(self):
    #     payload = {
    #         "song_id": 1000
    #     }
    #     response = self.client.put(self.PLAYLIST_SONG_URL + '/playlist/1/song/1', headers=self.request_headers_admin(),
    #                                json=payload)
    #     self.assertEqual(response.status_code, 404)

    def test_delete_playlist_song_by_playlist_song(self):
        response = self.client.delete(self.PLAYLIST_SONG_URL + '/playlist/1/song/1', headers=self.request_headers_user_new())
        self.assertEqual(response.status_code, 200)

    def test_get_user_playlist(self):
        response = self.client.get(self.USER_PLAYLIST_URL + '/userforpl/private', headers=self.request_headers_user_new())
        self.assertEqual(response.status_code, 200)

    def test_get_user_playlist_no_auth(self):
        response = self.client.get(self.USER_PLAYLIST_URL + '/userforpl/private')
        self.assertEqual(response.status_code, 401)

    def test_get_user_playlist_notfound(self):
        response = self.client.get(self.USER_PLAYLIST_URL + '/nonex/private', headers=self.request_headers_user_new())
        self.assertEqual(response.status_code, 404)

    def test_get_user_playlist_all(self):
        response = self.client.get(self.USER_PLAYLIST_URL + '/userforpl', headers=self.request_headers_user_new())
        self.assertEqual(response.status_code, 200)

    def test_get_user_playlist_all_no_auth(self):
        response = self.client.get(self.USER_PLAYLIST_URL + '/userforpl')
        self.assertEqual(response.status_code, 401)

    def test_get_user_playlist_all_notfound(self):
        response = self.client.get(self.USER_PLAYLIST_URL + '/nonex', headers=self.request_headers_user_new())
        self.assertEqual(response.status_code, 404)


if __name__ == '__main__':
    unittest.main()
