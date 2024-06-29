# Data Wherehouse en GCP

## 1 - Crear un Bucket en GCP

En Google Cloud Platform (GCP), un bucket es un contenedor fundamental de almacenamiento de objetos. Es similar a una carpeta en tu computadora, pero en lugar de almacenar archivos localmente, los objetos (que pueden ser archivos, imágenes, videos, etc.) se almacenan en la nube de Google.

Para hacerlo, primeramente debemos crear un nuevo proyecto en el cual trabajar o en caso contrario seleccionar el que deseamos:

![NO SE PUEDE MOSTRAR](Imagenes/Docs_cloud_img/1.png)

Luego, seleccionamos en el menú desplegable de la izquierda la opción Cloud Storage, y luego Buckets:

![NO SE PUEDE MOSTRAR](Imagenes/Docs_cloud_img/2.png)

Nos daremos cuenta que no tendremos ningún Bocket (1) y por ende vamos a crear uno (2):

![NO SE PUEDE MOSTRAR](Imagenes/Docs_cloud_img/3.png)

Luego de crearlo debemos colocar un nombre, que será único en toda la plataforma y damos siguiente sin agregar etiquetas. 

En tipo de ubicación dejamos en EEUU y continuar.

La clase de almacenamientoi la dejamos en la configuración estándar y continuamos.

En acceso a los objetos dejamos en estándar impidiendo que quede abierto al público y le damos en crear. Si aparece un aviso de que está sin acceso público es que nos ha creado correctamente el Bocket.

De esta manera deberíamos ver la interfaz de Buckets:

![NO SE PUEDE MOSTRAR](Imagenes/Docs_cloud_img/4.png)

Ahora, para cargar los datos desde nuestra PC debemos usar un script de Python que cargue los datos a través de una llave de acceso que se mostrará ahora como crear.

### Creación de la Llave de Acceso 

Vamos a la barra lateral izquierda nuevamente y seleccionamos IAM y Administración, luego cuentas de servicio:

![NO SE PUEDE MOSTRAR](Imagenes/Docs_cloud_img/5.png)

Ahora le damos en CREAR CUENTA DE SERVICIO:

![NO SE PUEDE MOSTRAR](Imagenes/Docs_cloud_img/6.png)

Cargamos los detalles de la cuenta de servicio:

![NO SE PUEDE MOSTRAR](Imagenes/Docs_cloud_img/7.png)

En rol seleccionamos Básco y luego Propietario. Damos continuar:

![NO SE PUEDE MOSTRAR](Imagenes/Docs_cloud_img/8.png)

La última opción la dejamos en blanco y damos LISTO.

En el menú desplegable de la derecha del Permiso seleccionamos Administrar Claves:

![NO SE PUEDE MOSTRAR](Imagenes/Docs_cloud_img/9.png)

En la pestaña AGREGAR CLAVE le damos en Crear clave Nueva, en el cuadro de diálogo nos pedirá el formato, seleccionamos JSON. Luego lo nombramos y descargamos en un lugar seguro, ya que con ella cualquier persona podría hacer cambios de propietario en la Base de datos. Nos saldrá el mensaje de creación y descarga exitosa de la clave, luego seguimos con la carga de datos al Bocket.

![NO SE PUEDE MOSTRAR](Imagenes/Docs_cloud_img/11.png)

### Carga de datos al Bucket desde la PC usando Python y VSC

Debemos tener el archivo JSON descargado en la PC. Luego lo localizamos en el código del script y completamos la demás información que necesitamos.

```python
from google.cloud import storage

def subir_archivo_gcs(nombre_archivo, ruta_archivo, nombre_bucket="findeden"):
    """Sube un archivo a un bucket de Google Cloud Storage.

    Args:
        nombre_archivo: Nombre del archivo en el bucket (con extensión).
        ruta_archivo: Ruta completa al archivo en tu sistema local.
        nombre_bucket: Nombre del bucket de destino (por defecto "findeden").
    """
    try:
        storage_client = storage.Client.from_service_account_json('gcp.json')
        bucket = storage_client.bucket(nombre_bucket)
        blob = bucket.blob(nombre_archivo)

        # Aumentamos el timeout a 10 minutos para archivos grandes o conexiones lentas
        blob.upload_from_filename(ruta_archivo, timeout=600) 
        
        print(f"Archivo {nombre_archivo} subido a {nombre_bucket} exitosamente.")
    except Exception as e:
        print(f"Error al subir el archivo: {e}")

# Llamada a la función para subir tu archivo
subir_archivo_gcs('metadatosCA.parquet', 'Archivos/metadatosCA.parquet')
```
Lo siguiente es ejecutar el script, y eso lo hacemos con el siguiente comando en consola o en JupyterNotebooks:

```markdown
!python cloud_up.py
```

Luego de esto deberíamos corroborar los cambios en la nube. Para esto podemos habrir la vista previa.

### Dar Permiso de Acceso a un Proyecto

Vamos nuevamente a IAM y Administración, seleccionamos IAM, vamos a OTORGAR ACCESO.

Luego completamos la casilla de "Principales nuevas" con el correo de la persona a la que queremos habilitar y seleccionamos rol Administrador de objetos de Storage

![NO SE PUEDE MOSTRAR](Imagenes/Docs_cloud_img/13.png)

Lo siguiente es corroborar que el permiso esta presente en el panel de IAM:

![NO SE PUEDE MOSTRAR](Imagenes/Docs_cloud_img/12.png)

Por último debemos enviar la direccion del Bucket a la persona a la que concedimos el permiso.

## 2 - Crear un dataset en BigQuery
