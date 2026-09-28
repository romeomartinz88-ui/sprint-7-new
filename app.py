import pandas as pd
import plotly.express as px
import streamlit as st

# ---------- Carga y limpieza de datos ----------
raw_data = pd.read_csv('vehicles_us.csv')
car_data = raw_data.copy()

# Misma limpieza que en notebooks/EDA.ipynb
# (mediana por modelo y, si no hay dato, mediana global)
for col in ['cylinders', 'model_year', 'odometer']:
    median_by_model = car_data.groupby('model')[col].transform('median')
    car_data[col] = car_data[col].fillna(median_by_model)
    car_data[col] = car_data[col].fillna(car_data[col].median())

car_data['cylinders'] = car_data['cylinders'].astype(int)
car_data['model_year'] = car_data['model_year'].astype(int)
car_data['paint_color'] = car_data['paint_color'].fillna('unknown')
car_data['is_4wd'] = car_data['is_4wd'].fillna(0).astype(int)

# ---------- Interfaz ----------
st.header('Análisis de anuncios de venta de vehículos')
st.write(
    'Datos originales de `vehicles_us.csv`, limpiados en el notebook `EDA.ipynb`: '
    'los valores nulos se rellenaron con la mediana por modelo (y la mediana global '
    'cuando el modelo no tenía datos), `paint_color` con "unknown" e `is_4wd` con 0.'
)

# Casilla: datos limpios
show_data = st.checkbox('Mostrar datos limpios')
if show_data:
    st.write(f'Filas: {car_data.shape[0]:,} | Columnas: {car_data.shape[1]}')
    st.dataframe(car_data, height=400)  # tabla con scroll

# Casilla: resumen de columnas (tipo info)
show_info = st.checkbox('Mostrar resumen de columnas (info)')
if show_info:
    info_df = pd.DataFrame({
        'columna': car_data.columns,
        'tipo de dato': car_data.dtypes.astype(str).values,
        'nulos antes de limpiar': raw_data.isna().sum().values,
        'nulos después de limpiar': car_data.isna().sum().values,
    })
    st.dataframe(info_df, hide_index=True)

# Casilla: histograma
build_histogram = st.checkbox('Construir histograma')
if build_histogram:
    st.write('Histograma del kilometraje (odometer)')
    fig = px.histogram(car_data, x='odometer')
    st.plotly_chart(fig, use_container_width=True)

# Casilla: gráfico de dispersión
build_scatter = st.checkbox('Construir gráfico de dispersión')
if build_scatter:
    st.write('Relación entre kilometraje (odometer) y precio (price)')
    fig = px.scatter(car_data, x='odometer', y='price')
    st.plotly_chart(fig, use_container_width=True)