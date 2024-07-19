## Documentación Completa del Script ETL para FindEden: Análisis de Reseñas y Metadatos de Google para Locales en Los Ángeles

**1. Objetivo y Descripción General**

Este script de Python realiza un proceso ETL (Extracción, Transformación, Carga) para analizar reseñas y metadatos de locales en Los Ángeles obtenidos de Google. El objetivo principal es crear una base de datos enriquecida que permita evaluar la calidad de los locales y la confiabilidad de las reseñas de los usuarios, con un enfoque especial en el análisis de reseñas y metadatos de Google.

**2. Estructura del Script**

El script está organizado en las siguientes secciones principales:

*   **Instalación de Paquetes:** Asegura que las librerías necesarias estén instaladas.
*   **Extracción de Datos:**
    *   Descarga metadatos de locales desde Google Drive.
    *   Descarga reseñas de usuarios desde Google Drive.
*   **Transformación de Datos:**
    *   Limpieza y preprocesamiento de metadatos (eliminación de duplicados, extracción de ciudades, cálculo de horas de apertura, categorización, etc.).
    *   Limpieza y preprocesamiento de reseñas (eliminación de duplicados, identificación de reseñas con texto, fotos y respuestas, etc.).
    *   Aplicación de técnicas de Machine Learning para categorizar locales y evaluar la confiabilidad de los usuarios.
*   **Carga de Datos:**
    *   Carga de los datos transformados en una base de datos MySQL local.
    *   Carga de los datos transformados en Google Cloud BigQuery.
*   **Generación de Datos de Prueba:**
    *   Creación de nuevas entradas de prueba en los archivos de datos.
*   **Automatización:**
    *   Conversión del cuaderno Jupyter a un script de Python ejecutable.
    *   Generación del archivo `requirements.txt` para facilitar la instalación de dependencias.

**3. Funcionalidades Detalladas**

*   **Extracción y Limpieza de Metadatos:**
    *   Descarga archivos JSON con metadatos desde Google Drive utilizando `gdown`:

```python
# IDs de los archivos de Google Drive
file_links = [
    'https://drive.google.com/file/d/1OnyhmyG8xzdn4XU9LYcnwzBseB1_rChS', 
    # ... otros enlaces ...
]

# ... (Código para descargar y procesar los archivos JSON)
```
    *   Elimina duplicados y filtra por el estado de California:
```python
df_metadatosCA.drop_duplicates(subset=['gmap_id'], inplace=True)

df_metadatosCA['estado'] = df_metadatosCA['address'].str.extract(r', ([A-Z]{2}) \d{5}')
df_metadatosCA = df_metadatosCA[df_metadatosCA['estado'] == 'CA']
```
    *   Extrae información relevante como ciudad, horas de apertura diurna y nocturna, categorías de negocio, etc.:
```python
# Función para extraer la ciudad
def extract_city(address):
    match = re.search(r',\s*([^,]+),\s*[A-Z]{2}\s*\d{5}', address)
    if match:
        return match.group(1).strip()
    return None
```
    *   Aplica técnicas de Machine Learning para categorizar los locales en categorías generales (Auto, Belleza, Ropa, etc.) y específicas (tipos de restaurantes, religiones, etc.).
```python
def generalize_category(category):
    auto_keywords = ["auto", "car", "gas station", "parking", "vehicle", "tire"]
    # ... (Otras categorías y palabras clave)

    if isinstance(category, str):
        category_lower = category.lower()
        if any(keyword in category_lower for keyword in auto_keywords):
            return "Auto"
        # ... (Otras condiciones para las demás categorías)
```

*   **Extracción y Limpieza de Reseñas:**
    *   Descarga archivos JSON con reseñas desde Google Drive.
    *   Elimina duplicados y filtra por los locales de interés.

```python
#filtro por los negocios de la ciudad
df_reviewsGoogle_ML = df_reviewsGoogle[df_reviewsGoogle['gmap_id'].isin(negocios)][['user_id', 'time', 'rating', 'gmap_id']]
```

    *   Identifica reseñas con texto, fotos y respuestas.
    *   Calcula estadísticas de los usuarios (cantidad de reseñas, diferencia promedio con la calificación del local, etc.).
    *   Aplica técnicas de Machine Learning para ponderar la confiabilidad de los usuarios.

```python
# Calcular la cantidad de reseñas por user_id
reviews_count = df_reviewsGoogle['user_id'].value_counts()

# Filtrar los usuarios con más de 7 reseñas
filtered_reviews_count = reviews_count[reviews_count > 3]
```

*   **Cálculo de Calificaciones Ponderadas:**
    *   Combina metadatos y reseñas para calcular una calificación promedio ponderada para cada local, teniendo en cuenta la confiabilidad de los usuarios.

```python
# Realizar el merge para añadir user_rating a df_reviewsGoogle_filtered
df_reviewsGoogle_filtered = df_reviewsGoogle_filtered.merge(df_user_stats_filtered[['user_id', 'user_rating']], on='user_id', how='left')
```

*   **Carga en Bases de Datos:**
    *   Carga incremental de los datos en una base de datos MySQL local, evitando duplicados y actualizando solo los datos nuevos.
    *   Carga incremental de los datos en Google Cloud BigQuery, siguiendo la misma lógica.

```python
get_ipython().run_line_magic('run', 'scripts/carga_incremental_sql.py')
get_ipython().run_line_magic('run', 'scripts/carga_incremental_gcp.py')
```

**4. Consideraciones Adicionales**

*   El script utiliza expresiones regulares para extraer información de las direcciones y categorías de los locales.
*   Se aplican técnicas de Machine Learning para categorizar locales y evaluar la confiabilidad de los usuarios, aunque los detalles específicos de los modelos no están incluidos en este código.
*   La carga incremental en las bases de datos asegura la eficiencia y evita la duplicación de datos.

**5. Ejecución del Script**

El script se puede ejecutar desde la línea de comandos utilizando:

```bash
python ETL.py
```

Asegúrate de tener todas las dependencias listadas en `requirements.txt` instaladas antes de ejecutar el script.
