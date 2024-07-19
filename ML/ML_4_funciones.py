# Funciones del sistema de recomendación para aplicar en la API

# Carga de librerías

import ast
import pandas as pd
import numpy as np
import math

#
#
def generate_user_preferences(res_w, res_sc, rel_w, rel_sc, rec_w, rec_sc, ct):

    """
    Genera las preferencias de usuario basadas en los pesos y subcategorías proporcionadas.

    Args:
        res_w (int): Peso para la categoría 'Restaurant'. Debe ser uno de [0, 1, 2, 3].
        res_sc (int): Subcategoría para 'Restaurant'. Debe ser uno de [0, 1, 2, 3, 4, 5].
        rel_w (int): Peso para la categoría 'Religion'. Debe ser uno de [0, 1, 2, 3].
        rel_sc (int): Subcategoría para 'Religion'. Debe ser uno de [0, 1, 2, 3, 4, 5].
        rec_w (int): Peso para la categoría 'Recreation'. Debe ser uno de [0, 1, 2, 3].
        rec_sc (int): Subcategoría para 'Recreation'. Debe ser uno de [0, 1, 2, 3].
        ct (int): Cronotipo del usuario. Debe ser uno de [0, 1].

    Returns:
        dict: Diccionario que contiene las preferencias del usuario para cada categoría y subcategoría.
    
    Raises:
        ValueError: Si alguno de los argumentos proporcionados no es válido.

    Ejemplo:
        user_prefs = generate_user_preferences(2, 1, 3, 0, 1, 2, 0)
        print(user_prefs)
        # Output: {'Restaurant': {'weight': 2, 'sub_category': 1},
        #          'Religion': {'weight': 3, 'sub_category': 0},
        #          'Recreation': {'weight': 1, 'sub_category': 2},
        #          'Cronotipo': 0}
    """

    # Definir los pesos y subcategorías
    weights = [0, 1, 2, 3]
    restaurant_subcategories = [0, 1, 2, 3, 4, 5]
    religion_subcategories = [0, 1, 2, 3, 4, 5]
    recreation_subcategories = [0, 1, 2, 3]
    chronotypes = [0, 1]  # Incluye el 2 para "Indiferente/ambos"

    # Validar las entradas
    if res_w not in weights:
        raise ValueError(f"res_w debe estar en {weights}, pero se recibió {res_w}")
    if res_sc not in restaurant_subcategories:
        raise ValueError(f"res_sc debe estar en {restaurant_subcategories}, pero se recibió {res_sc}")
    if rel_w not in weights:
        raise ValueError(f"rel_w debe estar en {weights}, pero se recibió {rel_w}")
    if rel_sc not in religion_subcategories:
        raise ValueError(f"rel_sc debe estar en {religion_subcategories}, pero se recibió {rel_sc}")
    if rec_w not in weights:
        raise ValueError(f"rec_w debe estar en {weights}, pero se recibió {rec_w}")
    if rec_sc not in recreation_subcategories:
        raise ValueError(f"rec_sc debe estar en {recreation_subcategories}, pero se recibió {rec_sc}")
    if ct not in chronotypes:
        raise ValueError(f"ct debe estar en {chronotypes}, pero se recibió {ct}")

    # Generar preferencias del usuario
    user_preferences = {
        "Restaurant": {
            "weight": res_w,
            "sub_category": res_sc
        },
        "Religion": {
            "weight": rel_w,
            "sub_category": rel_sc
        },
        "Recreation": {
            "weight": rec_w,
            "sub_category": rec_sc
        },
        "Cronotipo": ct
    }
    
    return user_preferences

#
#
def group_coordinates(*coords):

    """
    Agrupa coordenadas en listas separadas de latitudes y longitudes.

    Args:
        *coords: Una secuencia de números representando las coordenadas, alternando entre latitudes y longitudes.

    Returns:
        tuple: Dos listas, la primera contiene las latitudes y la segunda contiene las longitudes.
    
    Raises:
        ValueError: Si el número de coordenadas no es par.

    Ejemplo:
        latitudes, longitudes = group_coordinates(34.05, -118.25, 40.71, -74.01)
        print(latitudes)  # Output: [34.05, 40.71]
        print(longitudes) # Output: [-118.25, -74.01]
    """

    lat_inm = []
    lon_inm = []

    for i in range(0, len(coords), 2):
        lat_inm.append(coords[i])
        lon_inm.append(coords[i+1])

    return lat_inm, lon_inm

#
#
def filtrar_locales(df_locales, lat_inm, lon_inm, km, user_pref):

    """
    Filtra locales en función de la ubicación y las preferencias del usuario.

    Args:
        df_locales (pd.DataFrame): DataFrame que contiene información sobre los locales.
        lat_inm (float): Latitud de la ubicación del inmueble.
        lon_inm (float): Longitud de la ubicación del inmueble.
        km (float): Radio en kilómetros para filtrar locales alrededor del inmueble.
        user_pref (dict): Diccionario con las preferencias del usuario. Debe contener
                          las categorías 'Restaurant', 'Religion', 'Recreation' con
                          sus respectivos 'weight' y 'sub_category'.

    Returns:
        pd.DataFrame: DataFrame filtrado que contiene solo los locales de interés según
                      la ubicación y las preferencias del usuario.

    Raises:
        ValueError: Si algún valor de las preferencias del usuario no es válido.

    Ejemplo:
        df_locales_filtrados = filtrar_locales(df_locales, 34.05, -118.25, 5, user_pref)
        print(df_locales_filtrados.head())
    """
    
    df_locales_copy = df_locales.copy()

    # Función para determinar la categoría
    def determinar_categoria(row):
        if any(row[['res_asian', 'res_latin', 'res_euro', 'res_fast', 'res_vegan']] != 0):
            return 'res'
        elif row['religion'] != 0:
            return 'rel'
        elif row['recreation'] != 0:
            return 'rec'
        elif row['bienestar'] != 0:
            return 'bien'
        else:
            return np.nan

    # Crear la nueva columna 'ml_category'
    df_locales_copy['ml_category'] = df_locales_copy.apply(determinar_categoria, axis=1)
    
    # Filtrar el DataFrame según el área determinada
    df_locales_copy = df_locales_copy[
    (df_locales_copy['latitude'] >= (lat_inm - 0.0045 * km * 2)) & 
    (df_locales_copy['latitude'] <= (lat_inm + 0.0045 * km * 2)) &
    (df_locales_copy['longitude'] >= (lon_inm - 0.0054 * km * 2)) & 
    (df_locales_copy['longitude'] <= (lon_inm + 0.0054 * km * 2))
    ]
    
    # Filtrar el DataFrame a partir de las preferencias del usuario

    # Filtrar según el peso
    if user_pref['Restaurant']['weight'] == 0:
        df_locales_copy = df_locales_copy[
            (df_locales_copy['res_asian'] != 1) &
            (df_locales_copy['res_latin'] != 1) &
            (df_locales_copy['res_euro'] != 1) &
            (df_locales_copy['res_fast'] != 1) &
            (df_locales_copy['res_vegan'] != 1)
        ]
    if user_pref['Religion']['weight'] == 0:
        df_locales_copy = df_locales_copy[df_locales_copy['religion'] != 1]
    if user_pref['Recreation']['weight'] == 0:
        df_locales_copy = df_locales_copy[df_locales_copy['recreation'] != 1]

    # Filtrar según la sub-categoría para "Restaurant"
    restaurant_sub_category = user_pref['Restaurant']['sub_category']
    if restaurant_sub_category == 1:
        df_locales_copy = df_locales_copy[
            (df_locales_copy['res_asian'] == 1) |
            ((df_locales_copy['res_asian'] == 0) & 
            (df_locales_copy['res_latin'] == 0) & 
            (df_locales_copy['res_euro'] == 0) & 
            (df_locales_copy['res_fast'] == 0) & 
            (df_locales_copy['res_vegan'] == 0))
        ]
    elif restaurant_sub_category == 2:
        df_locales_copy = df_locales_copy[
            (df_locales_copy['res_latin'] == 1) |
            ((df_locales_copy['res_asian'] == 0) & 
            (df_locales_copy['res_latin'] == 0) & 
            (df_locales_copy['res_euro'] == 0) & 
            (df_locales_copy['res_fast'] == 0) & 
            (df_locales_copy['res_vegan'] == 0))
        ]
    elif restaurant_sub_category == 3:
        df_locales_copy = df_locales_copy[
            (df_locales_copy['res_euro'] == 1) |
            ((df_locales_copy['res_asian'] == 0) & 
            (df_locales_copy['res_latin'] == 0) & 
            (df_locales_copy['res_euro'] == 0) & 
            (df_locales_copy['res_fast'] == 0) & 
            (df_locales_copy['res_vegan'] == 0))
        ]
    elif restaurant_sub_category == 4:
        df_locales_copy = df_locales_copy[
            (df_locales_copy['res_fast'] == 1) |
            ((df_locales_copy['res_asian'] == 0) & 
            (df_locales_copy['res_latin'] == 0) & 
            (df_locales_copy['res_euro'] == 0) & 
            (df_locales_copy['res_fast'] == 0) & 
            (df_locales_copy['res_vegan'] == 0))
        ]
    elif restaurant_sub_category == 5:
        df_locales_copy = df_locales_copy[
            (df_locales_copy['res_vegan'] == 1) |
            ((df_locales_copy['res_asian'] == 0) & 
            (df_locales_copy['res_latin'] == 0) & 
            (df_locales_copy['res_euro'] == 0) & 
            (df_locales_copy['res_fast'] == 0) & 
            (df_locales_copy['res_vegan'] == 0))
        ]

    # Filtrar según la sub-categoría para "Religion"
    religion_sub_category = user_pref['Religion']['sub_category']
    df_locales_copy = df_locales_copy[
        (df_locales_copy['religion'] == religion_sub_category) |
        (df_locales_copy['religion'] == 0)
    ]

    # Filtrar según la sub-categoría para "Recreation"
    recreation_sub_category = user_pref['Recreation']['sub_category']
    df_locales_copy = df_locales_copy[
        (df_locales_copy['recreation'] == recreation_sub_category) |
        (df_locales_copy['recreation'] == 0)
    ]

    # Dejo solo columnas de interes
    
    # Añadir columna "distance" al DataFrame
    df_locales_copy['distance'] = df_locales_copy.apply(
        lambda row: calcular_distancia(row['latitude'], row['longitude'], lat_inm, lon_inm),
        axis=1
    )
    df_filtrado = df_locales_copy[['address','gmap_id', 'latitude', 'longitude','avg_rating',
       'num_of_reviews','religion', 'recreation', 'bienestar', 'avg_rating_correction','forecast', 'tendencia','rating_3_months', 'time_category', 'distance','ml_category']]

    return df_filtrado

#
#
def calcular_distancia(lat_1, long_1, lat_2, long_2):

    """
    Calcula la distancia en metros entre dos puntos geográficos especificados por sus latitudes y longitudes.

    Args:
        lat_1 (float): Latitud del primer punto.
        long_1 (float): Longitud del primer punto.
        lat_2 (float): Latitud del segundo punto.
        long_2 (float): Longitud del segundo punto.

    Returns:
        float: Distancia en metros entre los dos puntos, redondeada a la centena más cercana.

    Ejemplo:
        distancia = calcular_distancia(34.05, -118.25, 36.16, -115.15)
        print(distancia)  # Output: 360000.0 (por ejemplo)
    """

    # Constantes para convertir grados a metros
    METROS_POR_GRADO_LAT = 111320  # Aprox. para todas las latitudes
    METROS_POR_GRADO_LONG = 111320 * math.cos(math.radians(lat_1))  # Varía según la latitud

    # Diferencias en grados
    delta_lat = lat_2 - lat_1
    delta_long = long_2 - long_1

    # Convertir diferencias en grados a diferencias en metros
    delta_lat_metros = delta_lat * METROS_POR_GRADO_LAT
    delta_long_metros = delta_long * METROS_POR_GRADO_LONG

    # Calcular distancia euclidiana
    distancia_metros = math.sqrt(delta_lat_metros**2 + delta_long_metros**2)
    
    # Redondear a la centena más cercana
    distancia_redondeada = round(distancia_metros, -2)
    
    return distancia_redondeada

#
#
def calcular_puntuacion(df_prueba, user_pref):

    """
    Calcula el puntaje total de una zona basada en las preferencias del usuario y las características de los locales en la zona.

    Args:
        df_prueba (pd.DataFrame): DataFrame con los datos de los locales en la zona.
        user_pref (dict): Diccionario con las preferencias del usuario, incluyendo pesos y subcategorías para "Restaurant", "Religion" y "Recreation".

    Returns:
        tuple: Contiene el puntaje total, los puntajes individuales para restaurantes, religión, recreación y bienestar, y una lista de mensajes con la información de los mejores locales encontrados.

    Ejemplo:
        user_pref = {
            'Restaurant': {'weight': 3, 'sub_category': 1},
            'Religion': {'weight': 2, 'sub_category': 1},
            'Recreation': {'weight': 1, 'sub_category': 1}
        }
        total_score, score_res, score_rel, score_rec, score_bien, messages = calcular_puntuacion(df_prueba, user_pref)
        print(total_score)  # Output: 8.6 (por ejemplo)
        print(messages)     # Output: ["Tienes un restaurante llamado 'Best Restaurant' a 100 metros con una valoración histórica de 4.8 y una predicción de 4.9 dentro de tres meses"]
    """

    total_score = 0
    score_res = 0
    score_rel = 0
    score_rec = 0
    score_bien = 0

    best_restaurant = ""
    best_bienestar = ""
    best_recreation = ""
    best_religion = ""

    df = df_prueba.copy()

    # Restaurantes (bienestar, recreation, religion son 0)
    restaurants = df[(df['bienestar'] == 0) & (df['recreation'] == 0) & (df['religion'] == 0)]
    if len(restaurants) > 0:
        if len(restaurants) == 1:
            score_res = 4
        elif len(restaurants) in [2, 3]:
            score_res = 4.3
        else:
            score_res = 4.5
        
        max_avg_rating = max(restaurants['avg_rating'].max(), restaurants['avg_rating_correction'].max())
        if max_avg_rating > 4.5:
            score_res += 0.3
        
        # Encontrar el restaurante con el max_avg_rating más alto
        best_restaurant_idx = restaurants.loc[
            (restaurants['avg_rating'] == max_avg_rating) |
            (restaurants['avg_rating_correction'] == max_avg_rating)
        ].index[0]
        
        if df.at[best_restaurant_idx, 'forecast'] == 'fuerte':
            if df.at[best_restaurant_idx, 'tendencia'] == 'Alta':
                score_res += 0.2
        elif df.at[best_restaurant_idx, 'tendencia'] == 'Alta':
            score_res += 0.1

        # Guardar el mejor restaurante
        best_restaurant = df.at[best_restaurant_idx, 'address']
        best_restaurant_name = best_restaurant.split(',')[0]
        best_restaurant_rating = max(
        df.at[best_restaurant_idx, 'avg_rating'], 
        df.at[best_restaurant_idx, 'avg_rating_correction'] if pd.notna(df.at[best_restaurant_idx, 'avg_rating_correction']) else -np.inf
        )
        best_restaurant_rating = round(best_restaurant_rating, 2)
        best_restaurant_dist = df.at[best_restaurant_idx, 'distance']
        best_restaurant_fc = df.at[best_restaurant_idx, 'rating_3_months']

        
    
    # Bienestar (bienestar es 1)
    bienestar = df[df['bienestar'] == 1]
    if len(bienestar) > 0:
        if len(bienestar) == 1:
            score_bien = 1.5
        elif len(bienestar) in [2, 3]:
            score_bien = 2
        else:
            score_bien = 2.5
        
        max_avg_rating = max(bienestar['avg_rating'].max(), bienestar['avg_rating_correction'].max())
        if max_avg_rating > 4.5:
            score_bien += 0.3
        
        best_bienestar_idx = bienestar.loc[
            (bienestar['avg_rating'] == max_avg_rating) |
            (bienestar['avg_rating_correction'] == max_avg_rating)
        ].index[0]
        
        if df.at[best_bienestar_idx, 'forecast'] == 'fuerte':
            if df.at[best_bienestar_idx, 'tendencia'] == 'Alta':
                score_bien += 0.2
        elif df.at[best_bienestar_idx, 'tendencia'] == 'Alta':
            score_bien += 0.1
        
        # Guardar el mejor bienestar
        best_bienestar = df.at[best_bienestar_idx, 'address']
        best_bienestar_name = best_bienestar.split(',')[0]
        best_bienestar_rating = max(
        df.at[best_bienestar_idx, 'avg_rating'], 
        df.at[best_bienestar_idx, 'avg_rating_correction'] if pd.notna(df.at[best_bienestar_idx, 'avg_rating_correction']) else -np.inf
        )
        best_bienestar_rating = round(best_bienestar_rating, 2)
        best_bienestar_dist = df.at[best_bienestar_idx, 'distance']
        best_bienestar_fc = df.at[best_bienestar_idx, 'rating_3_months']
    
    # Recreación (recreation es distinto de 0)
    recreation = df[df['recreation'] != 0]
    if len(recreation) > 0:
        if len(recreation) == 1:
            score_rec = 0.5
        elif len(recreation) in [2, 3]:
            score_rec = 0.6
        else:
            score_rec = 0.7
        
        max_avg_rating = max(recreation['avg_rating'].max(), recreation['avg_rating_correction'].max())
        if max_avg_rating > 4.5:
            score_rec += 0.1
        
        best_recreation_idx = recreation.loc[
            (recreation['avg_rating'] == max_avg_rating) |
            (recreation['avg_rating_correction'] == max_avg_rating)
        ].index[0]
        
        if df.at[best_recreation_idx, 'forecast'] == 'fuerte':
            if df.at[best_recreation_idx, 'tendencia'] == 'Alta':
                score_rec += 0.2
        elif df.at[best_recreation_idx, 'tendencia'] == 'Alta':
            score_rec += 0.1
        
        # Guardar el mejor recreación
        best_recreation = df.at[best_recreation_idx, 'address']
        best_recreation_name = best_recreation.split(',')[0]
        best_recreation_rating = max(
        df.at[best_recreation_idx, 'avg_rating'], 
        df.at[best_recreation_idx, 'avg_rating_correction'] if pd.notna(df.at[best_recreation_idx, 'avg_rating_correction']) else -np.inf
        )
        best_recreation_rating = round(best_recreation_rating, 2)
        best_recreation_dist = df.at[best_recreation_idx, 'distance']
        best_recreation_fc = df.at[best_recreation_idx, 'rating_3_months']
    
    # Religión (religion es distinto de 0)
    religion = df[df['religion'] != 0]
    if len(religion) > 0:
        if len(religion) == 1:
            score_rel = 0.5
        elif len(religion) in [2, 3]:
            score_rel = 0.6
        else:
            score_rel = 0.7
        
        max_avg_rating = max(religion['avg_rating'].max(), religion['avg_rating_correction'].max())
        if max_avg_rating > 4.5:
            score_rel += 0.1
        
        best_religion_idx = religion.loc[
            (religion['avg_rating'] == max_avg_rating) |
            (religion['avg_rating_correction'] == max_avg_rating)
        ].index[0]
        
        if df.at[best_religion_idx, 'forecast'] == 'fuerte':
            if df.at[best_religion_idx, 'tendencia'] == 'Alta':
                score_rel += 0.2
        elif df.at[best_religion_idx, 'tendencia'] == 'Alta':
            score_rel += 0.1
        
        # Guardar el mejor religión
        best_religion = df.at[best_religion_idx, 'address']
        best_religion_name = best_religion.split(',')[0]
        best_religion_rating = max(
        df.at[best_religion_idx, 'avg_rating'], 
        df.at[best_religion_idx, 'avg_rating_correction'] if pd.notna(df.at[best_religion_idx, 'avg_rating_correction']) else -np.inf
        )
        best_religion_rating = round(best_religion_rating, 2)
        best_religion_dist = df.at[best_religion_idx, 'distance']
        best_religion_fc = df.at[best_religion_idx, 'rating_3_months']


    # Ponderación final del puntaje:
    p_res = user_pref['Restaurant']['weight'] # Puede ser 0, 1, 2 o 3
    p_rec = user_pref['Recreation']['weight']
    p_rel = user_pref['Religion']['weight']

    def ajustar_score(score, ponderacion):
        if ponderacion == 1:
            return score * 0.8
        elif ponderacion == 3:
            return score + (5 - score) * 0.1
        return score

    score_res = ajustar_score(score_res, p_res)
    score_rec = ajustar_score(score_rec, p_rec)
    score_rel = ajustar_score(score_rel, p_rel)
    
    total_score = score_res + score_rel + score_bien + score_rec

    if p_res == 0:
        total_score = (5 * total_score) / 10
        
    elif p_rec == 0:
        total_score = (9 * total_score) / 10
    
    elif p_rel == 0:
        total_score = (9 * total_score) / 10
    
    messages = []

    def agregar_mensaje(category_name, category_dist, category_rating, category_fc, category_label):
        if category_fc is not None and not pd.isna(category_fc):
            return f"Tienes un {category_label} llamado '{category_name}' a {category_dist} metros con una valoración histórica de {category_rating} y una predicción de {category_fc} dentro de tres meses"
        else:
            return f"Tienes un {category_label} llamado '{category_name}' a {category_dist} metros con una valoración histórica de {category_rating}"

    if best_restaurant:
        messages.append(agregar_mensaje(best_restaurant_name, best_restaurant_dist, best_restaurant_rating, best_restaurant_fc, 'restaurante'))
    if best_bienestar:
        messages.append(agregar_mensaje(best_bienestar_name, best_bienestar_dist, best_bienestar_rating, best_bienestar_fc, 'lugar interesante'))
    if best_recreation:
        messages.append(agregar_mensaje(best_recreation_name, best_recreation_dist, best_recreation_rating, best_recreation_fc, 'lugar de recreación'))
    if best_religion:
        messages.append(agregar_mensaje(best_religion_name, best_religion_dist, best_religion_rating, best_religion_fc, 'lugar de culto'))
    
    return total_score, score_res, score_rel, score_rec, score_bien, messages

#
#
def obtener_recomendacion(df_base_datos, user_pref, km, lat_inm, lon_inm):

    """
    Genera recomendaciones de inmuebles basadas en las preferencias del usuario y la proximidad a locales de interés.

    Args:
        df_base_datos (pd.DataFrame): DataFrame con los datos de los locales.
        user_pref (dict): Diccionario con las preferencias del usuario, incluyendo pesos y subcategorías para "Restaurant", "Religion" y "Recreation".
        km (float): Radio en kilómetros para buscar locales alrededor de las coordenadas de los inmuebles.
        lat_inm (list): Lista de latitudes de los inmuebles.
        lon_inm (list): Lista de longitudes de los inmuebles.

    Returns:
        tuple: Contiene un DataFrame con los resultados de las recomendaciones para cada inmueble y un DataFrame con los detalles de los locales cercanos.

    Ejemplo:
        df_base_datos = pd.read_csv('locales.csv')
        user_pref = {
            'Restaurant': {'weight': 3, 'sub_category': 1},
            'Religion': {'weight': 2, 'sub_category': 1},
            'Recreation': {'weight': 1, 'sub_category': 1}
        }
        lat_inm = [40.7128, 34.0522]
        lon_inm = [-74.0060, -118.2437]
        km = 5.0
        resultados_df, locales_df = obtener_recomendacion(df_base_datos, user_pref, km, lat_inm, lon_inm)
        print(resultados_df)
        print(locales_df)
    """
    
    # Crear listas para almacenar los resultados y los DataFrames filtrados
    resultados = []
    df_locales_list = []

    # Iterar sobre las coordenadas
    for i, (lat, lon) in enumerate(zip(lat_inm, lon_inm)):
        df_bd_filtrada = filtrar_locales(df_base_datos, lat, lon, km, user_pref)
        score_inm, score_res, score_rel, score_rec, score_bien, mensajes = calcular_puntuacion(df_bd_filtrada, user_pref)
        
        # Crear el código del inmueble
        inmueble_codigo = f'inm_{i + 1}'
        
        # Agregar los resultados a la lista
        resultados.append({
            'inmueble': inmueble_codigo,
            'score_inm': score_inm,
            'lat': lat,
            'lon': lon,
            'mensajes': mensajes
        })

        # Modificar el DataFrame filtrado para agregar las columnas necesarias
        df_bd_filtrada['inmueble'] = inmueble_codigo
        df_bd_filtrada['rating'] = df_bd_filtrada['avg_rating_correction'].fillna(df_bd_filtrada['avg_rating']).round(2)
        
        # Seleccionar y renombrar las columnas necesarias
        df_locales = df_bd_filtrada[['inmueble', 'address', 'latitude', 'longitude', 'rating', 'rating_3_months', 'time_category', 'ml_category']]
        
        # Agregar el DataFrame a la lista
        df_locales_list.append(df_locales)
    
    # Convertir la lista de resultados a un DataFrame
    resultados_df = pd.DataFrame(resultados)
    
    # Concatenar los DataFrames de locales
    locales_df = pd.concat(df_locales_list, ignore_index=True)
    
    resultados_df["score_inm"] = resultados_df["score_inm"].round(2)
    
    return resultados_df, locales_df