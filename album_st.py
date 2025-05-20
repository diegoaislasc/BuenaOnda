import streamlit as st
from typing import Dict, List, Any, Optional
from base import CRUDView
from frontend.utils.api import APIClient
from datetime import date


class AlbumView(CRUDView):
    """
    Vista para gestionar álbumes en Streamlit.
    Implementa operaciones CRUD para la entidad Album.
    """
    
    def __init__(self, api_client: APIClient):
        """
        Inicializa la vista de álbumes.
        
        Args:
            api_client: Cliente API para interactuar con el backend
        """
        super().__init__("Gestión de Álbumes")
        self.api_client = api_client
    
    def render_list_view(self):
        """Renderiza la vista de listado de álbumes"""
        st.header("Lista de Álbumes")
        
        # Obtener todos los álbumes
        albums = self.get_all_items()
        
        # Obtener todos los artistas para mostrar nombres en lugar de IDs
        artists = self.api_client.get_all_artists()
        artist_dict = {artist["id"]: artist["stage_name"] for artist in artists}
        
        # Añadir nombre de artista a cada álbum
        for album in albums:
            album["artist_name"] = artist_dict.get(album["artist_id"], f"Artista ID: {album['artist_id']}")
        
        # Mostrar tabla de álbumes
        if albums:
            self.display_data_table(
                albums, 
                ["id", "title", "release_date", "artist_name"]
            )
            
            # Opción para ver canciones de un álbum
            st.subheader("Ver canciones por álbum")
            album_ids = [album["id"] for album in albums]
            album_titles = [album["title"] for album in albums]
            album_dict = dict(zip(album_titles, album_ids))
            
            selected_album = st.selectbox("Seleccionar álbum", album_titles)
            if selected_album:
                self.show_album_songs(album_dict[selected_album])
        else:
            st.info("No hay álbumes registrados")
    
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
        """Renderiza la vista de creación de álbumes"""
        st.header("Crear Nuevo Álbum")
        
        # Obtener artistas para el selector
        artists = self.api_client.get_all_artists()
        
        if not artists:
            st.warning("No hay artistas disponibles. Debes crear al menos un artista antes de crear un álbum.")
            return
        
        # Formulario para crear álbum
        with st.form("create_album_form"):
            title = st.text_input("Título del Álbum *", help="Campo obligatorio")
            
            # Selector de artista
            artist_ids = [artist["id"] for artist in artists]
            artist_names = [artist["stage_name"] for artist in artists]
            artist_dict = dict(zip(artist_names, artist_ids))
            
            selected_artist = st.selectbox("Artista *", artist_names)
            
            # Selector de fecha
            release_date = st.date_input("Fecha de Lanzamiento", value=None)
            
            submit_button = st.form_submit_button("Crear Álbum")
            
            if submit_button:
                if not title:
                    self.display_error_message("El título del álbum es obligatorio")
                    return
                
                # Crear álbum
                album_data = {
                    "title": title,
                    "artist_id": artist_dict[selected_artist],
                    "release_date": release_date.isoformat() if release_date else None
                }
                
                result = self.create_item(album_data)
                if result:
                    self.display_success_message(f"Álbum '{title}' creado exitosamente")
                else:
                    self.display_error_message("Error al crear el álbum. Puede que ya exista un álbum con ese título.")
    
    def render_update_view(self):
        """Renderiza la vista de actualización de álbumes"""
        st.header("Actualizar Álbum")
        
        # Obtener todos los álbumes
        albums = self.get_all_items()
        
        if not albums:
            st.info("No hay álbumes disponibles para actualizar")
            return
        
        # Obtener artistas para el selector
        artists = self.api_client.get_all_artists()
        
        if not artists:
            st.warning("No hay artistas disponibles.")
            return
        
        # Seleccionar álbum a actualizar
        album_ids = [album["id"] for album in albums]
        album_titles = [album["title"] for album in albums]
        album_dict = dict(zip(album_titles, album_ids))
        
        selected_album_title = st.selectbox("Seleccionar álbum a actualizar", album_titles)
        selected_album_id = album_dict[selected_album_title]
        
        # Obtener datos actuales del álbum
        current_album = self.get_item_by_id(selected_album_id)
        
        if not current_album:
            st.error("No se pudo obtener la información del álbum")
            return
        
        # Formulario para actualizar álbum
        with st.form("update_album_form"):
            title = st.text_input("Título del Álbum *", value=current_album["title"])
            
            # Selector de artista
            artist_ids = [artist["id"] for artist in artists]
            artist_names = [artist["stage_name"] for artist in artists]
            artist_dict = dict(zip(artist_ids, artist_names))
            
            # Encontrar el índice del artista actual
            current_artist_name = artist_dict.get(current_album["artist_id"], artist_names[0])
            artist_index = artist_names.index(current_artist_name) if current_artist_name in artist_names else 0
            
            selected_artist = st.selectbox("Artista *", artist_names, index=artist_index)
            selected_artist_id = [k for k, v in artist_dict.items() if v == selected_artist][0]
            
            # Selector de fecha
            release_date_value = None
            if current_album.get("release_date"):
                try:
                    release_date_value = date.fromisoformat(current_album["release_date"])
                except (ValueError, TypeError):
                    pass
            
            release_date = st.date_input("Fecha de Lanzamiento", value=release_date_value)
            
            submit_button = st.form_submit_button("Actualizar Álbum")
            
            if submit_button:
                if not title:
                    self.display_error_message("El título del álbum es obligatorio")
                    return
                
                # Actualizar álbum
                album_data = {
                    "title": title,
                    "artist_id": selected_artist_id,
                    "release_date": release_date.isoformat() if release_date else None
                }
                
                result = self.update_item(selected_album_id, album_data)
                if result:
                    self.display_success_message(f"Álbum '{title}' actualizado exitosamente")
                else:
                    self.display_error_message("Error al actualizar el álbum")
    
    def render_delete_view(self):
        """Renderiza la vista de eliminación de álbumes"""
        st.header("Eliminar Álbum")
        
        # Obtener todos los álbumes
        albums = self.get_all_items()
        
        if not albums:
            st.info("No hay álbumes disponibles para eliminar")
            return
        
        # Seleccionar álbum a eliminar
        album_ids = [album["id"] for album in albums]
        album_titles = [album["title"] for album in albums]
        album_dict = dict(zip(album_titles, album_ids))
        
        selected_album_title = st.selectbox("Seleccionar álbum a eliminar", album_titles)
        selected_album_id = album_dict[selected_album_title]
        
        # Advertencia y confirmación
        st.warning(f"¿Estás seguro de que deseas eliminar el álbum '{selected_album_title}'? Esta acción eliminará también todas las canciones asociadas.")
        
        if st.button("Eliminar Álbum"):
            result = self.delete_item(selected_album_id)
            if result:
                self.display_success_message(f"Álbum '{selected_album_title}' eliminado exitosamente")
            else:
                self.display_error_message("Error al eliminar el álbum")
    
    def get_all_items(self) -> List[Dict[str, Any]]:
        """Obtiene todos los álbumes"""
        return self.api_client.get_all_albums()
    
    def get_item_by_id(self, item_id: int) -> Optional[Dict[str, Any]]:
        """Obtiene un álbum por su ID"""
        return self.api_client.get_album_by_id(item_id)
    
    def create_item(self, item_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Crea un nuevo álbum"""
        return self.api_client.create_album(item_data)
    
    def update_item(self, item_id: int, item_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Actualiza un álbum existente"""
        return self.api_client.update_album(item_id, item_data)
    
    def delete_item(self, item_id: int) -> Optional[Dict[str, Any]]:
        """Elimina un álbum por su ID"""
        return self.api_client.delete_album(item_id)
