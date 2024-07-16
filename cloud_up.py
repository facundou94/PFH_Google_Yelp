from google.cloud import bigquery

def cargar_csv_a_bigquery_incremental(nombre_archivo, ruta_archivo, nombre_tabla=None, nombre_dataset='findeden', 
                                      esquema=None, campo_clave=None):
    """Carga un CSV a BigQuery, creando dataset y tabla si no existen.

    Args:
        nombre_archivo: Nombre del archivo CSV.
        ruta_archivo: Ruta completa al archivo CSV.
        nombre_tabla: (Opcional) Nombre de la tabla. Si no se proporciona, se usará el nombre del archivo sin extensión.
        nombre_dataset: Nombre del dataset (por defecto 'mi_dataset').
        esquema: (Opcional) Esquema de la tabla (lista de diccionarios).
        campo_clave: (Opcional) Nombre del campo clave para la carga incremental.
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

    job_config = bigquery.LoadJobConfig(
        source_format=bigquery.SourceFormat.CSV,
        skip_leading_rows=1,  # Ignorar la primera fila si contiene encabezados
        autodetect=True if esquema is None else False,  # Autodetectar el esquema si no se proporciona
        schema=esquema,
        write_disposition=bigquery.WriteDisposition.WRITE_APPEND if campo_clave else bigquery.WriteDisposition.WRITE_TRUNCATE,
    )

    if campo_clave:
        job_config.schema_update_options = [bigquery.SchemaUpdateOption.ALLOW_FIELD_ADDITION]
        job_config.time_partitioning = bigquery.TimePartitioning(
            type_=bigquery.TimePartitioningType.DAY,
            field=campo_clave,  # Particionar por el campo clave
        )

    with open(ruta_archivo, "rb") as source_file:
        load_job = client.load_table_from_file(source_file, tabla_id, job_config=job_config)

    load_job.result()  # Esperar a que el trabajo termine

    print(f"Archivo {nombre_archivo} cargado en la tabla {tabla_id}")

# Llamada a la función para subir tu archivo
cargar_csv_a_bigquery_incremental('metadatos_ML.csv', './Archivos/metadatos_ML.csv')  # Asumiendo que el archivo está en el mismo directorio que el script
cargar_csv_a_bigquery_incremental('reviewsGoogle_ML.csv', './Archivos/reviewsGoogle_ML.csv')  # Asumiendo que el archivo está en el mismo directorio que el script
cargar_csv_a_bigquery_incremental('locales_LA.csv', './Archivos/locales_LA.csv')  # Asumiendo que el archivo está en el mismo directorio que el script
cargar_csv_a_bigquery_incremental('reviews_LA.csv', './Archivos/reviews_LA.csv')  # Asumiendo que el archivo está en el mismo directorio que el script
