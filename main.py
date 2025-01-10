import requests
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st

# Título de la app  
st.title("Comparativa de Precios en Albion Online")

# Selección del producto
option = st.selectbox("Seleccione el producto:", ["Producto T3", "Producto T4", "Producto T5"])
item_id = {"Producto T3": 'T3_HIDE', "Producto T4": 'T4_HIDE', "Producto T5": 'T5_HIDE'}[option]

# Selección de la región
region = st.selectbox("Seleccione la región:", ["europe", "asia", "west"])
url = f"https://{region}.albion-online-data.com/api/v2/stats/prices/{item_id}"

# Botón para cargar los datos
if st.button("Consultar Precios"):
    response = requests.get(url)
    # Verifica si la respuesta fue exitosa (código de estado 200)
    if response.status_code == 200:
        data = response.json()
        st.write(response)  # Verifica los datos obtenidos de la API
    else:
        st.error(f"Error en la solicitud: {response.status_code}")

    # Verificar que data no esté vacía
    if data:
        cities_sell, sell_prices = [], []
        cities_buy, buy_prices = [], []

        # Filtrar los datos con precios mayores a cero
        for item in data:
            # Verificar si el precio de venta es mayor que cero
            if item.get("sell_price_min", 0) > 0:
                cities_sell.append(item["city"])
                sell_prices.append(item["sell_price_min"])
            
            # Verificar si el precio de compra es mayor que cero
            if item.get("buy_price_min", 0) > 0:
                cities_buy.append(item["city"])
                buy_prices.append(item["buy_price_min"])

        # Mostrar datos si existen
        if cities_sell:
            df_sell = pd.DataFrame({"Ciudad": cities_sell, "Precio Venta": sell_prices})
            st.subheader("Precios de Venta")
            st.dataframe(df_sell)

            # Gráfico de precios de Venta
            plt.figure(figsize=(10, 6))
            sns.barplot(x='Ciudad', y='Precio Venta', data=df_sell, color='skyblue')
            plt.title(f'Precios de Venta por Ciudad - {item_id}')
            plt.xlabel('Ciudad')
            plt.ylabel('Precio de Venta')
            plt.xticks(rotation=45)
            st.pyplot(plt)
        else:
            st.warning("No hay precios de venta disponibles para este ítem.")

        if cities_buy:
            df_buy = pd.DataFrame({"Ciudad": cities_buy, "Precio Compra": buy_prices})
            st.subheader("Precios de Compra")
            st.dataframe(df_buy)

            # Gráfico de precios de Compra
            plt.figure(figsize=(10, 6))
            sns.barplot(x='Ciudad', y='Precio Compra', data=df_buy, color='orange')
            plt.title(f'Precios de Compra por Ciudad - {item_id}')
            plt.xlabel('Ciudad')
            plt.ylabel('Precio de Compra')
            plt.xticks(rotation=45)
            st.pyplot(plt)
        else:
            st.warning("No hay precios de compra disponibles para este ítem.")
    else:
        st.warning("No se encontraron datos para el ítem seleccionado.")