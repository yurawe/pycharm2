from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from models.model import Base


class Album(Base):
    __tablename__ = "album"
    id = Column(Integer, primary_key=True)
    name = Column(String(25), nullable=False)
    songs = relationship("Song", backref="albums", passive_deletes=True)
