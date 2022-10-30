from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import declarative_base, relationship
from models.artist_song import artist_song

from models.model import Base


class Artist(Base):
    __tablename__ = "artist"
    id = Column(Integer, primary_key=True)
    name = Column(String(25), nullable=False)
    date_of_birth = Column(Date, nullable=True)
    country = Column(String(25), nullable=False)
    songs = relationship("Song", passive_deletes=True, secondary=artist_song)
