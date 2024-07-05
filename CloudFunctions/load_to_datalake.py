import os
import gdown
from google.cloud import storage

def download_and_upload_file(event, context):
    """Cloud Function triggered by changes in Google Drive.

    Args:
        event (dict): The Cloud Functions event payload.
        context (google.cloud.functions.Context): Metadata for the event.
    """

    file_links = [ 
        # ... (Tu lista de enlaces de archivos de Google Drive)
    ]

    bucket_name = "your_bucket_name"  # Reemplaza con el nombre de tu bucket
    storage_client = storage.Client(project="findeden")
    bucket = storage_client.bucket(bucket_name)

    for file_link in file_links:
        try:
            file_id = file_link.split('/d/')[1].split('/')[0]
            download_url = f'https://drive.google.com/uc?id={file_id}'
            file_name = file_link.split('/')[-1]  # Extraer el nombre del archivo
            
            temp_file_path = f'/tmp/{file_name}'

            # Descargar el archivo a un directorio temporal en Cloud Functions
            gdown.download(download_url, temp_file_path, quiet=False)

            # Subir el archivo al bucket de Cloud Storage
            blob = bucket.blob(file_name)
            blob.upload_from_filename(temp_file_path)

            print(f"Archivo {file_name} descargado y subido a Cloud Storage.")

        except Exception as e:
            print(f"Error al procesar el archivo {file_name}: {e}")

        finally:
            # Limpiar el archivo temporal
            if os.path.exists(temp_file_path):
                os.remove(temp_file_path)
