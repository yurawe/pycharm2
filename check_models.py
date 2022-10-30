from models.model import Session
from models.album import Album
from models.artist import Artist
from models.artist_song import artist_song
from models.genre import Genre
from models.playlist import Playlist
from datetime import date
from models.playlist_song import playlist_song
from models.song import Song
from models.user import User
from models.user_playlist import user_playlist

session = Session()
print('Starting')
album1 = Album(id=1, name='One-X')
artist1 = Artist(id=1, name='Three Days Grace', country='Canada')
genre1 = Genre(id=1, name='Rock')
playlist1 = Playlist(id=1, is_private=True, created_at=date.today(), updated_at=date.today())
user1 = User(id=1, first_name='John', last_name='Smith', email='john@gmail.com', phone=None, password='some_hash_pass')
song1 = Song(id=1, name='Time of Dying', length=3.06, language='English', release_date=date(2006, 6, 25), genre_id=1,
             album_id=1)
user2 = User(id=2, first_name='Jim', last_name='Ray', email='ray@gmail.com', phone=None, password='some_hash_pass2')

genre2 = Genre(id=2, name='Pop')
artist2 = Artist(id=2, name='Ed Sheeran', country='England')
album2 = Album(id=2,name='Some_name')
song2 = Song(id=2, name='Shape of you', length=3.26, language='English',release_date=date(2019,10,10), genre_id=2, album_id= 2)
playlist2 = Playlist(id=2, is_private=False, created_at=date.today(), updated_at=date.today())

session.add(playlist2)
session.add(album1)
session.add(artist1)
session.add(genre1)
session.add(song1)
session.add(user1)
session.add(playlist1)
session.add(song2)
session.add(user2)
session.add(artist2)
session.add(album2)
session.add(genre2)
user1.playlists.append(playlist1)
playlist1.songs.append(song1)
artist1.songs.append(song1)
artist2.songs.append(song2)
playlist1.songs.append(song2)
user1.playlists.append(playlist2)

print(artist1)

session.commit()
print('Committed')