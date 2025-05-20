import streamlit as st
from typing import Dict, List, Any, Optional
from base import CRUDView
from frontend.utils.api  import APIClient

class SongView(CRUDView):
    """
    Vista para gestionar canciones en Streamlit.
    Implementa operaciones CRUD para la entidad Song.
    """
    
    def __init__(self, api_client: APIClient):
        """
        Inicializa la vista de canciones.
        
        Args:
            api_client: Cliente API para interactuar con el backend
        """
        super().__init__("Gestión de Canciones")
        self.api_client = api_client
    
    def render_list_view(self):
        """Renderiza la vista de listado de canciones"""
        st.header("Lista de Canciones")
        
        # Obtener todas las canciones
        songs = self.get_all_items()
        
        # Obtener todos los álbumes para mostrar nombres en lugar de IDs
        albums = self.api_client.get_all_albums()
        album_dict = {album["id"]: album["title"] for album in albums}
        
        # Añadir nombre de álbum a cada canción y formatear duración
        for song in songs:
            song["album_title"] = album_dict.get(song["album_id"], f"Álbum ID: {song['album_id']}")
            minutes = song["duration"] // 60
            seconds = song["duration"] % 60
            song["duration_formatted"] = f"{minutes}:{seconds:02d}"
        
        # Mostrar tabla de canciones
        if songs:
            self.display_data_table(
                songs, 
                ["id", "title", "duration_formatted", "album_title"]
            )
        else:
            st.info("No hay canciones registradas")
    
    def render_create_view(self):
        """Renderiza la vista de creación de canciones"""
        st.header("Crear Nueva Canción")
        
        # Obtener álbumes para el selector
        albums = self.api_client.get_all_albums()
        
        if not albums:
            st.warning("No hay álbumes disponibles. Debes crear al menos un álbum antes de crear una canción.")
            return
        
        # Formulario para crear canción
        with st.form("create_song_form"):
            title = st.text_input("Título de la Canción *", help="Campo obligatorio")
            
            # Entrada para duración
            col1, col2 = st.columns(2)
            with col1:
                minutes = st.number_input("Minutos", min_value=0, max_value=59, value=0)
            with col2:
                seconds = st.number_input("Segundos", min_value=0, max_value=59, value=0)
            
            # Calcular duración total en segundos
            duration = minutes * 60 + seconds
            
            # Selector de álbum
            album_ids = [album["id"] for album in albums]
            album_titles = [album["title"] for album in albums]
            album_dict = dict(zip(album_titles, album_ids))
            
            selected_album = st.selectbox("Álbum *", album_titles)
            
            submit_button = st.form_submit_button("Crear Canción")
            
            if submit_button:
                if not title:
                    self.display_error_message("El título de la canción es obligatorio")
                    return
                
                if duration == 0:
                    self.display_error_message("La duración de la canción debe ser mayor a 0")
                    return
                
                # Crear canción
                song_data = {
                    "title": title,
                    "duration": duration,
                    "album_id": album_dict[selected_album]
                }
                
                result = self.create_item(song_data)
                if result:
                    self.display_success_message(f"Canción '{title}' creada exitosamente")
                else:
                    self.display_error_message("Error al crear la canción. Puede que ya exista una canción con ese título.")
    
    def render_update_view(self):
        """Renderiza la vista de actualización de canciones"""
        st.header("Actualizar Canción")
        
        # Obtener todas las canciones
        songs = self.get_all_items()
        
        if not songs:
            st.info("No hay canciones disponibles para actualizar")
            return
        
        # Obtener álbumes para el selector
        albums = self.api_client.get_all_albums()
        
        if not albums:
            st.warning("No hay álbumes disponibles.")
            return
        
        # Seleccionar canción a actualizar
        song_ids = [song["id"] for song in songs]
        song_titles = [song["title"] for song in songs]
        song_dict = dict(zip(song_titles, song_ids))
        
        selected_song_title = st.selectbox("Seleccionar canción a actualizar", song_titles)
        selected_song_id = song_dict[selected_song_title]
        
        # Obtener datos actuales de la canción
        current_song = self.get_item_by_id(selected_song_id)
        
        if not current_song:
            st.error("No se pudo obtener la información de la canción")
            return
        
        # Formulario para actualizar canción
        with st.form("update_song_form"):
            title = st.text_input("Título de la Canción *", value=current_song["title"])
            
            # Entrada para duración
            current_minutes = current_song["duration"] // 60
            current_seconds = current_song["duration"] % 60
            
            col1, col2 = st.columns(2)
            with col1:
                minutes = st.number_input("Minutos", min_value=0, max_value=59, value=current_minutes)
            with col2:
                seconds = st.number_input("Segundos", min_value=0, max_value=59, value=current_seconds)
            
            # Calcular duración total en segundos
            duration = minutes * 60 + seconds
            
            # Selector de álbum
            album_ids = [album["id"] for album in albums]
            album_titles = [album["title"] for album in albums]
            album_dict = dict(zip(album_ids, album_titles))
            
            # Encontrar el índice del álbum actual
            current_album_title = album_dict.get(current_song["album_id"], album_titles[0])
            album_index = album_titles.index(current_album_title) if current_album_title in album_titles else 0
            
            selected_album = st.selectbox("Álbum *", album_titles, index=album_index)
            selected_album_id = [k for k, v in album_dict.items() if v == selected_album][0]
            
            submit_button = st.form_submit_button("Actualizar Canción")
            
            if submit_button:
                if not title:
                    self.display_error_message("El título de la canción es obligatorio")
                    return
                
                if duration == 0:
                    self.display_error_message("La duración de la canción debe ser mayor a 0")
                    return
                
                # Actualizar canción
                song_data = {
                    "title": title,
                    "duration": duration,
                    "album_id": selected_album_id
                }
                
                result = self.update_item(selected_song_id, song_data)
                if result:
                    self.display_success_message(f"Canción '{title}' actualizada exitosamente")
                else:
                    self.display_error_message("Error al actualizar la canción")
    
    def render_delete_view(self):
        """Renderiza la vista de eliminación de canciones"""
        st.header("Eliminar Canción")
        
        # Obtener todas las canciones
        songs = self.get_all_items()
        
        if not songs:
            st.info("No hay canciones disponibles para eliminar")
            return
        
        # Seleccionar canción a eliminar
        song_ids = [song["id"] for song in songs]
        song_titles = [song["title"] for song in songs]
        song_dict = dict(zip(song_titles, song_ids))
        
        selected_song_title = st.selectbox("Seleccionar canción a eliminar", song_titles)
        selected_song_id = song_dict[selected_song_title]
        
        # Advertencia y confirmación
        st.warning(f"¿Estás seguro de que deseas eliminar la canción '{selected_song_title}'?")
        
        if st.button("Eliminar Canción"):
            result = self.delete_item(selected_song_id)
            if result:
                self.display_success_message(f"Canción '{selected_song_title}' eliminada exitosamente")
            else:
                self.display_error_message("Error al eliminar la canción")
    
    def get_all_items(self) -> List[Dict[str, Any]]:
        """Obtiene todas las canciones"""
        return self.api_client.get_all_songs()
    
    def get_item_by_id(self, item_id: int) -> Optional[Dict[str, Any]]:
        """Obtiene una canción por su ID"""
        return self.api_client.get_song_by_id(item_id)
    
    def create_item(self, item_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Crea una nueva canción"""
        return self.api_client.create_song(item_data)
    
    def update_item(self, item_id: int, item_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Actualiza una canción existente"""
        return self.api_client.update_song(item_id, item_data)
    
    def delete_item(self, item_id: int) -> Optional[Dict[str, Any]]:
        """Elimina una canción por su ID"""
        return self.api_client.delete_song(item_id)
