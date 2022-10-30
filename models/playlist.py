from sqlalchemy import Column, Integer, Boolean, Date
from sqlalchemy.orm import declarative_base, relationship

from models.user_playlist import user_playlist
from models.playlist_song import playlist_song

from models.model import Base


class Playlist(Base):
    __tablename__ = "playlist"
    id = Column(Integer, primary_key=True)
    is_private = Column(Boolean, nullable=False)
    created_at = Column(Date, nullable=False)
    updated_at = Column(Date, nullable=False)
    songs = relationship("Song",  secondary=playlist_song, passive_deletes=True)
