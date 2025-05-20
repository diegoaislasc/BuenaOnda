import streamlit as st
from api_st import APIClient
from artist_st import ArtistView
from album_st import AlbumView
from song_st import SongView

class App:
    """
    Aplicación principal de Buena Onda Música en Streamlit.
    Gestiona la navegación entre las diferentes vistas y la inicialización de componentes.
    """
    
    def __init__(self, api_url: str = "http://localhost:8000"):
        """
        Inicializa la aplicación con la URL de la API.
        
        Args:
            api_url: URL base de la API REST
        """
        self.api_client = APIClient(api_url)
        
        # Inicializar componentes
        self.artist_view = ArtistView(self.api_client)
        self.album_view = AlbumView(self.api_client)
        self.song_view = SongView(self.api_client)
        
        # Configurar página
        st.set_page_config(
            page_title="Buena Onda Música",
            page_icon="🎵",
            layout="wide",
            initial_sidebar_state="expanded"
        )
    
    def run(self):
        """Ejecuta la aplicación principal"""
        self._render_sidebar()
        self._render_main_content()
    
    def _render_sidebar(self):
        """Renderiza la barra lateral con navegación y logo"""
        with st.sidebar:
            st.title("🎵 Buena Onda Música")
            st.markdown("---")
            
            # Opciones de navegación
            st.subheader("Navegación")
            page = st.radio(
                "Selecciona una sección:",
                ["Inicio", "Artistas", "Álbumes", "Canciones"]
            )
            
            # Guardar selección en estado de sesión
            st.session_state.page = page
            
            st.markdown("---")
            st.info("Desarrollado con Streamlit y FastAPI")
    
    def _render_main_content(self):
        """Renderiza el contenido principal según la página seleccionada"""
        page = st.session_state.get("page", "Inicio")
        
        if page == "Inicio":
            self._render_home()
        elif page == "Artistas":
            self.artist_view.render()
        elif page == "Álbumes":
            self.album_view.render()
        elif page == "Canciones":
            self.song_view.render()
    
    def _render_home(self):
        """Renderiza la página de inicio"""
        st.title("Bienvenido a Buena Onda Música")
        
        st.markdown("""
        ### Sistema de Gestión para Disquera Independiente
        
        Esta aplicación te permite gestionar el catálogo musical de la disquera, incluyendo:
        
        - **Artistas**: Gestiona la información de los artistas de la disquera
        - **Álbumes**: Administra los álbumes publicados por cada artista
        - **Canciones**: Cataloga las canciones incluidas en cada álbum
        
        Utiliza el menú de navegación en la barra lateral para acceder a las diferentes secciones.
        """)
        
        # Mostrar estadísticas
        st.subheader("Estadísticas del Catálogo")
        
        try:
            col1, col2, col3 = st.columns(3)
            
            with col1:
                artists = self.api_client.get_all_artists()
                st.metric("Artistas", len(artists))
            
            with col2:
                albums = self.api_client.get_all_albums()
                st.metric("Álbumes", len(albums))
            
            with col3:
                songs = self.api_client.get_all_songs()
                st.metric("Canciones", len(songs))
        
        except Exception as e:
            st.error(f"Error al cargar estadísticas: {str(e)}")
            st.warning("Asegúrate de que el backend esté en ejecución en http://localhost:8000")

# Punto de entrada de la aplicación
if __name__ == "__main__":
    app = App()
    app.run()
