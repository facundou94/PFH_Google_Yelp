## Documentación Técnica: Extracción de Tablas MySQL a Archivos CSV

### Descripción General
Este script en Python se utiliza para extraer datos de tablas específicas de una base de datos MySQL y guardarlos en archivos CSV en un directorio especificado. La funcionalidad principal está encapsulada en la función `extraer_tablas_mysql_a_csv`.

### Requisitos
- Python 3.x
- Librerías:
  - `mysql-connector-python`
  - `pandas`

### Instalación de Dependencias
Puedes instalar las dependencias necesarias ejecutando:
```bash
pip install mysql-connector-python pandas
```

### Uso
La función `extraer_tablas_mysql_a_csv` se conecta a una base de datos MySQL, consulta datos de tablas específicas y guarda los datos en archivos CSV en un directorio local.

### Parámetros
- `host` (str): Dirección del servidor MySQL. Valor por defecto: 'localhost'.
- `port` (int): Puerto del servidor MySQL. Valor por defecto: 3307.
- `user` (str): Nombre de usuario de MySQL. Valor por defecto: 'root'.
- `password` (str): Contraseña de MySQL. Valor por defecto: '2236'.
- `database` (str): Nombre de la base de datos. Valor por defecto: 'Legacy_Inmobiliaria'.
- `csv_directory` (str): Directorio donde se guardarán los archivos CSV. Valor por defecto: 'datasets/SQL/'.

### Código
```python
import os
import mysql.connector
import pandas as pd

def extraer_tablas_mysql_a_csv(host='localhost', port=3307, user='root', password='2236',
                               database='Legacy_Inmobiliaria', csv_directory='datasets/SQL/'):
    """Extrae datos de tablas MySQL y los guarda en archivos CSV.

    Args:
        host: Dirección del servidor MySQL.
        port: Puerto del servidor MySQL.
        user: Nombre de usuario de MySQL.
        password: Contraseña de MySQL.
        database: Nombre de la base de datos.
        csv_directory: Directorio donde se guardarán los CSV.
    """

    try:
        # Conexión a la base de datos MySQL
        cnx = mysql.connector.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            database=database
        )

        # Asegurarse de que la carpeta exista
        os.makedirs(csv_directory, exist_ok=True)

        # Consultar datos de las tablas y guardar en archivos CSV
        tables = ['propiedades', 'publicaciones_Alquileres', 'inquilinos', 'contratos']
        for table in tables:
            query = f'SELECT * FROM {table}'
            df = pd.read_sql(query, cnx)
            df.to_csv(os.path.join(csv_directory, f'{table}.csv'), index=False)
            print(f'Archivo {table}.csv guardado en {csv_directory}.')

    except mysql.connector.Error as err:
        print(f"Error al conectar a MySQL: {err}")

    finally:
        # Cerrar la conexión
        if cnx.is_connected():
            cnx.close()

    print('Todos los archivos CSV han sido guardados en la carpeta local.')

# Llamada a la función
extraer_tablas_mysql_a_csv()  # Puedes pasar argumentos si es necesario
```

### Explicación del Código

1. **Importación de Módulos:**
   - `os`: Para la gestión del sistema de archivos.
   - `mysql.connector`: Para la conexión a la base de datos MySQL.
   - `pandas`: Para la manipulación de datos y conversión a CSV.

2. **Función `extraer_tablas_mysql_a_csv`:**
   - **Parámetros:** Define los parámetros necesarios para la conexión a MySQL y el directorio donde se guardarán los CSV.
   - **Conexión a MySQL:** Utiliza `mysql.connector.connect` para establecer una conexión con la base de datos.
   - **Creación del Directorio:** Utiliza `os.makedirs` para asegurarse de que el directorio especificado exista.
   - **Consulta y Guardado de Datos:** Para cada tabla en la lista `tables`, ejecuta una consulta SQL para obtener todos los datos de la tabla y los guarda en un archivo CSV utilizando `pandas`.
   - **Manejo de Errores:** Captura errores de conexión a MySQL y los imprime.
   - **Cierre de Conexión:** Asegura que la conexión a la base de datos se cierre al finalizar.

3. **Llamada a la Función:**
   - Ejecuta la función `extraer_tablas_mysql_a_csv` con los valores por defecto de los parámetros.

### Ejecución del Script
Para ejecutar el script, simplemente guarda el código en un archivo Python (por ejemplo, `extraer_mysql_a_csv.py`) y ejecútalo:
```bash
python extraer_mysql_a_csv.py
```

### Notas Adicionales
- Puedes modificar los parámetros al llamar a la función para conectar a diferentes servidores, bases de datos, o cambiar el directorio de los CSV.
- Asegúrate de que los valores de los parámetros sean correctos para tu entorno de base de datos.

Esta documentación proporciona una guía completa para entender y utilizar el script de extracción de datos de MySQL a CSV.