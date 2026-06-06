import os                              # Para acceder a variables de entorno del sistema operativo
from pathlib import Path               # para rutas de carpetas y archivos     

import mysql.connector
import pandas as pd
import plotly.express as px                 # Librería para crear gráficos interactivos
import streamlit as st                     # crear aplicaciones web de análisis de datos integrando Python, SQL,
from dotenv import load_dotenv               # permite leer el archivo .env donde guardamos credenciales


# CONFIGURACIÓN DE PÁGINA

st.set_page_config(
    page_title="MusicStream Divas",
    page_icon="🎤",
    layout="wide"
)


# VARIABLES DE ENTORNO

env_path = Path(__file__).parent / ".env"
load_dotenv(env_path)

password_sql = os.getenv("PASSW_SQL")


# FUNCIONES

def conectar_mysql():
    try:
        connection = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password=password_sql,
            database="musicstream"
        )
        return connection

    except Exception as e:
        st.error(f"Error de conexión: {e}")
        return None


def ejecutar_consulta(query):                 # Ejecuta cualquier consulta SQL y devuelve un DataFrame
    connection = conectar_mysql()

    if connection is None:
        return pd.DataFrame()

    try:
        df = pd.read_sql(query, connection)
        return df

    except Exception as e:
        st.error(f"Error en la consulta SQL: {e}")
        return pd.DataFrame()

    finally:
        connection.close()


def titulo_con_imagen(imagen, titulo, espacio=True):
    if espacio:
        st.markdown("<br><br>", unsafe_allow_html=True)

    col_img, col_text = st.columns([1, 6])

    with col_img:
        st.image(imagen, width=180)

    with col_text:
        st.markdown(
            f"<h3 style='padding-top:55px;'>{titulo}</h3>",
            unsafe_allow_html=True
        )


# PORTADA

st.image("Divas.png", use_container_width=True)                       # Muestra la imagen principal del dashboard

st.title("🎤 MusicStream: mujeres artistas por décadas")              # Título principal de la aplicación
st.markdown("Análisis de artistas femeninas cruzando datos de Deezer y Last.fm.")    # Texto descriptivo


# CONSULTAS SQL

query_albumes_decada = """                                    # Consulta que calcula el número de álbumes por década
SELECT 
    FLOOR(anio_lanzamiento / 10) * 10 AS decada,
    COUNT(DISTINCT titulo_album) AS total_albumes
FROM artistas
WHERE anio_lanzamiento IS NOT NULL
GROUP BY decada
ORDER BY decada;
"""

query_colaboraciones = """
SELECT 
    nombre_artista,
    COUNT(*) AS total_colaboraciones
FROM artistas
WHERE tipo = 'colaboracion'
GROUP BY nombre_artista
ORDER BY total_colaboraciones DESC;
"""

query_generos_artista = """
SELECT 
    nombre_artista,
    COUNT(DISTINCT genero) AS total_generos
FROM artistas
WHERE genero IS NOT NULL
GROUP BY nombre_artista
ORDER BY total_generos DESC;
"""

query_genero_decada = """
SELECT
    decada,
    genero,
    total_canciones
FROM (
    SELECT 
        FLOOR(anio_lanzamiento / 10) * 10 AS decada,
        genero,
        COUNT(*) AS total_canciones,
        ROW_NUMBER() OVER (
            PARTITION BY FLOOR(anio_lanzamiento / 10) * 10
            ORDER BY COUNT(*) DESC
        ) AS ranking
    FROM artistas
    WHERE anio_lanzamiento IS NOT NULL
      AND genero IS NOT NULL
    GROUP BY decada, genero
) AS tabla_ranking
WHERE ranking = 1
ORDER BY decada;
"""

query_fidelidad = """
SELECT 
    a.nombre_artista,
    MAX(l.listeners) AS listeners,
    MAX(l.playcount) AS playcount,
    ROUND(MAX(l.playcount) / MAX(l.listeners), 2) AS reproducciones_por_oyente
FROM artistas AS a
INNER JOIN lastfm_artistas AS l
    ON a.nombre_artista = l.nombre_artista
WHERE l.listeners IS NOT NULL
  AND l.listeners > 0
GROUP BY a.nombre_artista
ORDER BY reproducciones_por_oyente DESC;
"""

query_playcount_decada = """
SELECT
    FLOOR(a.anio_lanzamiento / 10) * 10 AS decada,
    ROUND(AVG(l.playcount), 0) AS promedio_playcount,
    MAX(l.playcount) AS mayor_playcount,
    COUNT(DISTINCT a.nombre_artista) AS total_artistas
FROM artistas AS a
INNER JOIN lastfm_artistas AS l
    ON a.nombre_artista = l.nombre_artista
WHERE l.playcount IS NOT NULL
  AND a.anio_lanzamiento IS NOT NULL
GROUP BY decada
ORDER BY decada;
"""

query_preview = """
SELECT
    nombre_artista,
    titulo_cancion,
    titulo_album,
    preview,
    link_deezer
FROM artistas
WHERE preview IS NOT NULL
ORDER BY nombre_artista, titulo_cancion;
"""


# CARGA DE DATOS

df_albumes_decada = ejecutar_consulta(query_albumes_decada)
df_colaboraciones = ejecutar_consulta(query_colaboraciones)
df_generos_artista = ejecutar_consulta(query_generos_artista)
df_genero_decada = ejecutar_consulta(query_genero_decada)
df_fidelidad = ejecutar_consulta(query_fidelidad)
df_playcount_decada = ejecutar_consulta(query_playcount_decada)
df_preview = ejecutar_consulta(query_preview)


# MÉTRICAS PRINCIPALES

titulo_con_imagen("resumen.png", "Resumen general", espacio=False)    # Crea un encabezado reutilizable con imagen y texto

col1, col2, col3 = st.columns(3)                                     # Divide la pantalla en tres columnas

with col1:
    st.metric(
        "Décadas analizadas",
        df_albumes_decada["decada"].nunique()
        if "decada" in df_albumes_decada.columns else 0
    )

with col2:
    st.metric(
        "Artistas con colaboraciones",
        df_colaboraciones["nombre_artista"].nunique()
        if "nombre_artista" in df_colaboraciones.columns else 0
    )

with col3:
    st.metric(                                                        # Muestra un indicador numérico destacado
        "Artistas con previews",
        df_preview["nombre_artista"].nunique()
        if "nombre_artista" in df_preview.columns else 0
    )


# ÁLBUMES POR DÉCADA

titulo_con_imagen("albumes.png", "Álbumes por década")

if not df_albumes_decada.empty:
    fig_albumes_decada = px.bar(                                    # Crea un gráfico de barras interactivo
        df_albumes_decada,
        x="decada",
        y="total_albumes",
        text="total_albumes",
        title="Álbumes por década"
    )

    st.plotly_chart(fig_albumes_decada, use_container_width=True)


# COLABORACIONES POR ARTISTA

titulo_con_imagen(
    "colaboracion.png",
    "Canciones en colaboración por artista"
)

if not df_colaboraciones.empty:                                  # Verifica que la consulta haya devuelto datos
    fig_colaboraciones = px.bar(
        df_colaboraciones.head(15),
        x="total_colaboraciones",
        y="nombre_artista",
        orientation="h",
        text="total_colaboraciones",
        title="Top artistas por colaboraciones"
    )

    fig_colaboraciones.update_layout(
        yaxis={"categoryorder": "total ascending"}
    )

    st.plotly_chart(fig_colaboraciones, use_container_width=True)


# GÉNEROS DISTINTOS POR ARTISTA

titulo_con_imagen(
    "generos_distintos.png",
    "Géneros distintos por artista"
)

if not df_generos_artista.empty:
    fig_generos_artista = px.bar(
        df_generos_artista.head(15),
        x="total_generos",
        y="nombre_artista",
        orientation="h",
        text="total_generos",
        title="Artistas con más variedad de géneros"
    )

    fig_generos_artista.update_layout(
        yaxis={"categoryorder": "total ascending"}
    )

    st.plotly_chart(fig_generos_artista, use_container_width=True)


# GÉNERO DOMINANTE POR DÉCADA

titulo_con_imagen(
    "genero_dominante.png",
    "Género dominante por década")

if not df_genero_decada.empty:
    st.dataframe(df_genero_decada, use_container_width=True)

    fig_genero_decada = px.bar(
        df_genero_decada,
        x="decada",
        y="total_canciones",
        color="genero",
        text="genero",
        title="Género dominante por década"
    )

    st.plotly_chart(fig_genero_decada, use_container_width=True)


# AUDIENCIA MÁS FIEL

titulo_con_imagen(
    "audiencia.png",
    "Audiencia más fiel: playcount por listener"
)

if not df_fidelidad.empty:
    fig_fidelidad = px.bar(
        df_fidelidad.head(15),
        x="reproducciones_por_oyente",
        y="nombre_artista",
        orientation="h",
        text="reproducciones_por_oyente",
        title="Reproducciones por oyente"
    )

    fig_fidelidad.update_layout(
        yaxis={"categoryorder": "total ascending"}
    )

    st.plotly_chart(fig_fidelidad, use_container_width=True)


# PLAYCOUNT MEDIO POR DÉCADA

titulo_con_imagen(
    "playcounts.png",
    "Playcount medio por década"
)

if not df_playcount_decada.empty:
    fig_playcount = px.line(
        df_playcount_decada,
        x="decada",
        y="promedio_playcount",
        markers=True,
        title="Promedio de playcount por década"
    )

    st.plotly_chart(fig_playcount, use_container_width=True)


# PREVIEW DE DEEZER

titulo_con_imagen(
    "preview.png",
    "Escucha una preview"
)

if df_preview.empty:
    st.warning("No hay previews disponibles en la base de datos.")

else:
    artista = st.selectbox(                                           # Crea una lista desplegable para elegir una artista
        "Selecciona una artista",
        sorted(df_preview["nombre_artista"].unique())
    )

    df_artista = df_preview[
        df_preview["nombre_artista"] == artista
    ]

    cancion = st.selectbox(
        "Selecciona una canción",
        sorted(df_artista["titulo_cancion"].unique())
    )

    fila_cancion = df_artista[
        df_artista["titulo_cancion"] == cancion
    ].iloc[0]

    st.write(f"**Álbum:** {fila_cancion['titulo_album']}")

    preview_url = fila_cancion["preview"]
    link_deezer = fila_cancion["link_deezer"]

    if preview_url:
        st.audio(preview_url)                                     # Reproduce la preview de la canción

    if link_deezer:
        st.link_button(                                          # Abre la canción en Deezer
            "Abrir canción en Deezer",
            link_deezer
        )