import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_delete_song():
    # Primero, asegúrate de que exista un artista y un álbum para asociar la canción
    artist_data = {
        "stage_name": "SongArtist",
        "real_name": "Real",
        "music_genre": "Jazz",
        "country_of_origin": "Chile",
        "email": "songartist@example.com",
        "instagram_handle": "songartist"
    }
    try:
        client.post("/artist/", json=artist_data)
    except Exception:
        pass

    # Busca el id del artista
    list_resp = client.get("/artist/")
    assert list_resp.status_code == 200
    artists = list_resp.json()
    artist_id = None
    for artist in artists:
        if artist.get("email") == artist_data["email"]:
            artist_id = artist["id"]
            break
    assert artist_id is not None, "No se encontró el artista para la canción"

    # Crea un álbum para la canción
    album_data = {
        "title": "SongAlbum",
        "release_date": None,
        "artist_id": artist_id
    }
    try:
        client.post("/album/", json=album_data)
    except Exception:
        pass

    # Busca el id del álbum
    list_resp = client.get("/album/")
    assert list_resp.status_code == 200
    albums = list_resp.json()
    album_id = None
    for album in albums:
        if album.get("title") == album_data["title"] and album.get("artist_id") == artist_id:
            album_id = album["id"]
            break
    assert album_id is not None, "No se encontró el álbum para la canción"

    # Datos de la canción
    song_data = {
        "title": "DeleteSong",
        "duration": 180,
        "album_id": album_id
    }
    # Intenta crear la canción (puede fallar por duplicado)
    try:
        client.post("/song/", json=song_data)
    except Exception:
        pass

    # Busca la canción por título y álbum en la lista de canciones
    list_resp = client.get("/song/")
    assert list_resp.status_code == 200
    songs = list_resp.json()
    song_id = None
    for song in songs:
        if song.get("title") == song_data["title"] and song.get("album_id") == album_id:
            song_id = song["id"]
            break
    assert song_id is not None, "No se encontró la canción recién creada o existente"

    # Elimina la canción
    response = client.delete(f"/song/{song_id}")
    assert response.status_code == 200

    # Verifica que ya no existe
    response = client.get(f"/song/{song_id}")
    assert response.status_code == 404