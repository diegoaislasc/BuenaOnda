from db import Base
from sqlalchemy import Integer, Column, String, Date, ForeignKey, Table, Numeric
from sqlalchemy.orm import relationship

#models.py no crea la base de datos por sí solo, pero le dice a SQLAlchemy cómo se ve la base para que pueda trabajar con ella desde Python.
#models.py es la forma en que SQLAlchemy “entiende” cómo están estructuradas tus tablas. Aunque las tablas ya existan en la base de datos, SQLAlchemy necesita conocer:
#Nombre de la tabla: para saber contra qué tabla hacer SELECT, INSERT, etc.
#Nombres y tipos de columnas: para poder mapear los datos correctamente.
#Relaciones entre tablas: para hacer JOIN, acceder a claves foráneas, y usar relationship().
#Piensa en models.py como el “mapa” que SQLAlchemy necesita para moverse por la base de datos.

# Artist model
class Artist(Base):
    __tablename__ = 'artist'

    id: int = Column(Integer, primary_key=True)
    real_name: str = Column(String(255))
    stage_name: str = Column(String(255), nullable=False, unique=True)
    music_genre: str = Column(String(255))
    country_of_origin: str = Column(String(255))
    email: str = Column(String(255), unique=True)
    instagram_handle: str = Column(String(30), unique=True)

    # Relationships
    albums = relationship("Album", back_populates="artist", cascade="all, delete-orphan")
    # events = relationship("Event", secondary="artist_event", back_populates="artists")
    # services = relationship("Service", secondary="artist_service", back_populates="artists")

    def __repr__(self):
        return f"<Artist(stage_name='{self.stage_name}', real_name='{self.real_name}')>"


# Album model
class Album(Base):
    __tablename__ = 'album'

    id: int = Column(Integer, primary_key=True)
    title: str = Column(String(255), nullable=False)
    release_date: Date = Column(Date)
    artist_id: int = Column(Integer, ForeignKey('artist.id', ondelete='CASCADE'), nullable=False)

    # Relationships
    artist = relationship("Artist", back_populates="albums")
    songs = relationship("Song", back_populates="album", cascade="all, delete-orphan")
    #studios = relationship("Studio", secondary="album_studio", back_populates="albums")

    def __repr__(self):
        return f"<Album(title='{self.title}', artist_id={self.artist_id})>"


#Song model
class Song(Base):
    __tablename__ = 'song'

    id: int = Column(Integer, primary_key=True)
    title: str = Column(String(255), nullable=False)
    duration: int = Column(Integer)
    album_id: int = Column(Integer, ForeignKey('album.id', ondelete='CASCADE'), nullable=False)

    # Relationships
    album = relationship("Album", back_populates="songs")
    #producers = relationship("Producer", secondary="song_producer", back_populates="songs")
    #songwriters = relationship("Songwriter", secondary="songwriter_song", back_populates="songs")

    def __repr__(self):
        return f"<Song(title='{self.title}', album_id={self.album_id})>"
