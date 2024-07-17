import pandas as pd
from sqlalchemy import create_engine

# Credenciales de la base de datos MySQL
database_username = 'root'
database_password = '2236'
database_ip       = '127.0.0.1' 
database_port     = '3307'
database_name     = 'findeden'

# Crear el motor de conexión
engine = create_engine(f'mysql+mysqlconnector://{database_username}:{database_password}@{database_ip}:{database_port}/{database_name}')

def cargar_df_incremental(df, nombre_tabla, campo_clave):
    """Carga un DataFrame en MySQL de forma incremental.

    Args:
        df: El DataFrame a cargar.
        nombre_tabla: Nombre de la tabla en MySQL.
        campo_clave: Nombre del campo clave para identificar registros únicos.
    """
    with engine.connect() as conn:
        # Obtener los valores existentes del campo clave en la tabla (si existen)
        query_existentes = f"SELECT DISTINCT {campo_clave} FROM {nombre_tabla}"
        try:
            valores_existentes = pd.read_sql(query_existentes, conn)[campo_clave].tolist()
        except KeyError:  # Si la tabla está vacía, no hay valores existentes
            valores_existentes = []

        # Filtrar el DataFrame para incluir solo los nuevos registros
        df_nuevos = df[~df[campo_clave].isin(valores_existentes)]

        if not df_nuevos.empty:
            # Insertar los nuevos registros en la tabla
            df_nuevos.to_sql(nombre_tabla, con=engine, if_exists='append', index=False)
            print(f"Se agregaron {len(df_nuevos)} nuevos registros a la tabla '{nombre_tabla}'.")
        else:
            print(f"No se encontraron nuevos registros para la tabla '{nombre_tabla}'.")

if __name__ == "__main__":
    df_metadatos = pd.read_csv('./Archivos/metadatos_ML.csv')
    df_reviewsGoogle = pd.read_csv('./Archivos/reviewsGoogle_ML.csv')
    df_metadatos_filtered = pd.read_csv('./Archivos/locales_LA.csv')
    df_reviewsGoogle_filtered = pd.read_csv('./Archivos/reviews_LA.csv')

    # Nombres de las tablas en MySQL
    table_metadatos = 'metadatos'
    table_reviews = 'reviewsGoogle'
    table_metadatos_filtered = 'locales_LA'
    table_reviews_filtered = 'reviews_LA'

    try:
        # Carga incremental de los DataFrames
        cargar_df_incremental(df_metadatos, table_metadatos, 'address') 
        cargar_df_incremental(df_reviewsGoogle, table_reviews, 'user_id')
        cargar_df_incremental(df_metadatos_filtered, table_metadatos_filtered, 'address')
        cargar_df_incremental(df_reviewsGoogle_filtered, table_reviews_filtered, 'user_id')

    except Exception as e:
        print(f"Error al cargar los DataFrames en MySQL: {e}")
