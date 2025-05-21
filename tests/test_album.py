import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_delete_album():
    # Primero, asegúrate de que exista un artista para asociar el álbum
    artist_data = {
        "stage_name": "AlbumArtist",
        "real_name": "Real",
        "music_genre": "Pop",
        "country_of_origin": "México",
        "email": "albumartist@example.com",
        "instagram_handle": "albumartist"
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
    assert artist_id is not None, "No se encontró el artista para el álbum"

    # Datos del álbum
    album_data = {
        "title": "DeleteAlbum",
        "release_date": None,
        "artist_id": artist_id
    }
    # Intenta crear el álbum (puede fallar por duplicado)
    try:
        client.post("/album/", json=album_data)
    except Exception:
        pass

    # Busca el álbum por título en la lista de álbumes
    list_resp = client.get("/album/")
    assert list_resp.status_code == 200
    albums = list_resp.json()
    album_id = None
    for album in albums:
        if album.get("title") == album_data["title"] and album.get("artist_id") == artist_id:
            album_id = album["id"]
            break
    assert album_id is not None, "No se encontró el álbum recién creado o existente"

    # Elimina el álbum
    response = client.delete(f"/album/{album_id}")
    assert response.status_code == 200

    # Verifica que ya no existe
    response = client.get(f"/album/{album_id}")
    assert response.status_code == 404