import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_delete_artist():
    # Datos del artista
    artist_data = {
        "stage_name": "DeleteArtist",
        "real_name": "Real",
        "music_genre": "Blues",
        "country_of_origin": "Perú",
        "email": "deleteartist@example.com",
        "instagram_handle": "deleteartist"
    }
    # Intenta crear el artista (puede fallar por duplicado)
    try:
        create_resp = client.post("/artist/", json=artist_data)
    except Exception:
        # Si hay error de validación, lo ignoramos (el artista puede existir)
        pass

    # Busca el artista por email en la lista de artistas
    list_resp = client.get("/artist/")
    assert list_resp.status_code == 200
    artists = list_resp.json()
    artist_id = None
    for artist in artists:
        if artist.get("email") == artist_data["email"]:
            artist_id = artist["id"]
            break
    assert artist_id is not None, "No se encontró el artista recién creado o existente"

    # Elimina el artista
    response = client.delete(f"/artists/{artist_id}")
    assert response.status_code == 200

    # Verifica que ya no existe
    response = client.get(f"/artists/{artist_id}")
    assert response.status_code == 404