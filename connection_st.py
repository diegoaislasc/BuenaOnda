import streamlit as st
import requests
import time

def test_api_connection(api_url):
    """
    Prueba la conexión con la API REST.
    
    Args:
        api_url: URL base de la API
        
    Returns:
        bool: True si la conexión es exitosa, False en caso contrario
    """
    try:
        response = requests.get(f"{api_url}/artist/")
        response.raise_for_status()
        return True
    except Exception:
        return False

def wait_for_api(api_url, max_attempts=5, delay=2):
    """
    Espera a que la API esté disponible, con reintentos.
    
    Args:
        api_url: URL base de la API
        max_attempts: Número máximo de intentos
        delay: Tiempo de espera entre intentos en segundos
        
    Returns:
        bool: True si la API está disponible, False en caso contrario
    """
    for attempt in range(max_attempts):
        if test_api_connection(api_url):
            return True
        
        if attempt < max_attempts - 1:
            time.sleep(delay)
    
    return False

def display_connection_status(api_url):
    """
    Muestra el estado de conexión con la API.
    
    Args:
        api_url: URL base de la API
    """
    with st.sidebar:
        if test_api_connection(api_url):
            st.success("✅ Conectado a la API")
        else:
            st.error("❌ No se pudo conectar a la API")
            st.warning(f"Asegúrate de que el backend esté en ejecución en {api_url}")
            st.info("Revisa las instrucciones de despliegue para más información")
