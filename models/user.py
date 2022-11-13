from sqlalchemy import Column, Integer, String, UniqueConstraint
from sqlalchemy.orm import relationship
from models.user_playlist import user_playlist

from models.model import Base


class User(Base):
    __tablename__ = "user"
    __table_args__ = (UniqueConstraint("email"),)
    id = Column(Integer, primary_key=True)
    first_name = Column(String(25), nullable=False)
    last_name = Column(String(25), nullable=False)
    email = Column(String(25), nullable=False)
    phone = Column(String(25), nullable=True)
    password = Column(String(512), nullable=False)
    username = Column(String(25), unique=True, nullable=False)
    playlists = relationship("Playlist", secondary=user_playlist, passive_deletes=True)
