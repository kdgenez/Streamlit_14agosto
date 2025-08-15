import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# -----------------------------
# Configuración de la página
# -----------------------------
st.set_page_config(
    page_title="Análisis Experimental Biológico",
    layout="wide"
)

st.title("🧬 Análisis Exploratorio de Experimento Biológico")
st.markdown(
    """
    Esta aplicación permite explorar datos de un experimento biológico simulado con **600 muestras** y **8 variables**.
    Puedes filtrar, visualizar y analizar los datos de forma interactiva.
    """
)

# -----------------------------
# Generar datos simulados
# -----------------------------
np.random.seed(42)
num_muestras = 600
variables = [
    "Longitud", "Peso", "Temperatura", "PH", "Proteína", "Glucosa", "Lípidos", "Enzima"
]

df = pd.DataFrame({
    "Muestra": range(1, num_muestras + 1),
    "Grupo": np.random.choice(["Control", "Tratado"], size=num_muestras),
    "Longitud": np.random.normal(50, 10, num_muestras),
    "Peso": np.random.normal(20, 5, num_muestras),
    "Temperatura": np.random.normal(37, 0.5, num_muestras),
    "PH": np.random.normal(7.4, 0.3, num_muestras),
    "Proteína": np.random.normal(5, 1.2, num_muestras),
    "Glucosa": np.random.normal(100, 15, num_muestras),
    "Lípidos": np.random.normal(150, 25, num_muestras),
    "Enzima": np.random.normal(200, 30, num_muestras)
})

# -----------------------------
# Filtros en la barra lateral
# -----------------------------
st.sidebar.header("⚙️ Controles")

# Filtro por grupo
grupo_seleccionado = st.sidebar.multiselect(
    "Selecciona grupo(s):",
    options=df["Grupo"].unique(),
    default=df["Grupo"].unique()
)

# Slider para filtrar por rango de valores de una variable
variable_filtro = st.sidebar.selectbox("Variable para filtrar rango:", variables)
min_val = float(df[variable_filtro].min())
max_val = float(df[variable_filtro].max())
rango = st.sidebar.slider(
    f"Rango de {variable_filtro}",
    min_value=min_val,
    max_value=max_val,
    value=(min_val, max_val)
)

# -----------------------------
# Aplicar filtros
# -----------------------------
df_filtrado = df[
    (df["Grupo"].isin(grupo_seleccionado)) &
    (df[variable_filtro].between(rango[0], rango[1]))
]

# -----------------------------
# Checkboxes para mostrar info
# -----------------------------
if st.checkbox("Mostrar datos filtrados"):
    st.dataframe(df_filtrado)

if st.checkbox("Mostrar estadísticas descriptivas"):
    st.write(df_filtrado.describe())

# -----------------------------
# Selección de gráficos
# -----------------------------
tipos_disponibles = ["Barras", "Líneas", "Dispersión", "Histograma"]
graficos_seleccionados = st.multiselect(
    "Selecciona uno o dos tipos de gráficos para mostrar:",
    tipos_disponibles,
    default=["Barras", "Líneas"]
)

variable_x = st.selectbox("Variable en eje X:", ["Muestra", "Grupo"])
variable_y = st.selectbox("Variable en eje Y:", variables)

# -----------------------------
# Función para crear gráficos
# -----------------------------
def crear_grafico(tipo):
    if tipo == "Barras":
        return px.bar(
            df_filtrado,
            x=variable_x,
            y=variable_y,
            color="Grupo",
            title=f"{tipo} - {variable_y} vs {variable_x}"
        )
    elif tipo == "Líneas":
        return px.line(
            df_filtrado,
            x=variable_x,
            y=variable_y,
            color="Grupo",
            markers=True,
            title=f"{tipo} - {variable_y} vs {variable_x}"
        )
    elif tipo == "Dispersión":
        return px.scatter(
            df_filtrado,
            x=variable_x,
            y=variable_y,
            color="Grupo",
            title=f"{tipo} - {variable_y} vs {variable_x}"
        )
    elif tipo == "Histograma":
        return px.histogram(
            df_filtrado,
            x=variable_y,
            color="Grupo",
            nbins=20,
            title=f"{tipo} - {variable_y}"
        )

# -----------------------------
# Mostrar gráficos
# -----------------------------
if len(graficos_seleccionados) == 1:
    st.plotly_chart(crear_grafico(graficos_seleccionados[0]), use_container_width=True)
elif len(graficos_seleccionados) == 2:
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(crear_grafico(graficos_seleccionados[0]), use_container_width=True)
    with col2:
        st.plotly_chart(crear_grafico(graficos_seleccionados[1]), use_container_width=True)
else:
    st.warning("Selecciona uno o dos tipos de gráficos para mostrar.")

