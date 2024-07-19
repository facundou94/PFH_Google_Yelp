## **Función: `genera_entradas`**

**Descripción:**

Esta función carga DataFrames desde archivos CSV, copia las últimas 100 filas de cada DataFrame, actualiza la columna de fecha de estas filas con la fecha actual del sistema y luego agrega estas filas modificadas al final del DataFrame original. Finalmente, guarda los DataFrames modificados de nuevo en sus respectivos archivos CSV, sobrescribiendo los originales.

**Código:**

```python
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

```

**Explicación detallada:**

1. **Parámetros de entrada:**
   - `nombres_archivos` (list): Una lista de cadenas que contiene los nombres de los DataFrames a procesar (sin la extensión `.csv`). Estos nombres deben coincidir con las variables globales que almacenan los DataFrames.
   - `rutas_archivos` (list): Una lista de cadenas que contiene las rutas completas a los archivos CSV correspondientes a cada DataFrame. El orden de las rutas debe coincidir con el orden de los nombres en `nombres_archivos`.

2. **Obtención de la fecha actual:**
   - `fecha_actual = date.today().strftime('%Y-%m-%d')`: Obtiene la fecha actual del sistema y la formatea como una cadena en el formato 'YYYY-MM-DD'.

3. **Iteración sobre DataFrames y archivos:**
   - `for nombre, ruta in zip(nombres_archivos, rutas_archivos)`: Itera simultáneamente sobre las listas `nombres_archivos` y `rutas_archivos`. En cada iteración, `nombre` contendrá el nombre de un DataFrame y `ruta` contendrá la ruta al archivo CSV correspondiente.

4. **Carga del DataFrame:**
   - `df = pd.read_csv(ruta)`: Carga el DataFrame desde el archivo CSV especificado en `ruta`.

5. **Copia de las últimas filas:**
   - `ultimas_filas = df.tail(100).copy()`: Selecciona las últimas 100 filas del DataFrame y las copia en un nuevo DataFrame llamado `ultimas_filas`. El método `.copy()` se utiliza para crear una copia independiente de las filas, evitando modificar el DataFrame original.

6. **Actualización de la fecha:**
   - `ultimas_filas['fecha'] = fecha_actual`: Asigna la `fecha_actual` (obtenida en el paso 2) a todas las filas en la columna `fecha` del DataFrame `ultimas_filas`.

7. **Concatenación de DataFrames:**
   - `df = pd.concat([df, ultimas_filas], ignore_index=True)`: Concatena el DataFrame original (`df`) con las últimas filas modificadas (`ultimas_filas`). El argumento `ignore_index=True` asegura que se creen nuevos índices para las filas agregadas, evitando conflictos con los índices existentes.

8. **Guardado en CSV:**
   - `df.to_csv(ruta, index=False)`: Guarda el DataFrame modificado (que ahora incluye las últimas filas con la fecha actualizada) en el archivo CSV original, sobrescribiéndolo. El argumento `index=False` evita que se guarde el índice de filas en el CSV.

**Ejemplo de uso:**

```python
nombres_archivos = ['metadatos_ML', 'reviewsGoogle_ML']
rutas_archivos = ['./Archivos/metadatos_ML.csv', './Archivos/reviewsGoogle_ML.csv']
genera_entradas(nombres_archivos, rutas_archivos)
```

Esto procesará los archivos `metadatos_ML.csv` y `reviewsGoogle_ML.csv`, agregando 100 filas al final de cada uno con la fecha actual en la columna `fecha`.