import pandas as pd
from sqlalchemy import create_engine, inspect

# Credenciales de la base de datos MySQL
database_username = 'root'
database_password = '2236'
database_ip       = '127.0.0.1' 
database_port     = '3307'
database_name     = 'findeden'

# Crear el motor de conexión
engine = create_engine(f'mysql+mysqlconnector://{database_username}:{database_password}@{database_ip}:{database_port}/{database_name}')

def crear_tabla_si_no_existe(df, nombre_tabla):
    """Verifica si la tabla existe y la crea si no existe."""
    inspector = inspect(engine)
    tablas_existentes = inspector.get_table_names()

    if nombre_tabla not in tablas_existentes:
        print(f"La tabla '{nombre_tabla}' no existe. Creando tabla...")
        try:
            df.to_sql(nombre_tabla, con=engine, if_exists='fail', index=False)
        except ValueError as e:
            if "Table '{}' already exists".format(nombre_tabla) in str(e):
                print(f"La tabla '{nombre_tabla}' ya existe. No es necesario crearla de nuevo.")
            else:
                raise
    else:
        print(f"La tabla '{nombre_tabla}' ya existe. No es necesario crearla de nuevo.")

if __name__ == "__main__":
    # Supón que tienes tus DataFrames ya cargados
    df_metadatos = pd.read_csv('./Archivos/metadatos_ML.csv')
    df_reviewsGoogle = pd.read_csv('./Archivos/reviewsGoogle_ML.csv')
    df_metadatos_filtered = pd.read_csv('./Archivos/locales_LA.csv')
    df_reviewsGoogle_filtered = pd.read_csv('./Archivos/reviews_LA.csv')

    # Nombres de las tablas en MySQL
    table_metadatos = 'metadatos'
    table_reviews = 'reviewsGoogle'
    table_metadatos_filtered = 'locales_LA'
    table_reviews_filtered = 'reviews_LA'

    # Verificar y crear tablas si no existen
    crear_tabla_si_no_existe(df_metadatos, table_metadatos)
    crear_tabla_si_no_existe(df_reviewsGoogle, table_reviews)
    crear_tabla_si_no_existe(df_metadatos_filtered, table_metadatos_filtered)
    crear_tabla_si_no_existe(df_reviewsGoogle_filtered, table_reviews_filtered)
