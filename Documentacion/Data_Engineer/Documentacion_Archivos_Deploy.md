Aquí tienes un esquema para la documentación del archivo `app.py` en formato Markdown:

---

# Documentación del archivo `app.py`

## Descripción general

Este archivo define una aplicación web interactiva utilizando [Streamlit](https://streamlit.io/). La aplicación permite a los usuarios seleccionar sus preferencias en cuanto a restaurantes, lugares de culto y lugares recreativos en su barrio, y luego genera un mapa interactivo que muestra las recomendaciones basadas en estas preferencias. 

## Dependencias

- `streamlit`: Para crear la interfaz web.
- `pandas`: Para la manipulación de datos.
- `folium`: Para la visualización de mapas.
- `streamlit_folium`: Para integrar Folium con Streamlit.
- `matplotlib.colors`: Para generar una paleta de colores.
- `ML_funciones`: Módulo personalizado para funciones de Machine Learning.

## Importaciones

```python
import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static
from folium.features import DivIcon
import ML_funciones
import matplotlib.colors as mcolors
```

## Carga de datos

```python
df_locales_ml = pd.read_csv("df_locales_ml.csv")
```

Se carga un archivo CSV que contiene datos sobre los lugares recomendados.

## Función `get_color(score)`

Genera un color en formato hexadecimal basado en una puntuación (`score`).

```python
def get_color(score):
    cmap = mcolors.LinearSegmentedColormap.from_list("", ["red", "yellow", "green"])
    norm = mcolors.Normalize(vmin=0, vmax=10)
    return mcolors.rgb2hex(cmap(norm(score)))
```

## Configuración del estilo y elementos de la interfaz

Se carga un archivo de estilo CSS y se configura la interfaz de usuario.

```python
with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.image("banner.jpg", width=1000)
st.title("FindEden: Encuentra tu propio Eden")
st.header("Bienvenido/a. Selecciona tus preferencias:")
```

## Entradas del usuario

Los usuarios pueden seleccionar sus preferencias en cuanto a restaurantes, lugares de culto y lugares recreativos mediante menús desplegables.

```python
val_res = st.selectbox("Cuánto valor tiene para vos contar con buenos restaurantes en tu barrio ?:", ["Mucho", "Normal", "Poco", "Nada"])
restaurant = None
if val_res in ["Mucho", "Normal", "Poco"]:
    restaurant = st.selectbox("Qué tipos de restaurantes te gustan ?:", ['Comida asiática', 'Comida latina', 'Comida europea', 'Comida norteamericana', 'Comida vegana'])
...
```

## Generación del mapa

Al presionar el botón "Generar mapa", se calculan las preferencias del usuario y se visualizan en un mapa interactivo.

```python
button_pressed = st.button("Generar mapa")

if button_pressed:
    ...
    lat_inm, lon_inm = ML_funciones.group_coordinates(...)
    user_pref = ML_funciones.generate_user_preferences(...)
    df_App, df_locales = ML_funciones.obtener_recomendacion(...)
    m = folium.Map(location=[df_App['lat'].mean(), df_App['lon'].mean()], zoom_start=12)
    ...
    folium_static(m)
```

### Leyenda del mapa

Se muestra una leyenda en el mapa para explicar los diferentes colores utilizados para los puntos en el mapa.

```python
legend_html = """
<div class='legend-container'>
...
"""
st.markdown(legend_html, unsafe_allow_html=True)
```

## Mensajes

Se muestran mensajes relacionados con las ubicaciones recomendadas.

```python
st.subheader("Mensajes:")
for i, mensajes in enumerate(df_App['mensajes'], start=1):
    st.write(f"Ubicación {i}:")
    for mensaje in mensajes:
        st.write(f"* {mensaje}")
```

## Archivos externos

- `df_locales_ml.csv`: Archivo CSV con datos de locales.
- `style.css`: Archivo de estilos CSS.
- `banner.jpg`: Imagen de banner.

## Módulos personalizados

- `ML_funciones`: Este módulo contiene funciones personalizadas para la generación de preferencias de usuario y recomendaciones basadas en datos.

---

Aquí tienes un esquema para la documentación del archivo `app.yaml` en formato Markdown:

---

# Documentación del archivo `app.yaml`

## Descripción general

El archivo `app.yaml` es la configuración para el despliegue de una aplicación en Google App Engine. Este archivo define el entorno de ejecución y la configuración necesaria para que la aplicación funcione correctamente en el entorno flexible de Google Cloud.

## Contenido del archivo

```yaml
runtime: custom
env: flex
```

### Campos

- **`runtime`**: Define el entorno de ejecución para la aplicación. En este caso, se especifica `custom`, lo que indica que se utilizará una imagen de contenedor personalizada para ejecutar la aplicación.

- **`env`**: Define el entorno en el que se ejecutará la aplicación. El valor `flex` indica que se utilizará el entorno flexible de Google App Engine, que permite una mayor personalización y escalabilidad en comparación con el entorno estándar.

## Entorno Flexible

El entorno flexible de Google App Engine proporciona las siguientes características:

- **Escalabilidad automática**: La aplicación puede escalar automáticamente en función del tráfico.
- **Personalización del entorno**: Permite el uso de contenedores personalizados y la configuración de variables de entorno.
- **Integración con servicios de Google Cloud**: Facilita la integración con otros servicios de Google Cloud, como bases de datos y almacenamiento.

## Consideraciones

- **Contenedor personalizado**: Asegúrate de tener un Dockerfile adecuado para construir la imagen del contenedor si estás utilizando un entorno `custom`.
- **Configuración adicional**: Puede ser necesario proporcionar archivos de configuración adicionales, como un Dockerfile, para definir el entorno exacto en el que se ejecutará la aplicación.

---

Este archivo es bastante sencillo, pero es fundamental para el despliegue en Google App Engine. 

Aquí tienes un esquema para la documentación del archivo `Dockerfile` en formato Markdown:

---

# Documentación del archivo `Dockerfile`

## Descripción general

El archivo `Dockerfile` define la imagen del contenedor para la aplicación. Esta imagen se utiliza para construir y ejecutar la aplicación en un entorno de contenedor Docker. En este caso, se usa una imagen base de Python y se configura para ejecutar una aplicación de Streamlit.

## Contenido del archivo

```dockerfile
FROM python:3.12.1-slim

# remember to expose the port your app'll be exposed on.
EXPOSE 8080

RUN pip install -U pip

COPY requirements.txt app/requirements.txt
RUN pip install -r app/requirements.txt

# copy into a directory of its own (so it isn't in the toplevel dir)
COPY . /app
WORKDIR /app

# run it!
ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8080", "--server.address=0.0.0.0"]
```

### Instrucciones

- **`FROM python:3.12.1-slim`**: Utiliza la imagen base de Python 3.12.1 en su versión `slim`, que es una versión reducida para minimizar el tamaño de la imagen.

- **`EXPOSE 8080`**: Expone el puerto 8080 para que la aplicación sea accesible desde fuera del contenedor.

- **`RUN pip install -U pip`**: Actualiza `pip` a la última versión disponible.

- **`COPY requirements.txt app/requirements.txt`**: Copia el archivo `requirements.txt` al directorio `app/` dentro del contenedor.

- **`RUN pip install -r app/requirements.txt`**: Instala las dependencias especificadas en `requirements.txt`.

- **`COPY . /app`**: Copia el contenido del directorio actual (donde se encuentra el Dockerfile) al directorio `/app` dentro del contenedor.

- **`WORKDIR /app`**: Establece el directorio de trabajo dentro del contenedor en `/app`.

- **`ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8080", "--server.address=0.0.0.0"]`**: Define el comando que se ejecutará cuando el contenedor se inicie. En este caso, se inicia la aplicación de Streamlit en el puerto 8080 y se configura para escuchar en todas las interfaces de red (`0.0.0.0`).

## Consideraciones

- **Port Binding**: Asegúrate de que el puerto 8080 esté abierto y disponible para el tráfico en el entorno donde se ejecuta el contenedor.
- **Dependencias**: Asegúrate de que todas las dependencias necesarias estén listadas en el archivo `requirements.txt`.
- **Archivo `app.py`**: El archivo `app.py` debe estar presente en el directorio desde el cual se construye la imagen, ya que es el punto de entrada de la aplicación.

---

Este `Dockerfile` es clave para crear la imagen de contenedor que se usará para desplegar tu aplicación en un entorno de contenedor. 

# Documentación del archivo `ML_funciones.py`

Este archivo contiene funciones utilizadas para generar preferencias de usuario, filtrar y puntuar locales según las preferencias del usuario, y obtener recomendaciones personalizadas.

## Funciones

### `generate_user_preferences`

Genera un diccionario de preferencias de usuario basado en los parámetros proporcionados.

**Parámetros:**
- `res_w` (int): Peso para la categoría de restaurante (0, 1, 2, 3).
- `res_sc` (int): Subcategoría del restaurante (0 a 5).
- `rel_w` (int): Peso para la categoría de religión (0, 1, 2, 3).
- `rel_sc` (int): Subcategoría de religión (0 a 5).
- `rec_w` (int): Peso para la categoría de recreación (0, 1, 2, 3).
- `rec_sc` (int): Subcategoría de recreación (0 a 3).
- `ct` (int): Cronotipo del usuario (0, 1).

**Retorno:**
- `user_preferences` (dict): Diccionario con las preferencias del usuario.

**Excepciones:**
- `ValueError`: Si algún parámetro no está en el rango permitido.

---

### `group_coordinates`

Agrupa coordenadas en listas de latitudes y longitudes.

**Parámetros:**
- `*coords` (float): Coordenadas en pares de latitud y longitud.

**Retorno:**
- `lat_inm` (list): Lista de latitudes.
- `lon_inm` (list): Lista de longitudes.

---

### `filtrar_locales`

Filtra un DataFrame de locales según la distancia y las preferencias del usuario.

**Parámetros:**
- `df_locales` (pd.DataFrame): DataFrame con los datos de locales.
- `lat_inm` (float): Latitud del inmueble de referencia.
- `lon_inm` (float): Longitud del inmueble de referencia.
- `km` (float): Radio de filtrado en kilómetros.
- `user_pref` (dict): Diccionario con las preferencias del usuario.

**Retorno:**
- `df_filtrado` (pd.DataFrame): DataFrame filtrado con las columnas de interés y la columna 'distance'.

---

### `calcular_distancia`

Calcula la distancia en metros entre dos puntos geográficos.

**Parámetros:**
- `lat_1` (float): Latitud del primer punto.
- `long_1` (float): Longitud del primer punto.
- `lat_2` (float): Latitud del segundo punto.
- `long_2` (float): Longitud del segundo punto.

**Retorno:**
- `distancia_redondeada` (float): Distancia entre los dos puntos en metros, redondeada a la centena más cercana.

---

### `calcular_puntuacion`

Calcula la puntuación total de los locales según las preferencias del usuario y otras métricas.

**Parámetros:**
- `df_prueba` (pd.DataFrame): DataFrame de locales filtrados.
- `user_pref` (dict): Diccionario con las preferencias del usuario.

**Retorno:**
- `total_score` (float): Puntuación total.
- `score_res` (float): Puntuación para restaurantes.
- `score_rel` (float): Puntuación para religión.
- `score_rec` (float): Puntuación para recreación.
- `score_bien` (float): Puntuación para bienestar.
- `messages` (list): Mensajes de recomendación.

---

### `obtener_recomendacion`

Obtiene recomendaciones para un usuario basadas en un DataFrame de base de datos y preferencias del usuario.

**Parámetros:**
- `df_base_datos` (pd.DataFrame): DataFrame con los datos de locales.
- `user_pref` (dict): Diccionario con las preferencias del usuario.
- `km` (float): Radio de filtrado en kilómetros.
- `lat_inm` (list): Lista de latitudes de inmuebles.
- `lon_inm` (list): Lista de longitudes de inmuebles.

**Retorno:**
- `resultados_df` (pd.DataFrame): DataFrame con los resultados de la puntuación por inmueble.
- `locales_df` (pd.DataFrame): DataFrame con los locales filtrados y sus detalles.

---

## Ejemplos de Uso

**Generar preferencias de usuario:**
```python
user_preferences = generate_user_preferences(2, 1, 3, 4, 1, 2, 1)
```


# Documentación del archivo `requirements.txt`

Este archivo `requirements.txt` contiene una lista de paquetes necesarios para el proyecto. A continuación se detalla cada paquete incluido en el archivo:

- **altair==5.3.0**: Biblioteca para crear gráficos estadísticos declarativos en Python.
- **attrs==23.2.0**: Paquete para crear clases con atributos en Python de manera más sencilla.
- **blinker==1.8.2**: Biblioteca para señales y eventos en Python.
- **branca==0.7.2**: Herramienta para construir elementos de visualización interactiva en mapas.
- **cachetools==5.4.0**: Proporciona herramientas para trabajar con cachés y almacenamiento en memoria.
- **certifi==2024.7.4**: Paquete que proporciona certificados CA actualizados para la verificación de SSL.
- **charset-normalizer==3.3.2**: Biblioteca para la detección de codificación de caracteres.
- **click==8.1.7**: Biblioteca para crear interfaces de línea de comandos (CLI) en Python.
- **colorama==0.4.6**: Herramienta para facilitar el uso de colores en la salida de la consola en Windows.
- **contourpy==1.2.1**: Biblioteca para la creación de gráficos de contorno en Python.
- **cycler==0.12.1**: Herramienta para la creación de ciclos en el estilo de gráficos.
- **folium==0.17.0**: Biblioteca para crear mapas interactivos utilizando Leaflet.js.
- **fonttools==4.53.1**: Biblioteca para manipular fuentes y archivos de fuentes.
- **gitdb==4.0.11**: Implementación de la base de datos Git en Python.
- **GitPython==3.1.43**: Biblioteca para interactuar con repositorios Git desde Python.
- **idna==3.7**: Implementación del estándar IDNA para la codificación de nombres de dominio internacionales.
- **Jinja2==3.1.4**: Motor de plantillas para Python.
- **jsonschema==4.23.0**: Biblioteca para validar datos JSON con esquemas JSON.
- **jsonschema-specifications==2023.12.1**: Especificaciones para el esquema JSON.
- **kiwisolver==1.4.5**: Solver para problemas de diseño de interfaces.
- **markdown-it-py==3.0.0**: Implementación del parser Markdown para Python.
- **MarkupSafe==2.1.5**: Herramienta para evitar ataques XSS en aplicaciones web mediante el escape de datos.
- **matplotlib==3.9.1**: Biblioteca para crear gráficos en 2D en Python.
- **mdurl==0.1.2**: Paquete para el manejo de URLs en Markdown.
- **numpy==2.0.0**: Biblioteca fundamental para cálculos numéricos en Python.
- **packaging==24.1**: Herramientas para la gestión de versiones y metadatos en paquetes.
- **pandas==2.2.2**: Biblioteca para el análisis de datos y la manipulación de estructuras de datos.
- **pillow==10.4.0**: Biblioteca para el procesamiento de imágenes en Python.
- **protobuf==5.27.2**: Implementación de Protocol Buffers para la serialización de datos.
- **pyarrow==17.0.0**: Herramientas para la interoperabilidad de datos entre Python y Apache Arrow.
- **pydeck==0.9.1**: Biblioteca para crear visualizaciones geoespaciales interactivas.
- **Pygments==2.18.0**: Herramienta para la coloración de sintaxis en código fuente.
- **pyparsing==3.1.2**: Biblioteca para la creación de analizadores de gramática en Python.
- **python-dateutil==2.9.0.post0**: Herramienta para el manejo avanzado de fechas y horas.
- **pytz==2024.1**: Biblioteca para la manipulación de zonas horarias.
- **referencing==0.35.1**: Paquete para la gestión de referencias y citas.
- **requests==2.32.3**: Biblioteca para hacer solicitudes HTTP de manera sencilla.
- **rich==13.7.1**: Herramienta para renderizar contenido de manera colorida en la consola.
- **rpds-py==0.19.0**: Implementación en Python de estructuras de datos persistentes.
- **six==1.16.0**: Paquete de compatibilidad entre Python 2 y Python 3.
- **smmap==5.0.1**: Herramienta para manejar mapas de bits en Git.
- **streamlit==1.36.0**: Framework para construir aplicaciones web interactivas de datos.
- **streamlit_folium==0.21.1**: Integración de Folium con Streamlit.
- **tenacity==8.5.0**: Biblioteca para implementar estrategias de reintentos.
- **toml==0.10.2**: Herramienta para manejar archivos TOML.
- **toolz==0.12.1**: Funciones y herramientas para el procesamiento de datos en Python.
- **tornado==6.4.1**: Framework para crear aplicaciones web y servidores en Python.
- **typing_extensions==4.12.2**: Extensiones para las anotaciones de tipo en Python.
- **tzdata==2024.1**: Datos de zonas horarias.
- **urllib3==2.2.2**: Biblioteca para la manipulación de URLs y solicitudes HTTP.
- **watchdog==4.0.1**: Biblioteca para monitorear cambios en el sistema de archivos.
- **xyzservices==2024.6.0**: Paquete para acceder a servicios de mapas y datos geoespaciales.

Este archivo asegura que el entorno de desarrollo tenga todas las dependencias necesarias para el funcionamiento adecuado del proyecto.




# Documentación del archivo `styles.css`

Este archivo `styles.css` contiene las reglas de estilo para personalizar la apariencia de la página web. A continuación se describen las diferentes secciones y estilos aplicados:

## Fondo de la Página

```css
body {
    background-color: white; /* Fondo blanco */
    color: black; /* Texto negro */
}
```
- **`background-color: white;`**: Establece el color de fondo de la página en blanco.
- **`color: black;`**: Define el color del texto en negro.

## Fondo de los Widgets

```css
.stSelectbox, .stButton, .stHeader, .stSubheader, .stTextInput, .stImage {
    background-color: #8FBC8F; /* Verde claro */
}
```
- **`background-color: #8FBC8F;`**: Aplica un fondo verde claro a los widgets seleccionados (Selectbox, Button, Header, Subheader, TextInput, Image).

## Texto de los Widgets

```css
.stSelectbox > div, .stButton > div, .stHeader > div, .stSubheader > div, .stTextInput > div, .stImage > div {
    color: #2E8B57; /* Verde oscuro */
}
```
- **`color: #2E8B57;`**: Establece el color del texto en verde oscuro para los elementos dentro de los widgets.

## Fondo de los Selectores

```css
.css-1d391kg {
    background-color: #D2B48C; /* Marrón claro */
}
```
- **`background-color: #D2B48C;`**: Aplica un fondo marrón claro a los selectores con la clase `.css-1d391kg`.

## Texto de los Selectores

```css
.css-1d391kg .css-1p9a4ka, .css-1d391kg .css-2vtrri, .css-1d391kg .css-15tx938 {
    color: #2E8B57; /* Verde oscuro */
}
```
- **`color: #2E8B57;`**: Define el color del texto en verde oscuro para los elementos dentro de los selectores con la clase `.css-1d391kg`.

## Estilo para el Mapa de Folium

```css
.stMarkdown iframe {
    border: 5px solid #8B4513; /* Marrón */
}
```
- **`border: 5px solid #8B4513;`**: Establece un borde de 5px sólido color marrón alrededor de los iframes de los mapas de Folium.

## Estilo para el Panel de Leyenda

```css
.legend-container {
    background-color: #2E8B57; /* Verde oscuro */
    color: black; /* Texto blanco */
    border-radius: 10px;
    padding: 10px;
    font-size: 14px;
    z-index: 1000;
}
```
- **`background-color: #2E8B57;`**: Aplica un fondo verde oscuro al panel de leyenda.
- **`color: black;`**: Define el color del texto en blanco.
- **`border-radius: 10px;`**: Redondea las esquinas del panel con un radio de 10px.
- **`padding: 10px;`**: Añade un relleno de 10px alrededor del contenido del panel.
- **`font-size: 14px;`**: Establece el tamaño de la fuente en 14px.
- **`z-index: 1000;`**: Asegura que el panel de leyenda esté por encima de otros elementos.

Este archivo de estilos permite personalizar la apariencia de la página web para que coincida con la paleta de colores deseada y mejore la presentación visual de los elementos interactivos y el contenido.
```

Si hay algún detalle adicional o cambios que quieras hacer, solo dímelo.