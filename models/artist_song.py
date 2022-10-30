from sqlalchemy import Column, Table, ForeignKey
from sqlalchemy.orm import declarative_base


from models.model import Base

artist_song = Table(
    "artist_song",
    Base.metadata,
    Column("artist_id", ForeignKey("artist.id",ondelete="CASCADE")),
    Column("song_id", ForeignKey("song.id", ondelete="CASCADE"))
)
