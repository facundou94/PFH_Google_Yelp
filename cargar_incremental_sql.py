import pandas as pd
from sqlalchemy import create_engine, text
import mysql.connector
from mysql.connector import Error

# Credenciales de la base de datos MySQL
database_username = 'root'
database_password = '2236'
database_ip       = '127.0.0.1'
database_port     = '3307'
database_name     = 'findeden'

# DataFrames cargados desde los archivos CSV
df_metadatos = pd.read_csv('./Archivos/metadatos_ML.csv')
df_reviewsGoogle = pd.read_csv('./Archivos/reviewsGoogle_ML.csv')
df_metadatos_filtered = pd.read_csv('./Archivos/locales_LA.csv')
df_reviewsGoogle_filtered = pd.read_csv('./Archivos/reviews_LA.csv')

# Función para crear la conexión con SQLAlchemy
def create_engine_connection():
    engine = create_engine(f"mysql+mysqlconnector://{database_username}:{database_password}@{database_ip}:{database_port}/{database_name}")
    return engine

# Función para verificar la existencia de una tabla
def check_table_exists(engine, table_name):
    with engine.connect() as connection:
        query = text(f"SHOW TABLES LIKE '{table_name}'")
        result = connection.execute(query).fetchone()
        return result is not None

# Función para verificar la existencia de una columna en una tabla
def check_column_exists(engine, table_name, column_name):
    with engine.connect() as connection:
        query = text(f"SHOW COLUMNS FROM {table_name} LIKE '{column_name}'")
        result = connection.execute(query).fetchone()
        return result is not None

# Función para crear una tabla basada en el DataFrame
def create_table_from_df(engine, df, table_name):
    df.head(0).to_sql(table_name, con=engine, if_exists='replace', index=False)
    print(f"Tabla {table_name} creada exitosamente")

# Función para modificar la columna 'category' en MySQL
def modify_category_column(engine, table_name):
    if check_column_exists(engine, table_name, 'category'):
        with engine.connect() as connection:
            query = text(f"ALTER TABLE {table_name} MODIFY COLUMN category TEXT;")
            connection.execute(query)
        print(f"Columna 'category' en la tabla {table_name} modificada a TEXT")
    else:
        print(f"La columna 'category' no existe en la tabla {table_name}")

# Función para obtener la fecha más reciente en la tabla de MySQL
def get_latest_date(engine, table_name):
    with engine.connect() as connection:
        query = text(f"SELECT MAX(fecha) FROM {table_name}")
        result = connection.execute(query).scalar()
    return result

# Función para realizar la carga incremental
def incremental_load(engine, df, table_name):
    latest_date_db = get_latest_date(engine, table_name)
    latest_date_df = df['fecha'].max()
    
    print(f"Fecha más reciente en MySQL ({table_name}): {latest_date_db}")
    print(f"Fecha más reciente en los archivos: {latest_date_df}")
    
    if latest_date_db:
        df_to_load = df[df['fecha'] > latest_date_db]
    else:
        df_to_load = df

    if not df_to_load.empty:
        df_to_load.to_sql(table_name, con=engine, if_exists='append', index=False)
        print(f"Se cargaron {len(df_to_load)} filas en la tabla {table_name}")
    else:
        print("No hay filas nuevas para cargar")

# Crear la conexión con SQLAlchemy
engine = create_engine_connection()

# DataFrames y sus correspondientes nombres de tabla
dfs = {
    "metadatos_ML": df_metadatos,
    "reviewsGoogle_ML": df_reviewsGoogle,
    "locales_LA": df_metadatos_filtered,
    "reviews_LA": df_reviewsGoogle_filtered
}

for table_name, df in dfs.items():
    if not check_table_exists(engine, table_name):
        print(f"La tabla {table_name} no existe. Creando tabla...")
        create_table_from_df(engine, df, table_name)
    else:
        print(f"La tabla {table_name} ya existe.")
        # Modificar la columna 'category' si existe
        modify_category_column(engine, table_name)
    
    incremental_load(engine, df, table_name)

# Cerrar la conexión
engine.dispose()
print("Conexión a MySQL cerrada")
