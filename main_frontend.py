# streamlit run main_frontend.py

import streamlit as st
from api_st import APIClient
from artist_st import ArtistView
from album_st import AlbumView
from song_st import SongView


def main():
    """Función principal para ejecutar la aplicación Streamlit"""

    # Configurar página
    st.set_page_config(
        page_title="Buena Onda Música",
        page_icon="🎵",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Inicializar la aplicación
    api_url = st.sidebar.text_input(
        "URL de la API",
        value="http://localhost:8000",
        help="URL base de la API REST"
    )
    
    # Verificar conexión con la API
    api_client = APIClient(api_url)
    
    try:
        # Intentar obtener artistas para verificar conexión
        api_client.get_all_artists()
        st.sidebar.success("Conectado a la API")
    except Exception as e:
        st.sidebar.error(f"Error de conexión: {str(e)}")
        st.sidebar.warning("Asegúrate de que el backend esté en ejecución")

    
    # Renderizar sidebar
    with st.sidebar:
        st.title("🎵 Buena Onda Música")
        st.markdown("---")
        
        # Opciones de navegación
        st.subheader("Navegación")
        page = st.radio(
            "Selecciona una sección:",
            ["Inicio", "Artistas", "Álbumes", "Canciones"]
        )
        
        st.markdown("---")
        st.info("Desarrollado con Streamlit y FastAPI")
    
    # Renderizar contenido principal
    if page == "Inicio":
        render_home(api_client)
    elif page == "Artistas":
        artist_view = ArtistView(api_client)
        artist_view.render()
    elif page == "Álbumes":
        album_view = AlbumView(api_client)
        album_view.render()
    elif page == "Canciones":
        song_view = SongView(api_client)
        song_view.render()

def render_home(api_client):
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
            artists = api_client.get_all_artists()
            st.metric("Artistas", len(artists))
        
        with col2:
            albums = api_client.get_all_albums()
            st.metric("Álbumes", len(albums))
        
        with col3:
            songs = api_client.get_all_songs()
            st.metric("Canciones", len(songs))
    
    except Exception as e:
        st.error(f"Error al cargar estadísticas: {str(e)}")
        st.warning("Asegúrate de que el backend esté en ejecución")

if __name__ == "__main__":
    main()
