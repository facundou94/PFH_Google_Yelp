#!/usr/bin/env python
# coding: utf-8

# # Importación Librerías

# In[1]:


get_ipython().system('pip install pandas matplotlib numpy re time ast collections gdown ipykernel nbconvert ipython')


# In[2]:


import pandas as pd
from io import StringIO
import gdown
import json
import os
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import ast
from collections import Counter
import numpy as np
import re
import time



# # Metadata  - Google

# ## Importar los archivos desde la GoogleDrive

# tamaño:
# carpeta: 2,76 Gb
# dataframe 370 Mb
# csv 2,3 Gb

# In[3]:


# IDs de los archivos de Google Drive
file_links = [
    'https://drive.google.com/file/d/1OnyhmyG8xzdn4XU9LYcnwzBseB1_rChS', 
    'https://drive.google.com/file/d/15D_5EkxqPP0XJb5I5bYI8b1wQV7B2fx_', 
    'https://drive.google.com/file/d/1fDBVCmf4JA7gkIyjpv5mHEMySb19C-vz', 
    'https://drive.google.com/file/d/1Mj2oUZy5gGznhthcUGi8_sgKhBwypE74', 
    'https://drive.google.com/file/d/1IXok40Zp61CGwFDgyvLUwV02c4BWGrjj',
    'https://drive.google.com/file/d/1UmsN_ZOFQqVl7W9SbnxHkSQavo1_Iwqx', 
    'https://drive.google.com/file/d/1KfQBhJlnuziKjf-9haQGaiPtCPnUUDla', 
    'https://drive.google.com/file/d/1ebTUx2klGy7L9lGlZl3GCPXxSwSD55vX', 
    'https://drive.google.com/file/d/1td6twU60LAS-z5mB0MeSJEpGhH7jcGKm', 
    'https://drive.google.com/file/d/1NQgHgNm9PV8MSiOXNoQ2UkIF9e5AdLk7', 
    'https://drive.google.com/file/d/1GYwWfH7EvWMZn14vQRNr5CjEely4eWrB'
]

# Nombres de los archivos locales (presumiendo que siguen el patrón 1.json, 2.json, ..., 11.json)
file_names = [f'{i}.json' for i in range(1, len(file_links) + 1)]

# Crear la carpeta ArchivosIgnore si no existe
output_dir = 'ArchivosIgnore'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Inicializar una lista para almacenar los DataFrames
dataframes = []

# Descargar y leer cada archivo JSON
for file_link, file_name in zip(file_links, file_names):
    try:
        # Ruta completa del archivo
        file_path = os.path.join(output_dir, file_name)
        
        # Verificar si el archivo ya está descargado
        if not os.path.exists(file_path):
            # Obtener el ID del archivo desde el enlace
            file_id = file_link.split('/d/')[1].split('/')[0]
            download_url = f'https://drive.google.com/uc?id={file_id}'
            
            # Descargar el archivo
            gdown.download(download_url, file_path, quiet=False)
        
        # Leer el archivo JSON en un DataFrame
        with open(file_path, 'r', encoding='utf-8') as file:
            first_char = file.read(1)
            if not first_char:
                raise ValueError(f"El archivo {file_name} está vacío.")
            file.seek(0)
            df = pd.read_json(file, lines=True)
        
        # Agregar el DataFrame a la lista
        dataframes.append(df)
    
    except Exception as e:
        print(f"Error al procesar el archivo {file_name}: {e}")
        if os.path.exists(file_path):
            os.remove(file_path)


# In[4]:


del df


# In[5]:


# Concatenar todos los DataFrames en uno solo
df_metadataGoog = pd.concat(dataframes, ignore_index=True)


# In[6]:


del dataframes


# ## Filtrar por estado California

# In[7]:


#extraer el estado de la dirección
df_metadataGoog['estado'] = df_metadataGoog['address'].str.extract(r', ([A-Z]{2}) \d{5}')
#filtro los datos de California, para liberar espacio
df_metadatosCA = df_metadataGoog[df_metadataGoog['estado'] == 'CA']
#elimino el dataframe que tiene los metadatos de todos los estados, para liberar memoria
del df_metadataGoog
#reseteo indice
df_metadatosCA.reset_index(inplace=True)
df_metadatosCA.drop('index', axis='columns', inplace=True)


# ## Eliminar duplicados

# In[8]:


df_metadatosCA.drop_duplicates(subset=['gmap_id'], inplace=True)


# ## Armado de columnas

# In[9]:


#solo para usar cuando se quiere importar el archivo
#df_metadatosCA=pd.read_parquet('Archivos/metadatosCA.parquet', engine='pyarrow')


# ### Extraer Ciudad

# In[10]:


# Función para extraer la ciudad
def extract_city(address):
    match = re.search(r',\s*([^,]+),\s*[A-Z]{2}\s*\d{5}', address)
    if match:
        return match.group(1).strip()
    return None

# Aplicar la función a la columna 'address' y crear la columna 'city'
df_metadatosCA['city'] = df_metadatosCA['address'].apply(extract_city)


# ### Hours

# In[11]:


# Función para asegurarse de que el tiempo esté en el formato "HH:MMAM/PM"
def ensure_time_format(time_str):
    if '–' in time_str:
        parts = time_str.split('–')
        parts = [ensure_time_format(part) for part in parts]
        return '–'.join(parts)
    try:
        if ':' not in time_str:
            time_obj = pd.to_datetime(time_str, format='%I%p', errors='coerce')
        else:
            time_obj = pd.to_datetime(time_str, format='%I:%M%p', errors='coerce')
        if time_obj is not pd.NaT:
            return time_obj.strftime('%I:%M%p')
    except Exception as e:
        print(f"Error formatting time: {time_str}, error: {e}")
    return None

# Función para calcular las horas diurnas (8 AM - 10 PM)
def calculate_day_hours(hours_array):
    total_day_hours = 0
    if hours_array is not None and isinstance(hours_array, np.ndarray):
        for entry in hours_array:
            if isinstance(entry, np.ndarray) and len(entry) == 2:
                day, hours = entry
                if 'Closed' in hours:
                    continue
                if '–' in hours:
                    open_time, close_time = hours.split('–')
                    open_time = ensure_time_format(open_time)
                    close_time = ensure_time_format(close_time)
                    
                    if open_time and close_time:
                        open_hour = pd.to_datetime(open_time, format='%I:%M%p').hour
                        close_hour = pd.to_datetime(close_time, format='%I:%M%p').hour

                        if open_hour < 8:
                            open_hour = 8
                        if close_hour > 22:
                            close_hour = 22

                        if close_hour < open_hour:
                            close_hour += 24  # Para manejar el cambio de día

                        total_day_hours += max(0, close_hour - open_hour)
    return total_day_hours

# Función para calcular las horas nocturnas (10 PM - 8 AM)
def calculate_night_hours(hours_array):
    total_night_hours = 0
    if hours_array is not None and isinstance(hours_array, np.ndarray):
        for entry in hours_array:
            if isinstance(entry, np.ndarray) and len(entry) == 2:
                day, hours = entry
                if 'Closed' in hours:
                    continue
                if '–' in hours:
                    open_time, close_time = hours.split('–')
                    open_time = ensure_time_format(open_time)
                    close_time = ensure_time_format(close_time)

                    if open_time and close_time:
                        open_hour = pd.to_datetime(open_time, format='%I:%M%p').hour
                        close_hour = pd.to_datetime(close_time, format='%I:%M%p').hour

                        if close_hour < open_hour:
                            close_hour += 24  # Para manejar el cambio de día

                        night_hours = 0
                        if open_hour < 8:
                            night_hours += min(8, close_hour) - open_hour
                        if close_hour > 22:
                            night_hours += close_hour - 22

                        total_night_hours += max(0, night_hours)
    return total_night_hours

# Aplicar las funciones al DataFrame
df_metadatosCA['Hours_day'] = df_metadatosCA['hours'].apply(calculate_day_hours)
df_metadatosCA['Hours_night'] = df_metadatosCA['hours'].apply(calculate_night_hours)


# ### Categorias

# In[12]:


# Expandir las listas en filas individuales
categorias_expandidas = df_metadatosCA['category'].explode()

# Contar las ocurrencias de cada categoría
conteo_categorias = categorias_expandidas.value_counts()

# Eliminar la serie que ya no se usa
del categorias_expandidas


# In[13]:


conteo_categorias.to_csv('Archivos/categoriasCA.csv')


# ### Explotar columna MISC

# In[14]:


# Función para extraer y expandir los diccionarios en nuevas columnas
def expand_misc_column(misc_dict):
    if pd.isna(misc_dict):
        return pd.Series()
    expanded = {}
    for key, value in misc_dict.items():
        if value is not None and isinstance(value, np.ndarray):
            expanded[key] = ', '.join(value)
        else:
            expanded[key] = value
    return pd.Series(expanded)

# Aplicar la función al DataFrame
expanded_df = df_metadatosCA['MISC'].apply(expand_misc_column)

# Unir el DataFrame original con el DataFrame expandido
df_metadatosCA = pd.concat([df_metadatosCA, expanded_df], axis=1)

#Eliminar la columna MISC que ya no se usa
df_metadatosCA.drop(columns='MISC', inplace=True)

del expanded_df


# ## Exportaciones

# In[15]:


# Elegir ciudad
ciudadelegida='Los Angeles'


# ### Listado de negocios de la ciudad

# In[16]:


#filtro el listado
negocios=df_metadatosCA['gmap_id'][df_metadatosCA['city'] == ciudadelegida]


# In[17]:


#lo exporto a un csv
negocios.to_csv('Archivos/negociosciudad.csv', index=False)


# ### Machine Learning

# In[18]:


# Elegir ciudad
ciudadelegida='Los Angeles'


# In[19]:


# Generar el dataframe a exportar
df_ML = df_metadatosCA.loc[df_metadatosCA['city'] == ciudadelegida, 
                           ['address', 'gmap_id', 'latitude', 'longitude',
                            'category', 'avg_rating', 'num_of_reviews', 'Hours_day', 'Hours_night']]

# Exportar el dataframe
df_ML.to_csv('Archivos/metadatos_ML.csv', index=False)


# ### EDA

# In[20]:


df_metadatosCA['Service options'].value_counts()


# In[21]:


df_metadatosCA.drop(columns=['name', 'description', 'hours', 'state', 'relative_results', 'From the business'], inplace=True)


# In[22]:


#guardo el archivo parquet, para poder importarlo si es necesario
df_metadatosCA.to_parquet('Archivos/metadatosCA.parquet', engine='pyarrow')


# # Reviews Estados - Google

# ## Importar datos

# In[23]:


# IDs de los archivos de Google Drive
file_links = [
    'https://drive.google.com/file/d/13JlGdagtTp4SrUIXu5osayX0f-vmeMz6',
    'https://drive.google.com/file/d/1PIruhKSA5gEwk93-jwKdlG_vtwJmBHWV', 
    'https://drive.google.com/file/d/1JVSi-345m8nt52m2_MPkLULZexbvZUAV', 
    'https://drive.google.com/file/d/1vYYCtcNcfdRzQpEskb8x-8npZUHj2XY-', 
    'https://drive.google.com/file/d/1nCyVnhNpfphd26ye3lj9UsWvPTEhik6b', 
    'https://drive.google.com/file/d/12PR9jUiZLYvjw6BZjwlexgsWmJlMOajN',
    'https://drive.google.com/file/d/1Oq1UdTmQ4xFgkaFdx09JXJQ1_pnIk-il', 
    'https://drive.google.com/file/d/1UwzEftWrssj8Vt0BAf_W9L_TVDGa9JD9', 
    'https://drive.google.com/file/d/1KsXni6or_cPKovgUaRI_3G4-mRXfqgog', 
    'https://drive.google.com/file/d/1fK2kTLDqlUcDt6bKa20W5LvOmrfemDrg', 
    'https://drive.google.com/file/d/1rMz_y1cqa8IBwv1K6K34fAXB2qoRjmEG', 
    'https://drive.google.com/file/d/1t59IfitryIsy8-F9NL9J6M75UElQO0i9',
    'https://drive.google.com/file/d/17VtmF8701j3Tk-tdHeRrXDzj32UyWFVh',
    'https://drive.google.com/file/d/1zoN6XJV220ofRKVlM8DP--FriL_OcZEP',
    'https://drive.google.com/file/d/1HUVCM9uOrXhoOzoSD9NqhHJ1PHrLEhBC',
    'https://drive.google.com/file/d/1sqp0YG4OHVUoA0gWrgwg1wXpdOlF5RfD',
    'https://drive.google.com/file/d/1SPDbJPTxKV1QqMcRNsHIhV7EZBLtRCWf',
    'https://drive.google.com/file/d/1_Ik1uLilfLe0MEb1Gia-t9SpE1Wwdwnm'
]

# Nombres de los archivos locales (presumiendo que siguen el patrón 1.json, 2.json, ..., 11.json)
file_names = [f'ArchivosIgnore/{i}.json' for i in range(1, len(file_links) + 1)]

# Inicializar una lista para almacenar los DataFrames
dataframes = []

# Descargar y leer cada archivo JSON si no está descargado previamente
for file_link, file_name in zip(file_links, file_names):
    try:
        # Verificar si el archivo ya está descargado
        if not os.path.exists(file_name):
            # Obtener el ID del archivo desde el enlace
            file_id = file_link.split('/d/')[1].split('/')[0]
            download_url = f'https://drive.google.com/uc?id={file_id}'
            
            # Descargar el archivo
            gdown.download(download_url, file_name, quiet=False)
            
            # Verificar si el archivo descargado es un JSON válido
            with open(file_name, 'r', encoding='utf-8') as file:
                first_char = file.read(1)
                if not first_char:
                    raise ValueError(f"El archivo {file_name} está vacío.")
                file.seek(0)
            
        # Leer el archivo JSON en un DataFrame
        df = pd.read_json(file_name, lines=True)
        
        # Agregar el DataFrame a la lista
        dataframes.append(df)
    
    except Exception as e:
        print(f"Error al procesar el archivo {file_name}: {e}")


# In[24]:


del df


# In[25]:


# Concatenar todos los DataFrames en uno solo
df_reviewsGoogle = pd.concat(dataframes, ignore_index=True)


# In[26]:


del dataframes


# In[27]:


del file_link
del file_name
del file_names
del file_links
del first_char


# Espacio que ocupan
# Carpeta: 763 Mb (3,8 segundos en importar para una lista, 48,44 segundos para pasarlo a dataframe)
# Dataframe: 164,8 Mb
# CSV: 545 Mbs

# ## Eliminación de duplicados

# In[28]:


df_reviewsGoogle.drop_duplicates(subset=['user_id', 'time', 'gmap_id'], inplace=True)


# ## Columnas

# In[29]:


#si tiene texto
df_reviewsGoogle['has_text'] = df_reviewsGoogle['text'].apply(lambda x: 1 if isinstance(x, str) and len(x.strip()) > 0 else 0)


# In[30]:


#cantidad de fotos
df_reviewsGoogle['num_pics'] = df_reviewsGoogle['pics'].apply(lambda x: len(x) if isinstance(x, list) else 0)


# In[31]:


#si tiene respuesta
df_reviewsGoogle['has_resp'] = df_reviewsGoogle['resp'].apply(lambda x: 1 if isinstance(x, dict) and len(x) > 0 else 0)


# ## Exportaciones

# ### Machine Learning

# In[32]:


#filtro por los negocios de la ciudad
df_reviewsGoogle_ML = df_reviewsGoogle[df_reviewsGoogle['gmap_id'].isin(negocios)][['user_id', 'time', 'rating', 'gmap_id']]


# In[33]:


#esportar a un csv
df_reviewsGoogle_ML.to_csv('Archivos/reviewsGoogle_ML.csv', index=False)


# ### EDA

# In[34]:


#eliminar columnas innecesarias
df_reviewsGoogle.drop(columns=['name', 'text', 'pics', 'resp'], inplace=True)


# In[35]:


#esportar a un parquet
df_reviewsGoogle.to_parquet('ArchivosIgnore/ReviewsGoogle.parquet', engine='pyarrow')


# ### Eliminacion de dfs

# In[36]:


del df_reviewsGoogle
del df_reviewsGoogle_ML


# # Business - YELP

# ## Importar los archivos desde la nube

# In[37]:


# ID del archivo de Google Drive
file_id = '1byFtzpZXopdCN-XYmMHMpZqzgAqfQBBu'

# Construir la URL de descarga
download_url = f'https://drive.google.com/uc?id={file_id}'

# Nombre del archivo local
file_path = 'ArchivosIgnore/business.pkl'

# Verificar si el archivo ya está descargado
if not os.path.exists(file_path):
    try:
        # Descargar el archivo usando gdown
        gdown.download(download_url, file_path, quiet=False)
        print(f"Archivo '{file_path}' descargado correctamente.")

    except Exception as e:
        print(f"Error al descargar el archivo: {e}")

# Cargar el archivo pickle en un DataFrame de pandas si existe
if os.path.exists(file_path):
    try:
        df_business = pd.read_pickle(file_path)
        print(f"Archivo '{file_path}' cargado en el DataFrame correctamente.")

    except Exception as e:
        print(f"Error al cargar el archivo en el DataFrame: {e}")

else:
    print(f"El archivo '{file_path}' no está disponible para cargar en el DataFrame.")


# ## Eliminacion de duplicados

# In[38]:


df_business.columns


# In[39]:


df_business.drop_duplicates(subset=['business_id'], inplace=True)


# ### Elimino columnas duplicadas

# In[40]:


#renombro y saco columnas
df_business.columns=['business_id', 'name', 'address', 'city', 'state', 'postal_code',
       'latitude', 'longitude', 'stars', 'review_count', 'is_open',
       'attributes', 'categories', 'hours', 'business_id2', 'name2', 'address2',
       'city2', 'state2', 'postal_code2', 'latitude2', 'longitude2', 'stars2',
       'review_count2', 'is_open2', 'attributes2', 'categories2', 'hours2']

df_business.drop(columns=['business_id2', 'name2', 'address2',
       'city2', 'state2', 'postal_code2', 'latitude2', 'longitude2', 'stars2',
       'review_count2', 'is_open2', 'attributes2', 'categories2', 'hours2'], inplace=True)


# ## Filtrado por california

# In[41]:


# Luego, aplica el filtro para las empresas en California (por código postal)
df_business_CA = df_business[(df_business['postal_code'] >= '90000') & (df_business['postal_code'] <= '96612')]


# In[42]:


del df_business


# ## Filtrado por Los Angeles 

# In[43]:


df_business_LA = df_business_CA[(df_business_CA['postal_code'] >= '90000') & (df_business_CA['postal_code'] <= '91609')]


# ## Transformación de los Datos 
# 

# In[44]:


# Elimina valores nulos en las columnas attributes y hours
df_business_CA= df_business_CA.dropna(subset=['attributes', 'hours'])

# Modificación del tipo  de datos en las columnas 'latitude','longitud','stars','review_count','is-open'

df_business_CA['latitude'] = pd.to_numeric(df_business_CA['latitude'], errors='coerce')
df_business_CA['longitude'] = pd.to_numeric(df_business_CA['longitude'], errors='coerce')
df_business_CA['stars'] = pd.to_numeric(df_business_CA['stars'], errors='coerce')
df_business_CA['review_count'] = pd.to_numeric(df_business_CA['review_count'], errors='coerce')
df_business_CA['is_open'] = pd.to_numeric(df_business_CA['is_open'], errors='coerce')


# ## Eliminacion de columnas

# In[45]:


df_business_CA.drop(columns=['is_open'], inplace=True)


# In[46]:


#Elimino columnas que no se usan del DF dpara ML
df_business_LA.drop(columns=['state', 'postal_code','is_open','hours'], inplace=True)


# ## Exportación

# In[47]:


#guardo el archivo parquet, para poder importarlo si es necesario
df_business_CA.to_parquet('Archivos/business_CA_Yelp.parquet', engine='pyarrow')


# In[48]:


#csv para ML
df_business_LA.to_csv('Archivos/business_ML.csv', index=False)


# In[49]:


#Listado de negocios de YELP
businessCA=df_business_CA['business_id']


# In[50]:


businessCA.to_csv('Archivos/yelpCA.csv', index=False)


# In[51]:


businessML=df_business_LA['business_id']
businessML.to_csv('Archivos/BusinesslistYELPML.csv', index=False)


# # Review - YELP
# 

# ## Importacion de los datos

# In[55]:


# ID del archivo de Google Drive
file_id = '1mwNNdOMSNty6WumYdH9FJNJZJYQ6oD1c'

# URL de descarga directa desde Google Drive
url = f'https://drive.google.com/uc?id={file_id}'

# Nombre del archivo descargado y ruta de salida
output = 'ArchivosIgnore/data.json'
file_path = output

# Verificar si el archivo ya está descargado
if not os.path.exists(file_path):
    try:
        # Descargar el archivo
        gdown.download(url, output, quiet=False)
        print(f"Archivo '{output}' descargado correctamente.")

    except Exception as e:
        print(f"Error al descargar el archivo: {e}")

# Procesar el archivo JSON en chunks y guardar en un DataFrame final
try:
    # Definir el tamaño del chunk (número de líneas por chunk)
    chunk_size = 1000

    # Lista para almacenar los DataFrames procesados
    results = []

    # Leer el archivo JSON en chunks
    chunks = pd.read_json(file_path, lines=True, chunksize=chunk_size)

    # Procesar cada chunk por separado
    for i, chunk in enumerate(chunks):
        # Ejemplo de procesamiento: mostrar las primeras filas del chunk
        print(f"Procesando chunk {i + 1}")
        print(chunk.head())

        # Guardar resultados intermedios en una lista
        results.append(chunk)

        # Liberar memoria si no necesitas almacenar los chunks completos
        del chunk

    # Combinar todos los chunks procesados en un solo DataFrame final
    final_df = pd.concat(results, ignore_index=True)
    print("Procesamiento completo. DataFrame final creado.")

except Exception as e:
    print(f"Error al procesar el archivo JSON: {e}")


# ## Filtros de dataframe

# In[53]:


businessCA=pd.read_csv('Archivos/yelpCA.csv')
businessML=pd.read_csv('Archivos/businesslistYELPML.csv')


# In[54]:


reviewYELP=final_df[final_df['business_id'].isin(businessCA['business_id'])]


# In[ ]:


reviewYELPML=final_df[final_df['business_id'].isin(businessML['business_id'])]


# In[ ]:


del final_df


# ## Exportaciones

# In[ ]:


reviewYELPML.to_csv('Archivos/ReviewsYELP_ML.csv', index=False)


# In[ ]:


reviewYELP.to_parquet('Archivos/ReviewYELP.parquet', engine='pyarrow')


# # USER - YELP

# ## Importacion de datos

# In[56]:


# ID del archivo de Google Drive
file_id = '1TT4ARRIV6i2fO1b5yb0aSUkjhxMb9u6g'

# URL de descarga directa desde Google Drive
url = f'https://drive.google.com/uc?id={file_id}'

# Nombre del archivo descargado
output = 'user.parquet'

# Verificar si el archivo ya está descargado
if not os.path.exists(output):
    try:
        # Descargar el archivo si no está presente localmente
        gdown.download(url, output, quiet=False)
        print(f"Archivo '{output}' descargado correctamente.")

    except Exception as e:
        print(f"Error al descargar el archivo: {e}")

# Leer el archivo Parquet en un DataFrame si existe
if os.path.exists(output):
    try:
        df = pd.read_parquet(output)
        print(f"Archivo '{output}' cargado en el DataFrame correctamente.")

    except Exception as e:
        print(f"Error al cargar el archivo en el DataFrame: {e}")

else:
    print(f"El archivo '{output}' no está disponible para cargar en el DataFrame.")


# ## Filtro ciudad elegida

# In[ ]:


# se importa el archivo usado
df_rev_YELP_ML=pd.read_csv('Archivos/ReviewsYELP_ML.csv')
#se toman los valores de userid
listado=df_rev_YELP_ML['user_id'].unique()
#eliminar df
del df_rev_YELP_ML


# ## Transformación

# In[ ]:


# Calcular valores nulos y porcentajes
valores_nulos = df.isnull().sum()
# Contar las ocurrencias de cada fila duplicada
duplicate_counts = df[df.duplicated()].sum()


# In[ ]:


# Escribir el DataFrame como un archivo Parquet
filtered_reviews_ca.to_parquet('Archivos/user_ca.parquet', index=False)


# # Carga (LOAD)

# ## Archivos para Machine Learning

# In[ ]:


df_users_ML=df[df['user_id'].isin(listado)]


# In[ ]:


df_users_ML.drop(columns=['compliment_hot',
       'compliment_more', 'compliment_profile', 'compliment_cute',
       'compliment_list', 'compliment_note', 'compliment_plain',
       'compliment_cool', 'compliment_funny', 'compliment_writer',
       'compliment_photos'], inplace=True)


# In[ ]:


df_users_ML.drop_duplicates(inplace=True)


# In[ ]:


df_users_ML.to_csv('Archivos/user_ML.csv', index=False)


# ## Crear ETL local como script de Python

# In[57]:


get_ipython().system('jupyter nbconvert --to script ETL.ipynb')


# ## GCP Bucket
# 

# In[ ]:


get_ipython().run_line_magic('run', 'cloud_up.py')

