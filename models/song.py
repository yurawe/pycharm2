from sqlalchemy import Column, Integer, String, Date, Float, ForeignKey, orm
from sqlalchemy.orm import declarative_base, relationship, backref

from models.album import Album
from models.artist_song import artist_song
from models.genre import Genre
from models.playlist_song import playlist_song

from models.model import Base


class Song(Base):
    __tablename__ = "song"
    id = Column(Integer, primary_key=True)
    name = Column(String(25), nullable=False)
    length = Column(Float, nullable=False)
    language = Column(String(25), nullable=False)
    release_date = Column(Date, nullable=False)
    genre_id = Column(Integer, ForeignKey("genre.id", ondelete="SET NULL"))
    album_id = Column(Integer, ForeignKey("album.id", ondelete="CASCADE"))
    genre = orm.relationship(Genre, backref="song")
    album = orm.relationship(Album, backref=backref("song", cascade="all, delete"))
