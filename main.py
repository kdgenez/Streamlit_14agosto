import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# ------------------------------------
# Configuración de la página
# ------------------------------------
st.set_page_config(
    page_title="Análisis Exploratorio con Datos Aleatorios",
    layout="wide"
)

st.title("📊 Análisis Exploratorio de Datos Aleatorios")
st.markdown(
    """
    Este dashboard genera un conjunto de datos aleatorios y realiza un análisis exploratorio básico.
    Incluye visualizaciones en **gráfica de barras** y **gráfica de líneas** usando Plotly.
    """
)

# ------------------------------------
# Generar datos aleatorios
# ------------------------------------
st.sidebar.header("⚙️ Configuración de datos")
num_filas = st.sidebar.slider("Número de filas", min_value=10, max_value=100, value=30, step=5)
num_columnas = st.sidebar.slider("Número de columnas", min_value=2, max_value=5, value=3)

np.random.seed(42)
columnas = [f"Variable_{i+1}" for i in range(num_columnas)]
datos = pd.DataFrame(np.random.randint(0, 100, size=(num_filas, num_columnas)), columns=columnas)

# Agregar una columna de categorías para ejemplo
datos["Categoría"] = np.random.choice(["A", "B", "C"], size=num_filas)

# ------------------------------------
# Mostrar datos y estadísticas
# ------------------------------------
st.subheader("📋 Vista previa de los datos")
st.dataframe(datos)

st.subheader("📈 Estadísticas descriptivas")
st.write(datos.describe())

# ------------------------------------
# Visualización: Barras
# ------------------------------------
st.subheader("📊 Gráfica de Barras")
columna_barras = st.selectbox("Selecciona variable para gráfica de barras:", columnas)
barras = datos.groupby("Categoría")[columna_barras].mean().reset_index()
fig_barras = px.bar(
    barras,
    x="Categoría",
    y=columna_barras,
    color="Categoría",
    title=f"Promedio de {columna_barras} por Categoría"
)
st.plotly_chart(fig_barras, use_container_width=True)

# ------------------------------------
# Visualización: Líneas
# ------------------------------------
st.subheader("📈 Gráfica de Líneas")
columna_linea = st.selectbox("Selecciona variable para gráfica de líneas:", columnas)
fig_linea = px.line(
    datos,
    y=columna_linea,
    title=f"Evolución de {columna_linea} en el tiempo",
    markers=True
)
st.plotly_chart(fig_linea, use_container_width=True)
