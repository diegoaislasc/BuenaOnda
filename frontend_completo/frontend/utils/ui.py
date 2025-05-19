import streamlit as st
import os

def custom_css():
    """
    Aplica estilos CSS personalizados a la aplicación Streamlit.
    """
    st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        color: #1E3A8A;
        margin-bottom: 1rem;
    }
    
    .section-header {
        font-size: 1.8rem;
        color: #2563EB;
        margin-top: 1.5rem;
        margin-bottom: 1rem;
    }
    
    .info-box {
        background-color: #EFF6FF;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #3B82F6;
        margin-bottom: 1rem;
    }
    
    .success-box {
        background-color: #ECFDF5;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #10B981;
        margin-bottom: 1rem;
    }
    
    .warning-box {
        background-color: #FFFBEB;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #F59E0B;
        margin-bottom: 1rem;
    }
    
    .error-box {
        background-color: #FEF2F2;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #EF4444;
        margin-bottom: 1rem;
    }
    
    .stButton>button {
        background-color: #2563EB;
        color: white;
        border-radius: 0.25rem;
        padding: 0.5rem 1rem;
        font-weight: 500;
    }
    
    .stButton>button:hover {
        background-color: #1D4ED8;
    }
    
    .sidebar .sidebar-content {
        background-color: #F3F4F6;
    }
    
    .dataframe {
        font-size: 0.9rem;
    }
    
    /* Estilos para formularios */
    .stForm {
        background-color: #F9FAFB;
        padding: 1rem;
        border-radius: 0.5rem;
        border: 1px solid #E5E7EB;
    }
    
    /* Estilos para tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 1rem;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 3rem;
        white-space: pre-wrap;
        background-color: #F3F4F6;
        border-radius: 0.5rem 0.5rem 0 0;
        padding: 0.5rem 1rem;
        font-weight: 500;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: #2563EB;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)

def get_logo():
    """
    Devuelve el HTML para mostrar el logo de Buena Onda Música.
    """
    return """
    <div style="display: flex; align-items: center; margin-bottom: 1rem;">
        <div style="font-size: 2.5rem; margin-right: 0.5rem;">🎵</div>
        <div>
            <div style="font-size: 1.5rem; font-weight: bold; color: #1E3A8A;">Buena Onda Música</div>
            <div style="font-size: 0.9rem; color: #6B7280;">Disquera Independiente</div>
        </div>
    </div>
    """

def format_duration(seconds):
    """
    Formatea una duración en segundos a formato minutos:segundos.
    
    Args:
        seconds: Duración en segundos
        
    Returns:
        str: Duración formateada como "mm:ss"
    """
    minutes = seconds // 60
    remaining_seconds = seconds % 60
    return f"{minutes}:{remaining_seconds:02d}"
