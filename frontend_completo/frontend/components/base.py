import streamlit as st
from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional, Callable, TypeVar, Generic

T = TypeVar('T')

class CRUDView(Generic[T], ABC):
    """
    Clase base abstracta para vistas CRUD en Streamlit.
    Define la estructura común y métodos que deben implementar todas las vistas CRUD.
    """
    
    def __init__(self, title: str):
        """
        Inicializa la vista CRUD con un título.
        
        Args:
            title: Título de la vista
        """
        self.title = title
    
    def render(self):
        """Renderiza la vista completa"""
        st.title(self.title)
        
        # Tabs para las diferentes operaciones CRUD
        tab_list, tab_create, tab_update, tab_delete = st.tabs(["Listar", "Crear", "Actualizar", "Eliminar"])
        
        with tab_list:
            self.render_list_view()
            
        with tab_create:
            self.render_create_view()
            
        with tab_update:
            self.render_update_view()
            
        with tab_delete:
            self.render_delete_view()
    
    @abstractmethod
    def render_list_view(self):
        """Renderiza la vista de listado"""
        pass
    
    @abstractmethod
    def render_create_view(self):
        """Renderiza la vista de creación"""
        pass
    
    @abstractmethod
    def render_update_view(self):
        """Renderiza la vista de actualización"""
        pass
    
    @abstractmethod
    def render_delete_view(self):
        """Renderiza la vista de eliminación"""
        pass
    
    @abstractmethod
    def get_all_items(self) -> List[Dict[str, Any]]:
        """Obtiene todos los elementos"""
        pass
    
    @abstractmethod
    def get_item_by_id(self, item_id: int) -> Optional[Dict[str, Any]]:
        """Obtiene un elemento por su ID"""
        pass
    
    @abstractmethod
    def create_item(self, item_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Crea un nuevo elemento"""
        pass
    
    @abstractmethod
    def update_item(self, item_id: int, item_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Actualiza un elemento existente"""
        pass
    
    @abstractmethod
    def delete_item(self, item_id: int) -> Optional[Dict[str, Any]]:
        """Elimina un elemento por su ID"""
        pass
    
    def display_success_message(self, message: str):
        """Muestra un mensaje de éxito"""
        st.success(message)
    
    def display_error_message(self, message: str):
        """Muestra un mensaje de error"""
        st.error(message)
    
    def display_info_message(self, message: str):
        """Muestra un mensaje informativo"""
        st.info(message)
    
    def display_data_table(self, data: List[Dict[str, Any]], columns: List[str]):
        """
        Muestra una tabla de datos.
        
        Args:
            data: Lista de diccionarios con los datos
            columns: Lista de columnas a mostrar
        """
        if not data:
            st.info("No hay datos disponibles")
            return
        
        # Crear un DataFrame para mostrar los datos
        import pandas as pd
        df = pd.DataFrame(data)
        
        # Mostrar solo las columnas especificadas
        if columns and all(col in df.columns for col in columns):
            df = df[columns]
        
        st.dataframe(df)
