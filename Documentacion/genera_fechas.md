## **Función: `cargar_csv_a_dataframe`**

**Descripción:**

Esta función carga un archivo CSV en un DataFrame de pandas, genera una nueva columna de fechas en orden decreciente y guarda el DataFrame modificado de nuevo en el archivo CSV, sobrescribiendo el original.

**Código:**

```python
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

```

**Explicación detallada:**

1. **Carga del CSV:**
   - `pd.read_csv(ruta_archivo)`: Lee el archivo CSV especificado en `ruta_archivo` y lo almacena en un DataFrame de pandas llamado `df`.

2. **Generación de fechas decrecientes:**
   - `fecha_inicio_dt = datetime.strptime(fecha_inicio, '%d/%m/%Y')`: Convierte la cadena de texto `fecha_inicio` (por defecto, '16/07/2024') en un objeto `datetime` para poder realizar operaciones de fecha.
   - `df['fecha'] = [fecha_inicio_dt - timedelta(days=idx // 1000) for idx in df.index]`:
      - Crea una nueva columna llamada `fecha` en el DataFrame.
      - Itera sobre cada índice de fila (`idx`) en el DataFrame.
      - Para cada índice, calcula una fecha restando `idx // 1000` días a la `fecha_inicio_dt`. Esto significa que la fecha disminuirá en un día por cada 1000 filas.
      - Asigna la fecha calculada a la fila correspondiente en la nueva columna `fecha`.

3. **Asignación a variable global:**
   - `globals()[nombre_archivo] = df`: Asigna el DataFrame modificado (con la nueva columna de fecha) a una variable global. El nombre de la variable global será el mismo que `nombre_archivo` (sin la extensión `.csv`). Esto permite acceder fácilmente al DataFrame desde cualquier parte del código.

4. **Guardado en CSV:**
   - `df.to_csv(ruta_archivo, index=False)`: Guarda el DataFrame modificado en un archivo CSV.
      - `ruta_archivo`: Es la misma ruta que se utilizó para cargar el archivo original, lo que significa que el archivo original será sobrescrito.
      - `index=False`: Evita que se guarde el índice de filas en el CSV.

**Parámetros:**

- `nombre_archivo` (str): Nombre del archivo CSV sin la extensión. Este nombre se utilizará para crear la variable global que almacena el DataFrame.
- `ruta_archivo` (str): Ruta completa al archivo CSV que se va a cargar y sobreescribir.
- `fecha_inicio` (str, opcional): Fecha de inicio en formato 'dd/mm/aaaa' para la generación de la columna de fecha. El valor predeterminado es '16/07/2024'.

**Valor de retorno:**

- None (La función no devuelve ningún valor explícitamente, pero modifica el estado global al crear una variable con el nombre del archivo que contiene el DataFrame resultante).

**Dependencias:**

- `pandas`: Biblioteca para manipulación y análisis de datos.
- `datetime`, `timedelta`: Módulos de Python para trabajar con fechas y horas.