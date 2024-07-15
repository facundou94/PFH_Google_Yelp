from google.cloud import storage

def subir_archivo_gcs(nombre_archivo, ruta_archivo, nombre_bucket="findeden"):
    """Sube un archivo a un bucket de Google Cloud Storage.

    Args:
        nombre_archivo: Nombre del archivo en el bucket (con extensión).
        ruta_archivo: Ruta completa al archivo en tu sistema local.
        nombre_bucket: Nombre del bucket de destino (por defecto "findeden").
    """
    try:
        storage_client = storage.Client.from_service_account_json('LocalFunctions/gcp.json')
        bucket = storage_client.bucket(nombre_bucket)
        blob = bucket.blob(nombre_archivo)

        # Aumentamos el timeout a 10 minutos para archivos grandes o conexiones lentas
        blob.upload_from_filename(ruta_archivo, timeout=600) 
        
        print(f"Archivo {nombre_archivo} subido a {nombre_bucket} exitosamente.")
    except Exception as e:
        print(f"Error al subir el archivo: {e}")

# Llamada a la función para subir tu archivo
subir_archivo_gcs('metadatosCA.parquet', './Archivos/metadatosCA.parquet')  # Asumiendo que el archivo está en el mismo directorio que el script
