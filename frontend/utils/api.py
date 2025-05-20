import requests
from typing import Dict, List, Any, Optional

class APIClient:
    """
    Cliente para interactuar con la API REST de Buena Onda Música.
    Implementa métodos para realizar operaciones CRUD en las diferentes entidades.
    """
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        """
        Inicializa el cliente API con la URL base.
        
        Args:
            base_url: URL base de la API REST
        """
        self.base_url = base_url
        
    def _handle_response(self, response):
        """
        Maneja la respuesta de la API, verificando errores y devolviendo datos.
        
        Args:
            response: Objeto de respuesta de requests
            
        Returns:
            Datos de la respuesta o None en caso de error
        """
        try:
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            print(f"Error HTTP: {e}")
            return None
        except requests.exceptions.ConnectionError:
            print("Error de conexión: No se pudo conectar a la API")
            return None
        except requests.exceptions.Timeout:
            print("Error de tiempo de espera: La solicitud tomó demasiado tiempo")
            return None
        except requests.exceptions.RequestException as e:
            print(f"Error en la solicitud: {e}")
            return None
        except ValueError:
            print("Error al procesar la respuesta JSON")
            return None
    
    # Métodos para Artistas
    def get_all_artists(self) -> List[Dict[str, Any]]:
        """Obtiene todos los artistas"""
        response = requests.get(f"{self.base_url}/artist/")
        return self._handle_response(response) or []
    
    def get_artist_by_id(self, artist_id: int) -> Optional[Dict[str, Any]]:
        """Obtiene un artista por su ID"""
        response = requests.get(f"{self.base_url}/artists/{artist_id}")
        return self._handle_response(response)
    
    def create_artist(self, artist_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Crea un nuevo artista"""
        response = requests.post(f"{self.base_url}/artist/", json=artist_data)
        return self._handle_response(response)
    
    def update_artist(self, artist_id: int, artist_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Actualiza un artista existente"""
        response = requests.put(f"{self.base_url}/artist/{artist_id}", json=artist_data)
        return self._handle_response(response)
    
    def delete_artist(self, artist_id: int) -> Optional[Dict[str, Any]]:
        """Elimina un artista por su ID"""
        response = requests.delete(f"{self.base_url}/artists/{artist_id}")
        return self._handle_response(response)
    
    # Métodos para Álbumes
    def get_all_albums(self) -> List[Dict[str, Any]]:
        """Obtiene todos los álbumes"""
        response = requests.get(f"{self.base_url}/album/")
        return self._handle_response(response) or []
    
    def get_album_by_id(self, album_id: int) -> Optional[Dict[str, Any]]:
        """Obtiene un álbum por su ID"""
        response = requests.get(f"{self.base_url}/album/{album_id}")
        return self._handle_response(response)
    
    def create_album(self, album_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Crea un nuevo álbum"""
        response = requests.post(f"{self.base_url}/album/", json=album_data)
        return self._handle_response(response)
    
    def update_album(self, album_id: int, album_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Actualiza un álbum existente"""
        response = requests.put(f"{self.base_url}/album/{album_id}", json=album_data)
        return self._handle_response(response)
    
    def delete_album(self, album_id: int) -> Optional[Dict[str, Any]]:
        """Elimina un álbum por su ID"""
        response = requests.delete(f"{self.base_url}/album/{album_id}")
        return self._handle_response(response)
    
    # Métodos para Canciones
    def get_all_songs(self) -> List[Dict[str, Any]]:
        """Obtiene todas las canciones"""
        response = requests.get(f"{self.base_url}/song/")
        return self._handle_response(response) or []
    
    def get_song_by_id(self, song_id: int) -> Optional[Dict[str, Any]]:
        """Obtiene una canción por su ID"""
        response = requests.get(f"{self.base_url}/song/{song_id}")
        return self._handle_response(response)
    
    def create_song(self, song_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Crea una nueva canción"""
        response = requests.post(f"{self.base_url}/song/", json=song_data)
        return self._handle_response(response)
    
    def update_song(self, song_id: int, song_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Actualiza una canción existente"""
        response = requests.put(f"{self.base_url}/song/{song_id}", json=song_data)
        return self._handle_response(response)
    
    def delete_song(self, song_id: int) -> Optional[Dict[str, Any]]:
        """Elimina una canción por su ID"""
        response = requests.delete(f"{self.base_url}/song/{song_id}")
        return self._handle_response(response)
