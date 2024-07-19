## Función: `cargar_csv_a_bigquery_incremental`

**Descripción:**

Esta función automatiza la carga incremental de archivos CSV a BigQuery. Solo los registros nuevos, identificados por una fecha posterior a la última registrada en la tabla de BigQuery, son añadidos. Si el conjunto de datos (dataset) o la tabla no existen, se crean automáticamente.

**Código:**

```python
from google.cloud import bigquery
import pandas as pd

def cargar_csv_a_bigquery_incremental(nombre_archivo, ruta_archivo, nombre_tabla=None, nombre_dataset='findeden',
                                      esquema=None, campo_fecha='fecha'):
    """Carga un CSV a BigQuery de forma incremental.

    Args:
        nombre_archivo: Nombre del archivo CSV.
        ruta_archivo: Ruta completa al archivo CSV.
        nombre_tabla: (Opcional) Nombre de la tabla. Si no se proporciona, se usará el nombre del archivo sin extensión.
        nombre_dataset: Nombre del dataset (por defecto 'mi_dataset').
        esquema: (Opcional) Esquema de la tabla (lista de diccionarios).
        campo_fecha: Nombre del campo que contiene la fecha (por defecto 'fecha').
    """

    client = bigquery.Client.from_service_account_json('gcp.json')

    # Crear dataset si no existe
    dataset_id = f"{client.project}.{nombre_dataset}"
    try:
        client.get_dataset(dataset_id)
    except:
        dataset = bigquery.Dataset(dataset_id)
        client.create_dataset(dataset)
        print(f"Dataset {nombre_dataset} creado.")

    # Usar el nombre del archivo sin extensión como nombre de tabla si no se proporciona
    if nombre_tabla is None:
        nombre_tabla = nombre_archivo.split('.')[0]

    tabla_id = f"{dataset_id}.{nombre_tabla}"

    # Leer el CSV en un DataFrame y convertir la columna de fecha
    df = pd.read_csv(ruta_archivo)
    df[campo_fecha] = pd.to_datetime(df[campo_fecha], format='%Y-%m-%d')  # Ajusta el formato si es necesario

    # Obtener la fecha más reciente en BigQuery (si la tabla existe)
    fecha_nube = None
    try:
        query = f"SELECT MAX({campo_fecha}) AS max_fecha FROM `{tabla_id}`"
        job = client.query(query)
        for row in job:
            fecha_nube = row['max_fecha']
    except:
        pass  # La tabla no existe aún

    print(f"Tabla: {tabla_id}")
    print(f"Fecha más reciente en la nube: {fecha_nube}")

    # Filtrar el DataFrame para cargar solo datos nuevos
    if fecha_nube:
        df_nuevos = df[df[campo_fecha] > fecha_nube]
    else:
        df_nuevos = df  # Cargar todo si la tabla está vacía

    print(f"Fecha más reciente en el repositorio local: {df[campo_fecha].max()}")
    
    # Cargar solo si hay datos nuevos
    if not df_nuevos.empty:
        job_config = bigquery.LoadJobConfig(
            source_format=bigquery.SourceFormat.CSV,
            skip_leading_rows=1,
            autodetect=True if esquema is None else False,
            schema=esquema,
            write_disposition=bigquery.WriteDisposition.WRITE_APPEND,  # Siempre agregar en incremental
        )

        job = client.load_table_from_dataframe(df_nuevos, tabla_id, job_config=job_config)
        job.result()

        print(f"Se subieron {len(df_nuevos)} filas nuevas.")
    else:
        print("No hay datos nuevos para subir.")

# ... (llamadas a la función con tus archivos) 


# Llamada a la función para subir tus archivos (ajusta las rutas y campos según tus necesidades)
cargar_csv_a_bigquery_incremental('metadatos_ML.csv', './Archivos/metadatos_ML.csv')
cargar_csv_a_bigquery_incremental('reviewsGoogle_ML.csv', './Archivos/reviewsGoogle_ML.csv')
cargar_csv_a_bigquery_incremental('locales_LA.csv', './Archivos/locales_LA.csv')
cargar_csv_a_bigquery_incremental('reviews_LA.csv', './Archivos/reviews_LA.csv')

# Archivos Inmobiliaria:
cargar_csv_a_bigquery_incremental('Contratos.csv', './datasets/SQL/Contratos.csv')
cargar_csv_a_bigquery_incremental('Inquilinos.csv', './datasets/SQL/Inquilinos.csv')
cargar_csv_a_bigquery_incremental('Propiedades.csv', './datasets/SQL/Propiedades.csv')
cargar_csv_a_bigquery_incremental('Publicaciones_Alquileres.csv', './datasets/SQL/Publicaciones_Alquileres.csv')

```

**Explicación detallada:**

**1. Importación de Bibliotecas**

```python
from google.cloud import bigquery
import pandas as pd
```

* `google.cloud.bigquery`: Proporciona las herramientas para interactuar con BigQuery.
* `pandas`: Facilita la lectura y manipulación de datos en formato CSV.


**2. Definición de la Función `cargar_csv_a_bigquery_incremental`**

```python
def cargar_csv_a_bigquery_incremental(nombre_archivo, ruta_archivo, nombre_tabla=None, nombre_dataset='findeden',
                                      esquema=None, campo_fecha='fecha'):
   # ... (código de la función)
```
Esta función es el núcleo del proceso de carga incremental. Recibe los siguientes argumentos:

* `nombre_archivo`: Nombre del archivo CSV a cargar.
* `ruta_archivo`: Ruta completa del archivo CSV.
* `nombre_tabla`: Nombre de la tabla en BigQuery (opcional). Si no se proporciona, se usará el nombre del archivo sin extensión.
* `nombre_dataset`: Nombre del conjunto de datos en BigQuery (por defecto 'findeden').
* `esquema`: Esquema de la tabla (opcional). Si no se proporciona, se inferirá automáticamente.
* `campo_fecha`: Nombre del campo que contiene la fecha en el CSV (por defecto 'fecha').

**3. Conexión a BigQuery y Creación del Dataset**

```python
client = bigquery.Client.from_service_account_json('gcp.json')

# Crear dataset si no existe
dataset_id = f"{client.project}.{nombre_dataset}"
try:
    client.get_dataset(dataset_id)
except:
    dataset = bigquery.Dataset(dataset_id)
    client.create_dataset(dataset)
    print(f"Dataset {nombre_dataset} creado.")
```
* Se establece una conexión con BigQuery utilizando las credenciales del archivo `gcp.json`.
* Se verifica si el dataset especificado existe. Si no existe, se crea uno nuevo.

**4. Lectura del CSV y Conversión de Fecha**

```python
df = pd.read_csv(ruta_archivo)
df[campo_fecha] = pd.to_datetime(df[campo_fecha], format='%Y-%m-%d')  # Ajusta el formato si es necesario
```
* Se lee el archivo CSV en un DataFrame de Pandas (`df`).
* Se convierte la columna de fecha especificada (`campo_fecha`) al tipo de dato datetime para facilitar las comparaciones.

**5. Obtención de la Fecha Más Reciente en BigQuery**

```python
fecha_nube = None
try:
    query = f"SELECT MAX({campo_fecha}) AS max_fecha FROM `{tabla_id}`"
    job = client.query(query)
    for row in job:
        fecha_nube = row['max_fecha']
except:
    pass  # La tabla no existe aún
```
* Se intenta obtener la fecha más reciente presente en la tabla de BigQuery. Si la tabla no existe, se ignora el error y `fecha_nube` se mantiene como `None`.

**6. Filtrado de Datos Nuevos**

```python
if fecha_nube:
    df_nuevos = df[df[campo_fecha] > fecha_nube]
else:
    df_nuevos = df  # Cargar todo si la tabla está vacía
```
* Si se encontró una fecha en BigQuery, se filtran los datos del DataFrame para incluir solo las filas cuya fecha es posterior a la fecha más reciente en la nube.
* Si la tabla está vacía en BigQuery, se seleccionan todos los datos del DataFrame para cargarlos.

**7. Carga de Datos Nuevos a BigQuery**

```python
if not df_nuevos.empty:
    job_config = bigquery.LoadJobConfig(
        source_format=bigquery.SourceFormat.CSV,
        skip_leading_rows=1,
        autodetect=True if esquema is None else False,
        schema=esquema,
        write_disposition=bigquery.WriteDisposition.WRITE_APPEND, 
    )

    job = client.load_table_from_dataframe(df_nuevos, tabla_id, job_config=job_config)
    job.result()

    print(f"Se subieron {len(df_nuevos)} filas nuevas.")
else:
    print("No hay datos nuevos para subir.")
```
* Se verifica si hay datos nuevos para cargar (`df_nuevos` no está vacío).
* Si hay datos nuevos:
    * Se configura un trabajo de carga en BigQuery (`job_config`).
    * Se carga el DataFrame filtrado (`df_nuevos`) a la tabla especificada en BigQuery.
    * Se imprime un mensaje indicando cuántas filas se cargaron.
* Si no hay datos nuevos, se imprime un mensaje correspondiente.


**Llamadas a la función**

```python
# ... (llamadas a la función con tus archivos) 
```
Finalmente, se llama a la función `cargar_csv_a_bigquery_incremental` para cada archivo CSV que se desea cargar, proporcionando los argumentos necesarios.