# uvicorn main:app --reload
# http://127.0.0.1:8000/redoc
# http://127.0.0.1:8000/docs

from fastapi import FastAPI, Depends, HTTPException
import services, schemas
from db import get_db
from sqlalchemy.orm import Session

#services: Aquí están las funciones que hacen la lógica real de CRUD.
#schemas: Valida y estructura la entrada/salida de datos.
#models: Define cómo son tus tablas SQL.

#main.py es el punto de entrada principal de tu aplicación FastAPI.
#  Es donde se define cómo se comporta tu API: qué rutas existen, qué hacen y cómo interactúan con la base de datos.

#En FastAPI, el decorador @app.get(...) o @app.post(...)
# le dice a la aplicación que esa función se debe ejecutar cuando un cliente (como un navegador o frontend) haga una petición HTTP de cierto tipo a cierta URL.

app = FastAPI() #crea la aplicacion web

#ARTIST--------------------------------------------------------------------------------------------------------
@app.get("/artist/", response_model=list[schemas.ArtistResponse], tags=["Artistas"])
def get_all_artist(db: Session = Depends(get_db)):  #Depends(get_db): Inyecta automáticamente una sesión de la base de datos a cada función.
    return services.get_all_artists(db)

@app.get("/artists/{id}", response_model= schemas.ArtistResponse, tags=["Artistas"])
def get_artist_by_id(id: int, db: Session= Depends(get_db)):
    artist_queryset = services.get_artist_by_id(db, id)
    if artist_queryset:
        return artist_queryset
    raise HTTPException(status_code= 404, detail="Invalid artist id Provided")

@app.get("/artists/by-name/{name}", response_model= schemas.ArtistResponse, tags=["Artistas"])
def get_artist_by_name(name : str, db: Session = Depends(get_db)):
    artist_queryset = services.get_artist_by_name(db, name)
    if artist_queryset:
        return artist_queryset
    raise HTTPException(status_code = 404, detail="Artist not Found")

@app.post("/artist/", response_model=schemas.ArtistCreate, tags=["Artistas"])     #Recibe un JSON con la info del artista y lo guarda en la base de datos.
def create_artist(artist : schemas.ArtistCreate, db: Session = Depends(get_db)):
    return services.create_artist(db, artist)

@app.put("/artist/{id}", response_model=schemas.ArtistResponse, tags=["Artistas"])
def update_artist(artist : schemas.ArtistCreate, id: int, db: Session = Depends(get_db)): #artist son los nuevos datos validados por artist create
    db_update = services.update_artist(db, artist,id)
    if not db_update:
        raise HTTPException(status_code=404, detail="Artist not Found")
    return db_update

@app.delete("/artists/{id}", response_model= schemas.ArtistResponse, tags=["Artistas"])
def delete_artist(id: int, db: Session = Depends(get_db)):
    delete_entry = services.delete_artist(db,id)
    if delete_entry:
        return delete_entry
    raise HTTPException(status_code=404, detail = "Artist not Found")

#ALBUM---------------------------------------------------------------------------------------------------
@app.get("/album/", response_model=list[schemas.AlbumResponse], tags=["Albums"])
def get_all_albums(db: Session = Depends(get_db)):
    return services.get_all_albums(db)

@app.get("/album/{id}", response_model= schemas.AlbumResponse, tags=["Albums"])
def get_album_by_id(id: int, db: Session= Depends(get_db)):
    album_queryset = services.get_album_by_id(db, id)
    if album_queryset:
        return album_queryset
    raise HTTPException(status_code= 404, detail="Invalid album id Provided")

@app.get("/album/by-name/{name}", response_model= schemas.AlbumResponse, tags=["Albums"])
def get_album_by_name(name : str, db: Session = Depends(get_db)):
    album_queryset = services.get_album_by_name(db, name)
    if album_queryset:
        return album_queryset
    raise HTTPException(status_code = 404, detail="Album not Found")

@app.post("/album/", response_model=schemas.AlbumCreate, tags=["Albums"])
def create_album(album : schemas.AlbumCreate, db: Session = Depends(get_db)):
    return services.create_album(db, album)

@app.put("/album/{id}", response_model=schemas.AlbumResponse, tags=["Albums"])
def update_album(album : schemas.AlbumCreate, id: int, db: Session = Depends(get_db)):
    db_update = services.update_album(db, id, album)
    if not db_update:
        raise HTTPException(status_code=404, detail="Album not Found")
    return db_update

@app.delete("/album/{id}", response_model= schemas.AlbumResponse, tags=["Albums"])
def delete_album(id: int, db: Session = Depends(get_db)):
    delete_entry = services.delete_album(db,id)
    if delete_entry:
        return delete_entry
    raise HTTPException(status_code=404, detail = "Album not Found")

#SONGS-----------------------------------------------------------------------------------------
@app.post("/song/", response_model=schemas.SongCreate, tags=["Songs"])
def create_song(song: schemas.SongCreate, db: Session = Depends(get_db)):
    return services.create_song(db, song)

@app.put("/song/{id}", response_model=schemas.SongResponse, tags=["Songs"])
def update_song(song : schemas.SongCreate, id: int, db: Session = Depends(get_db)):
    db_update = services.update_song(db, id, song)
    if not db_update:
        raise HTTPException(status_code=404, detail="Song not Found")
    return db_update

@app.get("/song/", response_model=list[schemas.SongResponse], tags=["Songs"])   #@app.get("/artist/") está diciendo:
def get_all_songs(db: Session = Depends(get_db)):                               #“Cuando alguien haga un GET a la ruta /artist/, ejecuta la función get_all_artists()”.
    return services.get_all_songs(db)

@app.get("/song/{id}", response_model= schemas.SongResponse, tags=["Songs"])
def get_song_by_id(id: int, db: Session= Depends(get_db)):
    song_queryset = services.get_song_by_id(db, id)
    if song_queryset:
        return song_queryset
    raise HTTPException(status_code= 404, detail="Invalid song id Provided")

@app.get("/song/by-name/{title}", response_model= schemas.SongResponse, tags=["Songs"])
def get_song_by_title(title : str, db: Session = Depends(get_db)):
    song_queryset = services.get_song_by_title(db, title)
    if song_queryset:
        return song_queryset
    raise HTTPException(status_code = 404, detail="Song not Found")


@app.delete("/song/{id}", response_model= schemas.SongResponse, tags=["Songs"])
def delete_song(id: int, db: Session = Depends(get_db)):
    delete_entry = services.delete_song(db,id)
    if delete_entry:
        return delete_entry
    raise HTTPException(status_code=404, detail = "Song not Found")

