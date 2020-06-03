"""Models for Spotify user data viz app."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    """Data model for Spotify user of app"""

    __tablename__ = "users"

    #get user_id from API
    user_id = db.Column(db.String, primary_key=True)
    display_name = db.Column(db.String)
    image_url = db.Column(db.String) #use type text?

    artists = db.relationship("Artist",
                             secondary="user_artists",
                             backref="users")

    tracks = db.relationship("Track",
                             secondary="user_tracks",
                             backref="users")


class UserArtist(db.Model):
    """Association table for users and artists"""

    __tablename__ = "user_artists"

    userartist_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.String, db.ForeignKey('users.user_id'))
    artist_id = db.Column(db.String, db.ForeignKey('artists.artist_id'))


class UserTrack(db.Model):
    """Association table for users and tracks"""

    __tablename__ = "user_tracks"

    usertrack_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.String, db.ForeignKey('users.user_id'))
    track_id = track_id = db.Column(db.String, db.ForeignKey('tracks.track_id'))

class Artist(db.Model):
    """Data model for Spotify artist"""

    __tablename__ = "artists"

    artist_id = db.Column(db.String, primary_key=True)
    artist_name = db.Column(db.String)
    popularity = db.Column(db.Integer)

    #users relationship to User objects

    related = db.relationship("RelatedArtist", backref="artists")

    genres = db.relationship("Genre",
                         secondary="artist_genres",
                         backref="artists")

    tracks = db.relationship("Track", backref="artists")

    def __repr__(self):
        """Return a human-readable representation of a Human."""

        return f"<Artist artist_id={self.artist_id} artist_name={self.artist_name}>"


class RelatedArtist(db.Model):
    """Data model for related artists to Artist objects"""

    __tablename__ = "related_artists"

    pair_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    search_artist_id = db.Column(db.String, db.ForeignKey('artists.artist_id'))
    related_artist_id = db.Column(db.String)

    #artists relationship to Artist objects

class Genre(db.Model):
    """Data model for Spotify genres"""

    __tablename__ = "genres"

    genre_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    genre = db.Column(db.String(50))

    #artists relationship to Artist objects

class ArtistGenre(db.Model):
    """Association table for artists and genres"""

    __tablename__ = "artist_genres"

    artistgenre_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    artist_id = db.Column(db.String, db.ForeignKey('artists.artist_id'))
    genre_id = db.Column(db.Integer, db.ForeignKey('genres.genre_id'))


class Track(db.Model):
    """Data model for a Spotify track"""

    __tablename__ = "tracks"

    track_id = db.Column(db.String, primary_key=True)
    artist_id = db.Column(db.String, db.ForeignKey('artists.artist_id'))
    track_name = db.Column(db.String)

    #users relationship to User objects
    #artists relationship to Artist objects

    audio = db.relationship("Audio", backref="tracks")


class Audio(db.Model):
    """Spotify audio features for tracks"""

    __tablename__ = "audio_features"

    audio_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    track_id = db.Column(db.String, db.ForeignKey('tracks.track_id'))
    danceability = db.Column(db.Float)
    energy = db.Column(db.Float)
    speechiness = db.Column(db.Float)
    acousticness = db.Column(db.Float)
    instrumentalness = db.Column(db.Float)
    liveness = db.Column(db.Float)

    #tracks relationship to Track objects



def connect_to_db(flask_app, db_uri='postgresql:///synaesthetic', echo=True):
    """Connect the database to Flask app."""

    flask_app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    flask_app.config['SQLALCHEMY_ECHO'] = echo
    flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.app = flask_app
    db.init_app(flask_app)

    print('Connected to the db!')


if __name__ == '__main__':
    from server import app

    # Call connect_to_db(app, echo=False) if your program output gets
    # too annoying; this will tell SQLAlchemy not to print out every
    # query it executes.

    connect_to_db(app)