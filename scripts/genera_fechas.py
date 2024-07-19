import pandas as pd
from datetime import datetime, timedelta

# Función para cargar, nombrar DataFrames, agregar fecha decreciente y guardar en CSV
def cargar_csv_a_dataframe(nombre_archivo, ruta_archivo, fecha_inicio='16/07/2024'):
    df = pd.read_csv(ruta_archivo)

    # Agregar columna de fecha decreciente
    fecha_inicio_dt = datetime.strptime(fecha_inicio, '%d/%m/%Y')
    df['fecha'] = [fecha_inicio_dt - timedelta(days=idx // 1000) for idx in df.index]

    globals()[nombre_archivo] = df  # Asignar DataFrame a variable global

    # Guardar DataFrame en CSV (sobreescribir)
    df.to_csv(ruta_archivo, index=False)  # index=False evita guardar el índice de filas

# Archivos ML:
cargar_csv_a_dataframe('metadatos_ML', './Archivos/metadatos_ML.csv')
cargar_csv_a_dataframe('reviewsGoogle_ML', './Archivos/reviewsGoogle_ML.csv')
cargar_csv_a_dataframe('locales_LA', './Archivos/locales_LA.csv')
cargar_csv_a_dataframe('reviews_LA', './Archivos/reviews_LA.csv')

# Archivos Inmobiliaria:
cargar_csv_a_dataframe('Contratos', './datasets/SQL/Contratos.csv')
cargar_csv_a_dataframe('Inquilinos', './datasets/SQL/Inquilinos.csv')
cargar_csv_a_dataframe('Propiedades', './datasets/SQL/Propiedades.csv')
cargar_csv_a_dataframe('Publicaciones_Alquileres', './datasets/SQL/Publicaciones_Alquileres.csv')
