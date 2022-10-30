from sqlalchemy import Column, Integer, String, Date, Float, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
from models.artist_song import artist_song
from models.playlist_song import playlist_song

from models.model import Base


class Song(Base):
    __tablename__ = "song"
    id = Column(Integer, primary_key=True)
    name = Column(String(25), nullable=False)
    length = Column(Float, nullable=False)
    language = Column(String(25), nullable=False)
    release_date = Column(Date, nullable=False)
    genre_id = Column(Integer, ForeignKey("genre.id", ondelete="CASCADE"))
    album_id = Column(Integer, ForeignKey("album.id", ondelete="CASCADE"))

