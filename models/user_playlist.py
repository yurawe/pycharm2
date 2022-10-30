from sqlalchemy import Column, Table, ForeignKey
from models.model import Base

user_playlist = Table(
    "user_playlist",
    Base.metadata,
    Column("playlist_id", ForeignKey("playlist.id", ondelete="CASCADE")),
    Column("user_id", ForeignKey("user.id", ondelete="CASCADE"))
)

