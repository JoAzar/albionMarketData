
import datetime
import requests
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

@st.cache_data(ttl=3600)  # Cache por 1 hora
def get_cotizacion_dolar():
    url = 'https://dolarapi.com/v1/dolares'
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        today = datetime.date.today()
        last_week_date = today - datetime.timedelta(days=7)
        filtered_data = []

        #Filtrar casas
        casas_dolar_validas = ['mayorista', 'cripto', 'blue', 'oficial', 'tarjeta', 'bolsa', 'contadoconliqui']  # Filtrar por estos tipos de casas

        for entry in data:
            if entry['casa'] in casas_dolar_validas:
                entry_date = datetime.datetime.strptime(entry['fechaActualizacion'], '%Y-%m-%dT%H:%M:%S.%fZ').date()
                if last_week_date <= entry_date <= today:
                    filtered_data.append(entry)

        return filtered_data
    else:
        print("Error al obtener los datos.")
        return []
    
#FUNCION DE COTIZACIONES
def mostrar_cotizacion_dolar():
    with st.spinner('Cargando datos...'):
        last_week_data = get_cotizacion_dolar()

    if last_week_data:
        # Filtrar solo los últimos datos por cada casa
        latest_data = {
            'mayorista': {'compra': None, 'venta': None},
            'cripto': {'compra': None, 'venta': None},
            'blue': {'compra': None, 'venta': None},
            'oficial': {'compra': None, 'venta': None},
            'tarjeta': {'compra': None, 'venta': None},
            'bolsa': {'compra': None, 'venta': None},
            'contadoconliqui': {'compra': None, 'venta': None}
        }

        for entry in last_week_data:
            casa = entry['casa']
            if casa in latest_data:
                latest_data[casa]['compra'] = entry['compra']
                latest_data[casa]['venta'] = entry['venta']

        #Mostrar las métricas en columnas
        for casa in latest_data:
            compra = latest_data[casa]['compra']
            venta = latest_data[casa]['venta']

            if compra is not None and venta is not None:
                col1, col2 = st.columns(2)
                col1.markdown(f"""
                <div style="background-color: black; padding: .5em; border-radius: 5px; margin: 20px; text-align: center; drop-shadow: 0 4px 8px rgba(0, 0, 0, 0.4); border-radius: 30px 0px 0px 30px; border-right: 5px solid green;">
                    <h4 style="color: green; text-align: center; filter: drop-shadow(0 0 0.50rem black);">{casa.capitalize()} Compra</h4>
                    <p style="font-size: 3em; color: white; filter: drop-shadow(0 0 0.20rem black);">${compra}</p>
                </div>
                """, unsafe_allow_html=True)

                col2.markdown(f"""
                <div style="background-color: black; padding: .5em; border-radius: 5px; margin: 20px; text-align: center; drop-shadow: 0 4px 8px rgba(0, 0, 0, 0.4); border-radius: 0px 30px 30px 0px; border-left: 5px solid orange;">
                    <h4 style="color: orange; text-align: center; filter: drop-shadow(0 0 0.50rem black);">{casa.capitalize()} Venta</h4>
                    <p style="font-size: 3em; color: white; filter: drop-shadow(0 0 0.20rem black);">${venta}</p>
                </div>
                """, unsafe_allow_html=True)

            else:
                st.warning(f"No se encontraron datos para {casa.capitalize()}.")
    else:
        st.warning("No se encontraron datos para el dolar en la última semana.")

if __name__ == "__main__":
    mostrar_cotizacion_dolar()