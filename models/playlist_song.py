from sqlalchemy import Column, Table, ForeignKey

from models.model import Base

playlist_song = Table(
    "playlist_song",
    Base.metadata,
    Column("playlist_id", ForeignKey("playlist.id", ondelete="CASCADE")),
    Column("song_id", ForeignKey("song.id", ondelete="CASCADE"))
)