# Documentación Técnica del Script de Carga Incremental a MySQL

## Descripción General

Este script está diseñado para cargar datos de archivos CSV en una base de datos MySQL. Realiza una carga incremental, es decir, solo carga los datos que son más recientes que los datos actualmente almacenados en la base de datos. La documentación a continuación describe cómo se conecta a la base de datos, verifica la existencia de tablas, crea tablas si es necesario y realiza la carga de datos.

## Requisitos

- Python 3.x
- Bibliotecas: `pandas`, `sqlalchemy`, `mysql-connector-python`
- Base de datos MySQL en ejecución

## Estructura del Script

El script realiza las siguientes operaciones:

1. **Conexión a la Base de Datos**
2. **Verificación y Creación de Tablas**
3. **Carga Incremental de Datos**

### 1. Conexión a la Base de Datos

El primer paso es establecer una conexión a la base de datos MySQL utilizando SQLAlchemy y `mysql-connector-python`.

```python
from sqlalchemy import create_engine
import mysql.connector
from mysql.connector import Error

# Configuración de conexión a MySQL
db_config = {
    'user': 'usuario',
    'password': 'contraseña',
    'host': 'localhost',
    'database': 'findeden'
}

# Crear conexión con SQLAlchemy
engine = create_engine(f"mysql+mysqlconnector://{db_config['user']}:{db_config['password']}@{db_config['host']}/{db_config['database']}")
```

### 2. Verificación y Creación de Tablas

El script verifica si las tablas existen en la base de datos. Si una tabla no existe, la crea. Aquí se presenta el fragmento para verificar la existencia de una tabla y crearla si es necesario.

```python
def check_table_exists(engine, table_name):
    query = f"SHOW TABLES LIKE '{table_name}'"
    with engine.connect() as connection:
        result = connection.execute(query).fetchone()
    return result is not None

def create_table_from_df(engine, df, table_name):
    df.to_sql(table_name, engine, if_exists='replace', index=False)
    print(f"Tabla {table_name} creada exitosamente.")

# Ejemplo de uso
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
```

### 3. Carga Incremental de Datos

La carga incremental solo inserta datos que son más recientes que los datos ya existentes en la tabla. Aquí se muestra cómo se realiza la carga incremental.

```python
def get_most_recent_date(connection, table_name):
    query = f"SELECT MAX(fecha) FROM {table_name}"
    cursor = connection.cursor()
    cursor.execute(query)
    result = cursor.fetchone()
    return result[0]

def incremental_load(connection, df, table_name):
    most_recent_date = get_most_recent_date(connection, table_name)
    if most_recent_date:
        df = df[df['fecha'] > most_recent_date]
    if not df.empty:
        df.to_sql(table_name, connection, if_exists='append', index=False)
        print(f"Datos insertados en {table_name}.")
    else:
        print("No hay datos nuevos para insertar.")

# Ejemplo de uso
with engine.connect() as connection:
    for table_name, df in dfs.items():
        incremental_load(connection, df, table_name)
```

### Manejo de Errores

El script maneja errores comunes como columnas desconocidas y errores de datos. Se recomienda ajustar los tipos de datos en la base de datos para evitar estos problemas.

```python
def alter_column(engine, table_name, column_name, new_type):
    query = f"ALTER TABLE {table_name} MODIFY COLUMN {column_name} {new_type}"
    with engine.connect() as connection:
        connection.execute(query)
    print(f"Columna {column_name} en la tabla {table_name} modificada a {new_type}.")

# Ejemplo de uso para cambiar el tipo de columna 'category'
alter_column(engine, 'metadatos_ML', 'category', 'TEXT')
```

### Conclusión

Este script facilita la carga incremental de datos desde archivos CSV a una base de datos MySQL, gestionando la creación de tablas y la actualización de datos. Asegúrate de ajustar la configuración y los tipos de datos según tus necesidades específicas.

---

Puedes guardar este contenido en un archivo con extensión `.md` para incluirlo en tu documentación técnica.