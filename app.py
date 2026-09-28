import pandas as pd
import plotly.express as px
import streamlit as st

car_data = pd.read_csv('vehicles_us.csv')

st.header('Análisis de anuncios de venta de vehículos')

hist_button = st.button('Construir histograma')
if hist_button:
    st.write('Histograma del kilometraje (odometer)')
    fig = px.histogram(car_data, x='odometer')
    st.plotly_chart(fig, width="stretch")

scatter_button = st.button('Construir gráfico de dispersión')
if scatter_button:
    st.write('Relación entre kilometraje (odometer) y precio (price)')
    fig = px.scatter(car_data, x='odometer', y='price')
    st.plotly_chart(fig, width="stretch")