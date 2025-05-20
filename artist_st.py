import streamlit as st
from typing import Dict, List, Any, Optional
from base_st import CRUDView
from api_st import APIClient

class ArtistView(CRUDView):
    """
    Vista para gestionar artistas en Streamlit.
    Implementa operaciones CRUD para la entidad Artist.
    """
    
    def __init__(self, api_client: APIClient):
        """
        Inicializa la vista de artistas.
        
        Args:
            api_client: Cliente API para interactuar con el backend
        """
        super().__init__("Gestión de Artistas")
        self.api_client = api_client
    
    def render_list_view(self):
        """Renderiza la vista de listado de artistas"""
        st.header("Lista de Artistas")
        
        # Obtener todos los artistas
        artists = self.get_all_items()
        
        # Mostrar tabla de artistas
        if artists:
            self.display_data_table(
                artists, 
                ["id", "stage_name", "real_name", "music_genre", "country_of_origin", "email", "instagram_handle"]
            )
            
            # Opción para ver álbumes de un artista
            st.subheader("Ver álbumes por artista")
            artist_ids = [artist["id"] for artist in artists]
            artist_names = [artist["stage_name"] for artist in artists]
            artist_dict = dict(zip(artist_names, artist_ids))
            
            selected_artist = st.selectbox("Seleccionar artista", artist_names)
            if selected_artist:
                self.show_artist_albums(artist_dict[selected_artist])
        else:
            st.info("No hay artistas registrados")
    
    def show_artist_albums(self, artist_id: int):
        """
        Muestra los álbumes de un artista específico.
        
        Args:
            artist_id: ID del artista
        """
        # Obtener todos los álbumes
        albums = self.api_client.get_all_albums()
        
        # Filtrar álbumes del artista seleccionado
        artist_albums = [album for album in albums if album["artist_id"] == artist_id]
        
        if artist_albums:
            st.write(f"Álbumes del artista (Total: {len(artist_albums)})")
            self.display_data_table(artist_albums, ["id", "title", "release_date"])
            
            # Opción para ver canciones de un álbum
            st.subheader("Ver canciones por álbum")
            album_ids = [album["id"] for album in artist_albums]
            album_titles = [album["title"] for album in artist_albums]
            album_dict = dict(zip(album_titles, album_ids))
            
            if album_titles:
                selected_album = st.selectbox("Seleccionar álbum", album_titles)
                if selected_album:
                    self.show_album_songs(album_dict[selected_album])
        else:
            st.info("Este artista no tiene álbumes registrados")
    
    def show_album_songs(self, album_id: int):
        """
        Muestra las canciones de un álbum específico.
        
        Args:
            album_id: ID del álbum
        """
        # Obtener todas las canciones
        songs = self.api_client.get_all_songs()
        
        # Filtrar canciones del álbum seleccionado
        album_songs = [song for song in songs if song["album_id"] == album_id]
        
        if album_songs:
            st.write(f"Canciones del álbum (Total: {len(album_songs)})")
            
            # Formatear duración de segundos a minutos:segundos
            for song in album_songs:
                minutes = song["duration"] // 60
                seconds = song["duration"] % 60
                song["duration_formatted"] = f"{minutes}:{seconds:02d}"
            
            self.display_data_table(album_songs, ["id", "title", "duration_formatted"])
        else:
            st.info("Este álbum no tiene canciones registradas")
    
    def render_create_view(self):
        """Renderiza la vista de creación de artistas"""
        st.header("Crear Nuevo Artista")
        
        # Formulario para crear artista
        with st.form("create_artist_form"):
            stage_name = st.text_input("Nombre Artístico *", help="Campo obligatorio")
            real_name = st.text_input("Nombre Real")
            music_genre = st.text_input("Género Musical")
            country = st.text_input("País de Origen")
            email = st.text_input("Email")
            instagram = st.text_input("Instagram")
            
            submit_button = st.form_submit_button("Crear Artista")
            
            if submit_button:
                if not stage_name:
                    self.display_error_message("El nombre artístico es obligatorio")
                    return
                
                # Crear artista
                artist_data = {
                    "stage_name": stage_name,
                    "real_name": real_name if real_name else None,
                    "music_genre": music_genre if music_genre else None,
                    "country_of_origin": country if country else None,
                    "email": email if email else None,
                    "instagram_handle": instagram if instagram else None
                }
                
                result = self.create_item(artist_data)
                if result:
                    self.display_success_message(f"Artista '{stage_name}' creado exitosamente")
                else:
                    self.display_error_message("Error al crear el artista. Puede que ya exista un artista con ese nombre o email.")
    
    def render_update_view(self):
        """Renderiza la vista de actualización de artistas"""
        st.header("Actualizar Artista")
        
        # Obtener todos los artistas
        artists = self.get_all_items()
        
        if not artists:
            st.info("No hay artistas disponibles para actualizar")
            return
        
        # Seleccionar artista a actualizar
        artist_ids = [artist["id"] for artist in artists]
        artist_names = [artist["stage_name"] for artist in artists]
        artist_dict = dict(zip(artist_names, artist_ids))
        
        selected_artist_name = st.selectbox("Seleccionar artista a actualizar", artist_names)
        selected_artist_id = artist_dict[selected_artist_name]
        
        # Obtener datos actuales del artista
        current_artist = self.get_item_by_id(selected_artist_id)
        
        if not current_artist:
            st.error("No se pudo obtener la información del artista")
            return
        
        # Formulario para actualizar artista
        with st.form("update_artist_form"):
            stage_name = st.text_input("Nombre Artístico *", value=current_artist["stage_name"])
            real_name = st.text_input("Nombre Real", value=current_artist.get("real_name", ""))
            music_genre = st.text_input("Género Musical", value=current_artist.get("music_genre", ""))
            country = st.text_input("País de Origen", value=current_artist.get("country_of_origin", ""))
            email = st.text_input("Email", value=current_artist.get("email", ""))
            instagram = st.text_input("Instagram", value=current_artist.get("instagram_handle", ""))
            
            submit_button = st.form_submit_button("Actualizar Artista")
            
            if submit_button:
                if not stage_name:
                    self.display_error_message("El nombre artístico es obligatorio")
                    return
                
                # Actualizar artista
                artist_data = {
                    "stage_name": stage_name,
                    "real_name": real_name if real_name else None,
                    "music_genre": music_genre if music_genre else None,
                    "country_of_origin": country if country else None,
                    "email": email if email else None,
                    "instagram_handle": instagram if instagram else None
                }
                
                result = self.update_item(selected_artist_id, artist_data)
                if result:
                    self.display_success_message(f"Artista '{stage_name}' actualizado exitosamente")
                else:
                    self.display_error_message("Error al actualizar el artista")
    
    def render_delete_view(self):
        """Renderiza la vista de eliminación de artistas"""
        st.header("Eliminar Artista")
        
        # Obtener todos los artistas
        artists = self.get_all_items()
        
        if not artists:
            st.info("No hay artistas disponibles para eliminar")
            return
        
        # Seleccionar artista a eliminar
        artist_ids = [artist["id"] for artist in artists]
        artist_names = [artist["stage_name"] for artist in artists]
        artist_dict = dict(zip(artist_names, artist_ids))
        
        selected_artist_name = st.selectbox("Seleccionar artista a eliminar", artist_names)
        selected_artist_id = artist_dict[selected_artist_name]
        
        # Advertencia y confirmación
        st.warning(f"¿Estás seguro de que deseas eliminar al artista '{selected_artist_name}'? Esta acción eliminará también todos sus álbumes y canciones asociadas.")
        
        if st.button("Eliminar Artista"):
            result = self.delete_item(selected_artist_id)
            if result:
                self.display_success_message(f"Artista '{selected_artist_name}' eliminado exitosamente")
            else:
                self.display_error_message("Error al eliminar el artista")
    
    def get_all_items(self) -> List[Dict[str, Any]]:
        """Obtiene todos los artistas"""
        return self.api_client.get_all_artists()
    
    def get_item_by_id(self, item_id: int) -> Optional[Dict[str, Any]]:
        """Obtiene un artista por su ID"""
        return self.api_client.get_artist_by_id(item_id)
    
    def create_item(self, item_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Crea un nuevo artista"""
        return self.api_client.create_artist(item_data)
    
    def update_item(self, item_id: int, item_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Actualiza un artista existente"""
        return self.api_client.update_artist(item_id, item_data)
    
    def delete_item(self, item_id: int) -> Optional[Dict[str, Any]]:
        """Elimina un artista por su ID"""
        return self.api_client.delete_artist(item_id)
