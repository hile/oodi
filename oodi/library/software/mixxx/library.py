"""
Mixxx database loading
"""

import os

from systematic.sqlite import SQLiteDatabase

MIXXX_DATABASE_PATHS = (
    os.path.expanduser('~/.config/mixxx/mixxxdb.sqlite'),
    os.path.expanduser('~/Library/Application Support/Mixxx/mixxxdb.sqlite'),
)


class MixxxDatabaseError(Exception):
    pass


class MixxxTrack:
    def __init__(self, db, id, path):
        self.db = db
        self.id = id
        self.path = path

    def __repr__(self):
        return self.path

    @property
    def details(self):
        """
        Return track details
        """
        cursor = self.db.cursor
        cursor.execute("""
            SELECT composer, artist, title, album, genre, comment, url,
                   grouping, album_artist,
                   tracknumber, year, duration, bitrate, samplerate, key, bpm, channels, rating
            FROM library
            WHERE id = ?
        """, (self.id, ))

        data = self.db.as_dict(cursor, cursor.fetchone())
        for key in ('duration', 'bitrate', 'samplerate', 'channels', 'tracknumber', 'rating'):
            try:
                data[key] = int(data[key])
            except Exception:
                pass

        for key in ('bpm', ):
            try:
                data[key] = float(data[key])
            except Exception:
                pass

        return data


class MixxxDatabase(SQLiteDatabase):
    """
    Mixxx library database
    """
    def __init__(self, db_path=None):
        if db_path is None:
            db_path = self.__discover_database_path__()
        super().__init__(db_path)

    def __discover_database_path__(self):
        """
        Discover path to mixxx database. Varies by platform
        """
        for path in MIXXX_DATABASE_PATHS:
            if os.path.isfile(path):
                return path
        raise MixxxDatabaseError('Mixxx database not found')

    @property
    def tracks(self):
        cursor = self.cursor
        cursor.execute("""SELECT id, location FROM track_locations ORDER BY location""")
        return [MixxxTrack(self, *record) for record in cursor.fetchall()]

    def get_track(self, path):
        cursor = self.cursor
        cursor.execute("""SELECT id, location FROM track_locations WHERE location=?""", (path,))
        return MixxxTrack(self, *cursor.fetchone())
