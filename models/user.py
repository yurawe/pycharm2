from sqlalchemy import Column, Integer, String, UniqueConstraint
from sqlalchemy.orm import relationship
from models.user_playlist import user_playlist

from models.model import Base, Session

session = Session()


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

    @classmethod
    def get_by_username(cls, username):
        user = session.query(User).filter_by(username=username).first()
        return user

    @classmethod
    def get_by_email(cls, email):
        user = session.query(User).filter_by(email=email).first()
        return user

    def save_to_db(self):
        session.add(self)
        session.commit()
