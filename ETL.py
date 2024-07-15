#!/usr/bin/env python
# coding: utf-8

# # Función para instalar/actualizar paquetes

# In[1]:


# Ejecutar la función para instalar/actualizar paquetes
get_ipython().run_line_magic('run', 'LocalFunctions/install_or_update_packages.py')


# # Importación Librerías

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


# # Extracción

# ## Descarga de Archivos

# ### 1 - Metadata - Google

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

# Crear la carpeta MetadataGoogle si no existe
output_dir = 'datasets/MetadataGoogle'
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


# #### Filtrar por Estado California

# Este código combina varios DataFrames, filtra los datos por el estado de California y luego limpia el DataFrame resultante para que tenga un índice continuo y no tenga la columna de índice antigua.

# In[4]:


# Concatenar todos los DataFrames en uno solo
if dataframes:
    df_metadataGoogle = pd.concat(dataframes, ignore_index=True)

    # Filtrar por el estado de California (CA)
    df_metadataGoogle['estado'] = df_metadataGoogle['address'].str.extract(r', ([A-Z]{2}) \d{5}')
    df_metadatosCA = df_metadataGoogle[df_metadataGoogle['estado'] == 'CA']

    # Eliminar el DataFrame original para liberar memoria
    del df_metadataGoogle

    # Resetear índice y eliminar la columna de índice antigua
    df_metadatosCA.reset_index(inplace=True)
    df_metadatosCA.drop('index', axis='columns', inplace=True)


# #### a - Eliminar duplicados

# In[5]:


df_metadatosCA.drop_duplicates(subset=['gmap_id'], inplace=True)


# In[6]:


# Guardar el DataFrame filtrado en un archivo CSV
output_csv_path = os.path.join(output_dir, 'MetadataGoogle.csv')
df_metadatosCA.to_csv(output_csv_path, index=False)

# Eliminar DataFrames de la memoria
del dataframes


# #### b - Extraer Ciudad

# Este código de Python está diseñado para extraer la ciudad de una columna de direcciones en un DataFrame de Pandas llamado df_metadatosCA.
# 
# Este código toma un DataFrame con direcciones y crea una nueva columna que contiene los nombres de las ciudades extraídas. Se basa en una expresión regular para identificar y extraer el nombre de la ciudad según un formato de dirección común.

# In[7]:


# Función para extraer la ciudad y colocarla en una nueva columna
def extract_city(address):
    match = re.search(r',\s*([^,]+),\s*[A-Z]{2}\s*\d{5}', address)
    if match:
        return match.group(1).strip()
    return None

# Aplicar la función a la columna 'address' y crear la columna 'city'
df_metadatosCA['city'] = df_metadatosCA['address'].apply(extract_city)


# #### c - Horas de Atención

# Este script de Python está diseñado para analizar horarios de apertura y cierre de negocios y calcular las horas diurnas y nocturnas que están abiertos. 
# 
# Estas líneas usan la función apply para aplicar las funciones calculate_day_hours y calculate_night_hours a cada fila de la columna "hours" del DataFrame df_metadatosCA. El resultado de cada función se guarda en una nueva columna con el nombre correspondiente.
# 
# 

# In[8]:


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


# In[9]:


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


# In[10]:


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


# In[11]:


# Aplicar las funciones al DataFrame
df_metadatosCA['Hours_day'] = df_metadatosCA['hours'].apply(calculate_day_hours)
df_metadatosCA['Hours_night'] = df_metadatosCA['hours'].apply(calculate_night_hours)


# #### d - Contabilizar Categorías

# Este código de Python está diseñado para analizar las categorías de negocios en un DataFrame llamado df_metadatosCA y contar cuántas veces aparece cada categoría. 

# In[12]:


df_metadatosCA.head(5)


# In[13]:


# Expandir las listas en filas individuales
categorias_expandidas = df_metadatosCA['category'].explode()

# Contar las ocurrencias de cada categoría
conteo_categorias = categorias_expandidas.value_counts()

categorias_expandidas


# In[14]:


num_categorias = len(conteo_categorias)
print(f"La Serie tiene {num_categorias} categorías únicas.")


# In[15]:


# Eliminar la serie que ya no se usa
del categorias_expandidas


# #### e -Explotar la columna MISC

#  Este código de Python está diseñado para tomar un DataFrame llamado df_metadatosCA que tiene una columna llamada 'MISC' que contiene diccionarios, y expandir esos diccionarios en nuevas columnas en el DataFrame.

# In[16]:


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


# In[17]:


df_metadatosCA.head(3)


# In[18]:


# Verifica si la carpeta 'Archivos' existe, si no, la crea
if not os.path.exists('Archivos'):
    os.makedirs('Archivos')

# Guarda el DataFrame en un archivo CSV en la carpeta 'Archivos'
conteo_categorias.to_csv('Archivos/categoriasCA.csv')


# ### 2 - Reviews Estados - Google

# In[19]:


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

# Nombre de la carpeta que quieres crear
carpeta_destino = 'datasets/ReviewsEstadosGoogle'

# Verificar si la carpeta existe
if not os.path.exists(carpeta_destino):
    # Crear la carpeta si no existe
    os.makedirs(carpeta_destino)
    print(f"Se ha creado la carpeta: {carpeta_destino}")
else:
    print(f"La carpeta {carpeta_destino} ya existe.")
    
# Nombres de los archivos locales (presumiendo que siguen el patrón 1.json, 2.json, ..., 11.json)
file_names = [f'datasets/ReviewsEstadosGoogle/{i}.json' for i in range(1, len(file_links) + 1)]

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

del df

# Concatenar todos los DataFrames en uno solo
df_reviewsGoogle = pd.concat(dataframes, ignore_index=True)


# #### a - Eliminación de duplicados

#  Este código elimina las filas duplicadas del DataFrame df_reviewsGoogle solo si las filas tienen los mismos valores en las columnas 'user_id', 'time' y 'gmap_id'. Esto es útil para asegurar que cada combinación única de estas tres columnas represente una reseña única.

# In[20]:


df_reviewsGoogle.drop_duplicates(subset=['user_id', 'time', 'gmap_id'], inplace=True)


# #### b - Tratamiento de Variables

# Este código crea una nueva columna 'has_text' en el DataFrame df_reviewsGoogle. Esta columna tendrá un valor de 1 si la columna 'text' contiene texto real (no está vacía o solo espacios en blanco) y 0 si no contiene texto real.

# In[21]:


# Si contiene texto
df_reviewsGoogle['has_text'] = df_reviewsGoogle['text'].apply(lambda x: 1 if isinstance(x, str) and len(x.strip()) > 0 else 0)


# Este código crea una nueva columna 'num_pics' en el DataFrame df_reviewsGoogle. Esta columna tendrá un valor que representa la cantidad de elementos en la lista que se encuentra en la columna 'pics' para cada fila. Si la columna 'pics' no contiene una lista, la columna 'num_pics' tendrá un valor de 0.

# In[22]:


# Cantidad de fotos
df_reviewsGoogle['num_pics'] = df_reviewsGoogle['pics'].apply(lambda x: len(x) if isinstance(x, list) else 0)


# Este código crea una nueva columna 'has_resp' en el DataFrame df_reviewsGoogle. Esta columna tendrá un valor de 1 si la columna 'resp' contiene un diccionario no vacío y 0 si no lo contiene.

# In[23]:


# Si tiene respuesta
df_reviewsGoogle['has_resp'] = df_reviewsGoogle['resp'].apply(lambda x: 1 if isinstance(x, dict) and len(x) > 0 else 0)


# In[24]:


df_reviewsGoogle


# #### c - Machine Learning

# El código filtra el conjunto de datos df_reviewsGoogle para obtener solo las reseñas que corresponden a los negocios que están en la lista "negocios". Luego, crea un nuevo conjunto de datos llamado df_reviewsGoogle_ML que contiene solo las columnas "user_id", "time", "rating" y "gmap_id" de las reseñas filtradas.
# 
# ¿Para qué se utiliza este código?
# 
# Este código parece ser un paso inicial para preparar los datos para un modelo de Machine Learning. Al filtrar las reseñas de los negocios que te interesan, estás creando un conjunto de datos específico que puedes usar para entrenar un modelo que prediga algo relacionado con las reseñas, como la calificación promedio de un negocio o la probabilidad de que un usuario deje una reseña positiva.

# In[25]:


#filtro por los negocios de la ciudad
#df_reviewsGoogle_ML = df_reviewsGoogle[df_reviewsGoogle['gmap_id'].isin(negocios)][['user_id', 'time', 'rating', 'gmap_id']]


# In[26]:


#filtro por los negocios de la ciudad
#df_reviewsGoogle_ML = df_reviewsGoogle[df_reviewsGoogle['gmap_id'].isin(negocios)][['user_id', 'time', 'rating', 'gmap_id']]


# ### 3 - Business - Google YELP

# #### Importar los archivos desde la nube:

# In[27]:


# ID del archivo de Google Drive
file_id = '1byFtzpZXopdCN-XYmMHMpZqzgAqfQBBu'

# Construir la URL de descarga
download_url = f'https://drive.google.com/uc?id={file_id}'

# Nombre de la carpeta que quieres crear
carpeta_destino = 'datasets/BusinessYelp'

# Verificar si la carpeta existe
if not os.path.exists(carpeta_destino):
    # Crear la carpeta si no existe
    os.makedirs(carpeta_destino)
    print(f"Se ha creado la carpeta: {carpeta_destino}")
else:
    print(f"La carpeta {carpeta_destino} ya existe.")

# Nombre del archivo local
file_path = "datasets/BusinessYelp/business.pkl"

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


# #### a Eliminar columnas Duplicadas

# In[28]:


# Supongamos que tienes un DataFrame llamado df_business
columnas_ordenadas = df_business.columns.sort_values()  # Ordenamos alfabéticamente

# Creamos un DataFrame auxiliar para mostrar en formato de tabla
df_tabla = pd.DataFrame({'Columnas': columnas_ordenadas})

# Mostramos el DataFrame en formato de tabla
display(df_tabla)


# Este código elimina todas las columnas duplicadas excepto la primera aparición.

# In[29]:


# Ejecutamos la eliminación en un DataFrame llamado df_business
df_business = df_business.loc[:, ~df_business.columns.duplicated()]


# In[30]:


# Supongamos que tienes un DataFrame llamado df_business
columnas_ordenadas = df_business.columns.sort_values()  # Ordenamos alfabéticamente

# Creamos un DataFrame auxiliar para mostrar en formato de tabla
df_tabla = pd.DataFrame({'Columnas': columnas_ordenadas})

# Mostramos el DataFrame en formato de tabla
display(df_tabla)


# #### b - Eliminación de Duplicados

# In[31]:


df_business.drop_duplicates(subset=['business_id'], inplace=True)


# #### c - Filtrar por Estado de California

# In[32]:


# Luego, aplica el filtro para las empresas en California (por código postal)
df_business_CA = df_business[(df_business['postal_code'] >= '90000') & (df_business['postal_code'] <= '96612')]


# In[33]:


del df_business


# #### d - Filtrar por Ciudad de Los Angeles

# In[34]:


df_business_LA = df_business_CA[(df_business_CA['postal_code'] >= '90000') & (df_business_CA['postal_code'] <= '91609')]


# #### e - Eliminación de columnas

# In[35]:


#Elimino columnas que no se usan del DF dpara ML
df_business_LA.drop(columns=['state', 'postal_code','is_open','hours', 'is_open'], inplace=True)


# #### f - Exportamos archivos según sea necesario:

# In[36]:


#guardo el archivo parquet, para poder importarlo si es necesario
df_business_CA.to_parquet('Archivos/business_CA_Yelp.parquet', engine='pyarrow')


# In[37]:


#csv para ML
df_business_LA.to_csv('Archivos/business_ML.csv', index=False)


# In[38]:


#Listado de negocios de YELP
businessCA=df_business_CA['business_id']


# In[39]:


businessCA.to_csv('Archivos/yelpCA.csv', index=False)


# In[40]:


businessML=df_business_LA['business_id']
businessML.to_csv('Archivos/BusinesslistYELPML.csv', index=False)


# ### 4 - Reviews Google YELP

# #### Importamos los datos:

# In[41]:


# ID del archivo de Google Drive
file_id = '1mwNNdOMSNty6WumYdH9FJNJZJYQ6oD1c'

# URL de descarga directa desde Google Drive
url = f'https://drive.google.com/uc?id={file_id}'

# Nombre de la carpeta que quieres crear
carpeta_destino = 'datasets/ReviewYelp'

# Verificar si la carpeta existe
if not os.path.exists(carpeta_destino):
    # Crear la carpeta si no existe
    os.makedirs(carpeta_destino)
    print(f"Se ha creado la carpeta: {carpeta_destino}")
else:
    print(f"La carpeta {carpeta_destino} ya existe.")

# Nombre del archivo descargado y ruta de salida
output = 'datasets/ReviewYelp/ReviewYelp.json'
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


# #### a - Filtramos al dataframe:

# In[42]:


businessCA=pd.read_csv('Archivos/yelpCA.csv')
businessML=pd.read_csv('Archivos/businesslistYELPML.csv')


# In[43]:


reviewYELP=final_df[final_df['business_id'].isin(businessCA['business_id'])]


# In[44]:


reviewYELPML=final_df[final_df['business_id'].isin(businessML['business_id'])]


# In[45]:


del final_df


# #### b - Exportamos los archivos:

# In[46]:


reviewYELPML.to_csv('Archivos/ReviewsYELP_ML.csv', index=False)


# In[47]:


reviewYELP.to_parquet('Archivos/ReviewYELP.parquet', engine='pyarrow')


# ### 5 - Users Google YELP

# Importamos la información:

# In[48]:


# ID del archivo de Google Drive
file_id = '1TT4ARRIV6i2fO1b5yb0aSUkjhxMb9u6g'

# URL de descarga directa desde Google Drive
url = f'https://drive.google.com/uc?id={file_id}'

# Nombre de la carpeta que quieres crear
carpeta_destino = 'datasets/UserYelp'

# Verificar si la carpeta existe
if not os.path.exists(carpeta_destino):
    # Crear la carpeta si no existe
    os.makedirs(carpeta_destino)
    print(f"Se ha creado la carpeta: {carpeta_destino}")
else:
    print(f"La carpeta {carpeta_destino} ya existe.")

# Nombre del archivo descargado
output = 'UserYelp/UserYelp.parquet'

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


# #### a -Filtramos por ciudad elegida:

# In[49]:


# se importa el archivo usado
df_rev_YELP_ML=pd.read_csv('Archivos/ReviewsYELP_ML.csv')

#se toman los valores de userid
listado=df_rev_YELP_ML['user_id'].unique()

#eliminar df
del df_rev_YELP_ML


# ## Carga (LOAD)

# ### 1 - Archivos para ML

# In[50]:


df_users_ML=df[df['user_id'].isin(listado)]


# In[51]:


df_users_ML.drop(columns=['compliment_hot',
       'compliment_more', 'compliment_profile', 'compliment_cute',
       'compliment_list', 'compliment_note', 'compliment_plain',
       'compliment_cool', 'compliment_funny', 'compliment_writer',
       'compliment_photos'], inplace=True)


# In[ ]:


df_users_ML.drop_duplicates(inplace=True)


# In[ ]:


df_users_ML.to_csv('Archivos/user_ML.csv', index=False)


# ## 2 - Crear ETL local como script de Python

# In[ ]:


get_ipython().system('jupyter nbconvert --to script ETL.ipynb')


# ## 3 - Cargamos la Información a GCP Bucket
# 

# In[ ]:


get_ipython().run_line_magic('run', 'CloudFunctions/cloud_up.py')


# In[ ]:


# Generar el archivo requirements.txt al final del script
get_ipython().run_line_magic('run', 'LocalFunctions/generate_requirements_file.py')

