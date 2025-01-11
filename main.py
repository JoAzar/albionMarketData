import requests
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st
from productos import productos
import requests



st.title("Comparativa de Precios en Albion Online")

#Selección del producto
option = st.selectbox("Seleccione el producto:", [
    "Peces","Joyas","Producto T2", "Producto T3", 
    "Producto T4", "Producto T4 1", "Producto T4 2", "Producto T4 3", "Producto T4 4", 
    "Producto T5", "Producto T5 1", "Producto T5 2", "Producto T5 3", "Producto T5 4",
    "Producto T6", "Producto T6 1", "Producto T6 2", "Producto T6 3", "Producto T6 4",
    "Producto T7", "Producto T7 1", "Producto T7 2", "Producto T7 3", "Producto T7 4",
    "Producto T8", "Producto T8 1", "Producto T8 2", "Producto T8 3", "Producto T8 4"
    ])

#Selección del ítem dentro del producto
item_option = st.selectbox("Seleccione el ítem:", list(productos[option].keys()))
item_id = productos[option][item_option]

#Selección de la región
region = st.selectbox("Seleccione la región:", ["europe", "west", "east"])

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

        col1, col2 = st.columns(2)

        with col1:
            st.write("Precio de Venta")
            st.dataframe(df_sell)

        with col2:
            st.write("Precio de Compra")
            st.dataframe(df_buy)

        # Configuración de estilo de Seaborn sin fondo
        sns.set(style="ticks", palette="muted")

        # Gráfico de precios de Venta
        if not df_sell.empty:
            plt.figure(figsize=(12, 8))
            ax = sns.barplot(x='Ciudad', y='Precio Venta', data=df_sell, color='skyblue')
            
            # Mejorar el título, etiquetas y formato
            ax.set_title(f'Precios de Venta por Ciudad - {item_id}', fontsize=16, fontweight='bold', color='blue', pad=20)
            ax.set_xlabel('Ciudad', fontsize=14, fontweight='bold', color='darkgray')
            ax.set_ylabel('Precio de Venta', fontsize=14, fontweight='bold', color='darkgray', labelpad=20)

            #ejes
            plt.xticks(rotation=45, ha='right', fontsize=12, color='white')
            plt.yticks(fontsize=12, color='white')

            # Añadir anotaciones con los valores de las barras
            for p in ax.patches:
                ax.annotate(f'{p.get_height():.2f}', (p.get_x() + p.get_width() / 2., p.get_height()),
                ha='center', va='center', fontsize=12, color='white', xytext=(0, 10), textcoords='offset points')

            plt.gcf().patch.set_facecolor('none')
            ax.set_facecolor('none')
            st.pyplot(plt)

        # Gráfico de precios de Compra
        if not df_buy.empty:
            plt.figure(figsize=(12, 8))
            ax = sns.barplot(x='Ciudad', y='Precio Compra', data=df_buy, color='orange')
            
            # Mejorar el título, etiquetas y formato
            ax.set_title(f'Precios de Compra por Ciudad - {item_id}', fontsize=16, fontweight='bold', color='orange', pad=20)
            ax.set_xlabel('Ciudad', fontsize=14, fontweight='bold', color='darkgray')
            ax.set_ylabel('Precio de Compra', fontsize=14, fontweight='bold', color='darkgray', labelpad=20)

            #ejes
            plt.xticks(rotation=45, ha='right', fontsize=12, color='white')
            plt.yticks(fontsize=12, color='white')

            for p in ax.patches:
                ax.annotate(f'{p.get_height():.2f}', (p.get_x() + p.get_width() / 2., p.get_height()),
                ha='center', va='center', fontsize=12, color='white', xytext=(0, 10), textcoords='offset points')

            plt.gcf().patch.set_facecolor('none')
            ax.set_facecolor('none')

            st.pyplot(plt)
    else:
        st.warning("No se encontraron datos para el ítem seleccionado.")