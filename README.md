<img src="logo_buenaonda.jpg" alt="Logo Buena Onda Música" width="250"/>
# Buena Onda Música

**Sistema de Gestión para Disquera Independiente**  
Proyecto CRUD Full Stack: FastAPI + PostgreSQL (Backend) & Streamlit (Frontend)



## Tabla de Contenidos

- [Descripción General](#descripción-general)
- [Arquitectura del Proyecto](#arquitectura-del-proyecto)
- [Características Principales](#características-principales)
- [Requisitos](#requisitos)
- [Instalación y Ejecución](#instalación-y-ejecución)
  - [1. Backend (API REST)](#1-backend-api-rest)
  - [2. Frontend (Streamlit)](#2-frontend-streamlit)
- [Pruebas Unitarias](#pruebas-unitarias)
- [Documentación de la API](#documentación-de-la-api)
- [Estructura de Carpetas y Archivos](#estructura-de-carpetas-y-archivos)
- [Notas y Buenas Prácticas](#notas-y-buenas-prácticas)
- [Créditos](#créditos)

---

## Descripción General

**Buena Onda Música** es una aplicación web para la gestión de un catálogo musical de una disquera independiente. Permite administrar artistas, álbumes y canciones de manera sencilla, intuitiva y profesional.

- **Backend:** API RESTful desarrollada con FastAPI, SQLAlchemy y PostgreSQL.
- **Frontend:** Interfaz de usuario moderna y responsiva con Streamlit.
- **Pruebas:** Cobertura de pruebas unitarias con Pytest.

---

## Arquitectura del Proyecto

```
+-------------------+         HTTP (JSON)         +----------------------+
|    Frontend       | <-------------------------> |        Backend       |
|  (Streamlit)      |                             |   (FastAPI + DB)     |
+-------------------+                             +----------------------+
        |                                                   |
        | REST API (CRUD)                                   |
        |                                                   |
        +-------------------+-------------------------------+
                            |
                    +------------------+
                    |  PostgreSQL DB   |
                    +------------------+
```

---

## Características Principales

- **CRUD completo** para Artistas, Álbumes y Canciones.
- **Relaciones**: Un artista puede tener varios álbumes, un álbum varias canciones.
- **Interfaz amigable** y navegación intuitiva.
- **Estadísticas** del catálogo musical.
- **Pruebas unitarias** para asegurar la calidad del código.
- **Documentación automática** de la API (Swagger/OpenAPI).
- **Validaciones** y manejo de errores.

---

## Requisitos

- Python 3.8 o superior
- PostgreSQL (para el backend)
- (Opcional) Virtualenv para aislar dependencias

---

## Instalación y Ejecución

### 1. Backend (API REST)

#### a) Instala las dependencias

```bash
pip install -r requirements.txt
```

#### b) Configura la base de datos

- Asegúrate de tener PostgreSQL corriendo.
- Crea una base de datos llamada `buenaondamusica`.
- Modifica la cadena de conexión en `db.py` si es necesario:
  ```
  postgresql://<usuario>:<contraseña>@localhost:5432/buenaondamusica
  ```

#### c) Ejecuta el backend

```bash
uvicorn main:app --reload
```

- La API estará disponible en: [http://localhost:8000](http://localhost:8000)

---

### 2. Frontend (Streamlit)

#### a) Instala las dependencias

```bash
pip install -r requirements_frontend.txt
```

#### b) Ejecuta la aplicación

```bash
streamlit run main_frontend.py
```
o
```bash
streamlit run app_frontend.py
```

- Accede a la interfaz en: [http://localhost:8501](http://localhost:8501)
- Configura la URL de la API en la barra lateral si es necesario.

---

## Pruebas Unitarias

- Las pruebas unitarias están ubicadas en la carpeta `tests/`.
- Se utilizan `pytest` y `fastapi.testclient` para simular peticiones a la API.
- Para ejecutar las pruebas:

```bash
pytest
```

- Las pruebas cubren operaciones CRUD para Artistas, Álbumes y Canciones, y son tolerantes a duplicados y errores de validación.

---

## Documentación de la API

- **Swagger UI:** [http://localhost:8000/docs](http://localhost:8000/docs)
- **ReDoc:** [http://localhost:8000/redoc](http://localhost:8000/redoc)

Aquí puedes consultar y probar todos los endpoints de la API de forma interactiva.

---

## Estructura de Carpetas y Archivos

```
BuenaOnda/
│
├── main.py                # Punto de entrada del backend (FastAPI)
├── db.py                  # Configuración de la base de datos
├── models.py              # Modelos SQLAlchemy (tablas)
├── schemas.py             # Esquemas Pydantic (validación)
├── services.py            # Lógica de negocio y acceso a datos
│
├── main_frontend.py       # Punto de entrada del frontend (Streamlit)
├── app_frontend.py        # Alternativa modular para el frontend
├── api_st.py              # Cliente de la API para el frontend
├── artist_st.py           # Vista CRUD de Artistas (Streamlit)
├── album_st.py            # Vista CRUD de Álbumes (Streamlit)
├── song_st.py             # Vista CRUD de Canciones (Streamlit)
├── base_st.py             # Clase base para vistas CRUD (Streamlit)
├── ui_st.py               # Utilidades y estilos para Streamlit
├── connection_st.py       # Utilidades de conexión para el frontend
│
├── requirements.txt           # Dependencias del backend
├── requirements_frontend.txt  # Dependencias del frontend
│
├── tests/                 # Pruebas unitarias (pytest)
│   ├── test_artist.py
│   ├── test_album.py
│   └── test_song.py
│
└── README.md              # Este archivo
```

---

## Créditos

- Desarrollado por: Diego Islas
- Universidad: Universidad Autónoma de Nuevo León
- Materia: Programación Orientada a Objetos
- Profesor/a: Ángel Manuel Tapia Avitia

---

¡Gracias por revisar este proyecto!  


---


