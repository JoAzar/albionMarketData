import requests
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st
from productos import productos

st.title("Comparativa de Precios en Albion Online")

#Selección del producto
option = st.selectbox("Seleccione el producto:", ["Peces","Joyas","Producto T2", "Producto T3", "Producto T4", "Producto T5"])

#Selección del ítem dentro del producto
item_option = st.selectbox("Seleccione el ítem:", list(productos[option].keys()))
item_id = productos[option][item_option]

#Selección de la región
region = st.selectbox("Seleccione la región:", ["europe", "asia", "west"])
url = f"https://{region}.albion-online-data.com/api/v2/stats/prices/{item_id}"

# Construir la URL de la imagen
image_url = f"https://render.albiononline.com/v1/item/{item_id}"

# Mostrar la imagen del ítem
st.image(image_url, caption=f"Imagen de {item_option}", width=150)

#Botón para cargar los datos
if st.button("Consultar Precios"):
    response = requests.get(url)
    data = response.json()

    if data:
        cities_sell, sell_prices = [], []
        cities_buy, buy_prices = [], []

        for item in data:
            if item.get("sell_price_min"):
                cities_sell.append(item["city"])
                sell_prices.append(item["sell_price_min"])
            if item.get("buy_price_min"):
                cities_buy.append(item["city"])
                buy_prices.append(item["buy_price_min"])

        #DataFrames
        df_sell = pd.DataFrame({"Ciudad": cities_sell, "Precio Venta": sell_prices})
        df_buy = pd.DataFrame({"Ciudad": cities_buy, "Precio Compra": buy_prices})

        #Mostrar tablas
        st.subheader("Precios de Venta")
        st.dataframe(df_sell)

        st.subheader("Precios de Compra")
        st.dataframe(df_buy)

        #Gráfico de precios de Venta
        if not df_sell.empty:
            plt.figure(figsize=(10, 6))
            sns.barplot(x='Ciudad', y='Precio Venta', data=df_sell, color='skyblue')
            plt.title(f'Precios de Venta por Ciudad - {item_id}')
            plt.xlabel('Ciudad')
            plt.ylabel('Precio de Venta')
            plt.xticks(rotation=45)
            st.pyplot(plt)

        #Gráfico de precios de Compra
        if not df_buy.empty:
            plt.figure(figsize=(10, 6))
            sns.barplot(x='Ciudad', y='Precio Compra', data=df_buy, color='orange')
            plt.title(f'Precios de Compra por Ciudad - {item_id}')
            plt.xlabel('Ciudad')
            plt.ylabel('Precio de Compra')
            plt.xticks(rotation=45)
            st.pyplot(plt)
    else:
        st.warning("No se encontraron datos para el ítem seleccionado.")