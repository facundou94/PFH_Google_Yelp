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
