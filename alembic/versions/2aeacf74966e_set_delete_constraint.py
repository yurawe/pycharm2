"""set delete constraint

Revision ID: 2aeacf74966e
Revises: bec87187ef99
Create Date: 2022-10-23 14:07:32.709552

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2aeacf74966e'
down_revision = 'bec87187ef99'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('artist_song_ibfk_1', 'artist_song', type_='foreignkey')
    op.drop_constraint('artist_song_ibfk_2', 'artist_song', type_='foreignkey')
    op.create_foreign_key('artist_song_ibfk_1', 'artist_song', 'artist', ['artist_id'], ['id'], ondelete='CASCADE')
    op.create_foreign_key('artist_song_ibfk_2', 'artist_song', 'song', ['song_id'], ['id'], ondelete='CASCADE')
    op.drop_constraint('playlist_song_ibfk_2', 'playlist_song', type_='foreignkey')
    op.drop_constraint('playlist_song_ibfk_1', 'playlist_song', type_='foreignkey')
    op.create_foreign_key('playlist_song_ibfk_1', 'playlist_song', 'song', ['song_id'], ['id'], ondelete='CASCADE')
    op.create_foreign_key('playlist_song_ibfk_2', 'playlist_song', 'playlist', ['playlist_id'], ['id'], ondelete='CASCADE')
    op.drop_constraint('song_ibfk_1', 'song', type_='foreignkey')
    op.drop_constraint('song_ibfk_2', 'song', type_='foreignkey')
    op.create_foreign_key('song_ibfk_1', 'song', 'genre', ['genre_id'], ['id'], ondelete='CASCADE')
    op.create_foreign_key('song_ibfk_2', 'song', 'album', ['album_id'], ['id'], ondelete='CASCADE')
    op.drop_constraint('user_playlist_ibfk_1', 'user_playlist', type_='foreignkey')
    op.drop_constraint('user_playlist_ibfk_2', 'user_playlist', type_='foreignkey')
    op.create_foreign_key('user_playlist_ibfk_1', 'user_playlist', 'playlist', ['playlist_id'], ['id'], ondelete='CASCADE')
    op.create_foreign_key('user_playlist_ibfk_2', 'user_playlist', 'user', ['user_id'], ['id'], ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('user_playlist_ibfk_1', 'user_playlist', type_='foreignkey')
    op.drop_constraint('user_playlist_ibfk_2', 'user_playlist', type_='foreignkey')
    op.create_foreign_key('user_playlist_ibfk_2', 'user_playlist', 'user', ['user_id'], ['id'])
    op.create_foreign_key('user_playlist_ibfk_1', 'user_playlist', 'playlist', ['playlist_id'], ['id'])
    op.drop_constraint('song_ibfk_1', 'song', type_='foreignkey')
    op.drop_constraint('song_ibfk_2', 'song', type_='foreignkey')
    op.create_foreign_key('song_ibfk_2', 'song', 'genre', ['genre_id'], ['id'])
    op.create_foreign_key('song_ibfk_1', 'song', 'album', ['album_id'], ['id'])
    op.drop_constraint('playlist_song_ibfk_1', 'playlist_song', type_='foreignkey')
    op.drop_constraint('playlist_song_ibfk_2', 'playlist_song', type_='foreignkey')
    op.create_foreign_key('playlist_song_ibfk_1', 'playlist_song', 'playlist', ['playlist_id'], ['id'])
    op.create_foreign_key('playlist_song_ibfk_2', 'playlist_song', 'song', ['song_id'], ['id'])
    op.drop_constraint('artist_song_ibfk_1', 'artist_song', type_='foreignkey')
    op.drop_constraint('artist_song_ibfk_2', 'artist_song', type_='foreignkey')
    op.create_foreign_key('artist_song_ibfk_2', 'artist_song', 'song', ['song_id'], ['id'])
    op.create_foreign_key('artist_song_ibfk_1', 'artist_song', 'artist', ['artist_id'], ['id'])
    # ### end Alembic commands ###