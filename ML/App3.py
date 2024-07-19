import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static
from folium.features import DivIcon
import ML_funciones
import matplotlib.colors as mcolors

df_locales_ml = pd.read_csv("df_locales_ml.csv")

def get_color(score):
    cmap = mcolors.LinearSegmentedColormap.from_list("", ["red", "yellow", "green"])
    norm = mcolors.Normalize(vmin=0, vmax=10)
    return mcolors.rgb2hex(cmap(norm(score)))

with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.image("banner.jpg", width=1000)
st.title("FindEden: Encuentra tu propio Eden")
st.header("Bienvenido/a. Selecciona tus preferencias:")

val_res = st.selectbox("Cuánto valor tiene para vos contar con buenos restaurantes en tu barrio ?:", ["Mucho", "Normal", "Poco", "Nada"])
restaurant = None
if val_res in ["Mucho", "Normal", "Poco"]:
    restaurant = st.selectbox("Qué tipos de restaurantes te gustan ?:", ['Comida asiática', 'Comida latina', 'Comida europea', 'Comida norteamericana', 'Comida vegana'])

val_rel = st.selectbox("Cuánto valor tiene para vos contar con lugares de culto en tu barrio ?:", ["Mucho", "Normal", "Poco", "Nada"])
religion = None
if val_rel in ["Mucho", "Normal", "Poco"]:
    religion = st.selectbox("Selecciona una religión:", ['Protestante', 'Católico', 'Judío', 'Budista', 'Musulmán'])

val_rec = st.selectbox("Cuánto valor tiene para vos contar con lugares recreativos en tu barrio ?:", ["Mucho", "Normal", "Poco", "Nada"])
recreation = None
if val_rec in ["Mucho", "Normal", "Poco"]:
    recreation = st.selectbox("A qué tipo de lugares te gusta acudir en general ?:", ['Arte/Música/Teatro', 'Clubes nocturno', 'Bares Deportivos/Bowling/Pool'])

button_pressed = st.button("Generar mapa")

if button_pressed:
    val_res_mapping = {"Mucho": 3, "Normal": 2, "Poco": 1, "Nada": 0}
    res_p = val_res_mapping[val_res]
    res_cat = 0

    restaurant_mapping = {'Comida asiática': 1, 'Comida latina': 2, 'Comida europea': 3, 'Comida norteamericana': 4, 'Comida vegana': 5}
    res_cat = restaurant_mapping[restaurant] if restaurant else 0

    val_rel_mapping = {"Mucho": 3, "Normal": 2, "Poco": 1, "Nada": 0}
    rel_p = val_rel_mapping[val_rel]

    religion_mapping = {'Protestante': 1, 'Católico': 2, 'Judío': 3, 'Budista': 4, 'Musulmán': 5}
    rel_cat = religion_mapping[religion] if religion else 0

    val_rec_mapping = {"Mucho": 3, "Normal": 2, "Poco": 1, "Nada": 0}
    rec_p = val_rec_mapping[val_rec]

    recreation_mapping = {'Arte/Música/Teatro': 1, 'Club nocturno': 2, 'Bares Deportivos/Bowling/Pool': 3}
    rec_cat = recreation_mapping[recreation] if recreation else 0

    lat_1 = 34.058092
    lon_1 = -118.292130
    lat_2 = 34.032025
    lon_2 = -118.244198
    lat_3 = 34.047421
    lon_3 = -118.256777
    lat_4 = 34.027630
    lon_4 = -118.266843
    lat_5 = 34.015112
    lon_5 = -118.251910
    lat_6 = 33.993401
    lon_6 = -118.278310

    lat_inm, lon_inm = ML_funciones.group_coordinates(
        lat_1, lon_1,
        lat_2, lon_2,
        lat_3, lon_3,
        lat_4, lon_4,
        lat_5, lon_5,
        lat_6, lon_6
    )

    user_pref = ML_funciones.generate_user_preferences(res_p, res_cat, rel_p, rel_cat, rec_p, rec_cat, 0)

    df_App, df_locales = ML_funciones.obtener_recomendacion(df_locales_ml, user_pref, 0.5, lat_inm, lon_inm)

    m = folium.Map(location=[df_App['lat'].mean(), df_App['lon'].mean()], zoom_start=12)

    for idx, row in df_App.iterrows():
        score = round(row['score_inm'], 2)

        # Ajustar el score y el texto si el score es menor a 5
        if score < 5:
            display_score = "<5"
            adjusted_score = 5
        else:
            display_score = str(score)
            adjusted_score = score

        size = int((adjusted_score / 10) * 10) + 5
        color = get_color(score)

        folium.CircleMarker(
            location=[row['lat'], row['lon']],
            radius=10,
            color='green',
            fill=True,
            popup=f"Inmueble {row['inmueble']} con puntuación de: {row['score_inm']}"
        ).add_to(m)

        folium.map.Marker(
            [row['lat'], row['lon']],
            icon=DivIcon(
                icon_size=(150, 36),
                icon_anchor=(0, 0),
                html=f'<div style="font-size: {size}pt; color: {color}; font-weight: bold; background-color: #E6D6C1; padding: 2px 5px; border-radius: 5px; text-align: center; width: 50px;">{display_score}</div>',
            )
        ).add_to(m)

        colors_locales = {
            'bien': 'red',
            'res': 'purple',
            'rel': 'blue',
            'rec': 'black'
        }

        inmueble_codigo = row['inmueble']
        df_locales_filtrada = df_locales[df_locales['inmueble'] == inmueble_codigo]
        for _, local_row in df_locales_filtrada.iterrows():
            secondary_color = colors_locales.get(local_row['ml_category'], 'gray')
            nombre = local_row['address'].split(',')[0]

            if pd.notna(local_row['rating_3_months']):
                popup_content = f"Nombre: {nombre}, puntuación: {local_row['rating']:.2f}. Se estima que dentro de tres meses sea: {local_row['rating_3_months']:.2f}"
            else:
                popup_content = f"Nombre: {nombre}, puntuación: {local_row['rating']:.2f}"

            folium.CircleMarker(
                location=[local_row['latitude'], local_row['longitude']],
                radius=5,
                color=secondary_color,
                fill=True,
                popup=popup_content
            ).add_to(m)

            folium.PolyLine(
                locations=[[row['lat'], row['lon']], [local_row['latitude'], local_row['longitude']]],
                color='gray',
                weight=1,
                opacity=0.7
            ).add_to(m)

    # Leyenda como componente HTML de Streamlit
    legend_html = """
    <div class='legend-container'>
    <div style='position: absolute; top: 10%; right: 5%; width: 150px; background-color: rgba(255, 255, 255, 1);
    border-radius: 10px; padding: 10px; font-size: 14px; z-index: 1000;'>
    <b>Leyenda:</b>
    <ul style='list-style-type: none; padding-left: 10px;'>
        <li><span style='background: green; padding: 5px; border-radius: 5px;'></span>  INMUEBLES </li>
        <li><span style='background: purple; padding: 5px; border-radius: 5px;'></span>  Restaurants </li>
        <li><span style='background: blue; padding: 5px; border-radius: 5px;'></span>  Culto </li>
        <li><span style='background: black; padding: 5px; border-radius: 5px;'></span>  Recreación </li>
        <li><span style='background: red; padding: 5px; border-radius: 5px;'></span>  Bienestar </li>
    </ul>
    </div>
    """
    st.markdown(legend_html, unsafe_allow_html=True)

    folium_static(m)

    st.subheader("Mensajes:")
    for i, mensajes in enumerate(df_App['mensajes'], start=1):
        st.write(f"Ubicación {i}:")
        for mensaje in mensajes:
            st.write(f"* {mensaje}")

