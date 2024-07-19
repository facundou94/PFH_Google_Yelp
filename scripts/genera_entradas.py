import pandas as pd
from datetime import date

def genera_entradas(nombres_archivos, rutas_archivos):
    """
    Carga DataFrames, copia las últimas 100 filas, actualiza la fecha 
    con la fecha actual y agrega estas filas al final del DataFrame original.
    Luego, guarda los DataFrames modificados en CSV.

    Args:
        nombres_archivos (list): Lista de nombres de los DataFrames (sin extensión).
        rutas_archivos (list): Lista de rutas completas a los archivos CSV.
    """
    
    fecha_actual = date.today().strftime('%Y-%m-%d')  # Obtener fecha actual en formato 'YYYY-MM-DD'

    for nombre, ruta in zip(nombres_archivos, rutas_archivos):
        # Cargar DataFrame
        df = pd.read_csv(ruta)  

        # Copiar últimas 100 filas
        ultimas_filas = df.tail(100).copy()  # Copiar para evitar modificar el DataFrame original

        # Actualizar fecha con la fecha actual
        ultimas_filas['fecha'] = fecha_actual

        # Concatenar las últimas filas modificadas al DataFrame original
        df = pd.concat([df, ultimas_filas], ignore_index=True)

        # Guardar DataFrame modificado en CSV (sobreescribir)
        df.to_csv(ruta, index=False)

# Listas de nombres y rutas de archivos
nombres_archivos = ['metadatos_ML', 'reviewsGoogle_ML', 'locales_LA', 'reviews_LA', 
                    'Contratos', 'Inquilinos', 'Propiedades', 'Publicaciones_Alquileres']
rutas_archivos = ['./Archivos/metadatos_ML.csv', './Archivos/reviewsGoogle_ML.csv', './Archivos/locales_LA.csv', './Archivos/reviews_LA.csv',
                  './datasets/SQL/Contratos.csv', './datasets/SQL/Inquilinos.csv', './datasets/SQL/Propiedades.csv', './datasets/SQL/Publicaciones_Alquileres.csv']

# Llamar a la función para generar las entradas
genera_entradas(nombres_archivos, rutas_archivos)
