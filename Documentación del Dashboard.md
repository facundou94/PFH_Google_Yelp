# Documentación del Dashboard Inmobiliario

## Introducción

Este documento describe la creación y configuración de un dashboard interactivo en Power BI para una inmobiliaria. El dashboard está diseñado para visualizar y analizar diversos KPIs relacionados con la ocupación, satisfacción y renovación de contratos de propiedades. Los datos se han extraído de una base de datos MySQL proporcionada por la inmobiliaria.

## Fuentes de Datos

Los datos utilizados en este dashboard provienen de una base de datos MySQL. La conexión a esta base de datos se realizó mediante las herramientas de importación de datos de Power BI.

## KPIs en el Dashboard

### 1 Tiempo Promedio de Vacancia
- **Descripción**: Mide el tiempo promedio que una propiedad permanece desocupada antes de ser alquilada nuevamente.
- **Cálculo**: Promedio de los días de vacancia de todas las propiedades.

### 2 Índice de Satisfacción del Cliente
- **Descripción**: Refleja la satisfacción general de los inquilinos con las propiedades y servicios de la inmobiliaria.
- **Cálculo**: Promedio de las valoraciones de los inquilinos.

### 3 Índice de Renovación de Contratos
- **Descripción**: Mide el porcentaje de contratos de alquiler que se renuevan al final de su término.
- **Cálculo**: (Número de contratos renovados / Número total de contratos) * 100

### 4 Índice de Conversión de Prospectos a Inquilinos
- **Descripción**: Mide la eficacia de la inmobiliaria en convertir prospectos en inquilinos.
- **Cálculo**: (Número de prospectos convertidos a inquilinos / Número total de prospectos) * 100

## Visualizaciones en el Dashboard

### Gráfico de Renovación de Contratos
- **Tipo de Gráfico**: Gráfico de Barras
- **Descripción**: Muestra la cantidad de contratos renovados frente a los no renovados en un periodo determinado.

### Correlación entre Valoración y Renovación de Contratos
- **Tipo de Gráfico**: Gráfico de Dispersión
- **Descripción**: Visualiza la relación entre la valoración de los inquilinos y la probabilidad de renovación del contrato.

### Valoración de Inquilinos
- **Tipo de Gráfico**: Gráfico de Barras Apiladas
- **Descripción**: Muestra qué aspectos valoran más los inquilinos (restaurantes, recreación, religión, etc.).
- **Cálculo**: Agrupación y suma de valoraciones por categoría.

###  Gráfico Medidor de Propiedades Desocupadas
- **Tipo de Gráfico**: Medidor
- **Descripción**: Indica el porcentaje de propiedades que están actualmente desocupadas.
- **Cálculo**: (Número de propiedades desocupadas / Número total de propiedades) * 100

###  Mapa de Propiedades
- **Tipo de Gráfico**: Mapa
- **Descripción**: Muestra la ubicación de cada propiedad en un mapa interactivo.
- **Datos Necesarios**: Dirección y coordenadas geográficas de cada propiedad.

## Implementación en Power BI

###  Conexión a MySQL
Para conectar Power BI a MySQL, se utilizó el conector nativo de Power BI para bases de datos MySQL. Se siguieron estos pasos:
1. Abrir Power BI Desktop.
2. Seleccionar "Obtener datos" > "Base de datos" > "MySQL".
3. Ingresar las credenciales y la información de la base de datos proporcionada por la inmobiliaria.
4. Importar las tablas relevantes: Inquilinos, Propiedades, Contratos, Publicaciones.

### Creación de Medidas y Columnas Calculadas
Para cada KPI, se crearon medidas y columnas calculadas utilizando el lenguaje DAX (Data Analysis Expressions).



###  Conexión de Power BI a MySQL en Google Cloud

1. **Abrir Power BI Desktop**
   - Inicia Power BI Desktop en tu ordenador.

2. **Seleccionar la Fuente de Datos**
   - En la pestaña **Inicio**, selecciona **Obtener datos**.
   - Elige **Base de datos** y luego selecciona **MySQL**.

3. **Ingresar la Información de Conexión**
   - Introduce el nombre del servidor MySQL de Google Cloud (generalmente en formato `ip_address:port` o `instance_name`).
   - Introduce el nombre de la base de datos, el nombre de usuario y la contraseña.

4. **Conectar y Cargar los Datos**
   - Haz clic en **Conectar**.
   - Power BI te pedirá autenticarte; ingresa las credenciales correspondientes.
   - Selecciona las tablas que deseas importar a Power BI y haz clic en **Cargar**.


## Conclusiones con la Implementación de FindEdén®

Desde EdenFornia Solutions®, se propone abordar las problemáticas identificadas en la gestión de propiedades inmobiliarias con la creación de la aplicación FindEdén®. FindEdén® integrará en su plataforma una metodología centrada en el cliente, basada en las filosofías de bienestar, utilizando un enfoque holístico. Esta aplicación ofrecerá recomendaciones de propiedades no solo basadas en los criterios clásicos, sino también en factores clave del bienestar humano, asegurando que los usuarios encuentren un hogar que realmente se adapte a su estilo de vida y promueva su bienestar integral.

FindEdén® se anexará a las bases de datos y motores de búsqueda convencionales de los servicios inmobiliarios. El usuario ingresará a la aplicación y, a partir de una serie de preguntas relacionadas a sus preferencias y modos de vida, y en conjunto con nuestra base de datos de reseñas, puntuará del 1 al 10 los inmuebles que ofrece la empresa. Los valores más altos indicarán un mayor grado de conexión entre el inmueble y las preferencias y modo de vida del usuario.

## Conclusiones por Métricas con FindEdén®

###  Tiempo Promedio de Vacancia
**Conclusión con FindEdén®**: Con FindEdén®, se espera una reducción significativa en el tiempo promedio de vacancia. Al proporcionar recomendaciones personalizadas basadas en las preferencias y el bienestar de los inquilinos, las propiedades estarán mejor alineadas con las necesidades de los usuarios, facilitando así la rápida ocupación.

###  Índice de Satisfacción del Cliente
**Conclusión con FindEdén®**: El índice de satisfacción del cliente aumentará considerablemente con la implementación de FindEdén®. Al enfocarse en factores de bienestar y ofrecer propiedades que realmente se adapten al estilo de vida de los inquilinos, se incrementará la satisfacción general, llevando a una mayor retención de inquilinos y recomendaciones positivas.

### Índice de Renovación de Contratos
**Conclusión con FindEdén®**: FindEdén® contribuirá a un aumento en el índice de renovación de contratos. Los inquilinos que encuentran propiedades alineadas con su bienestar y preferencias están más propensos a renovar sus contratos, reduciendo así la rotación y aumentando la estabilidad para la inmobiliaria.

###  Índice de Conversión de Prospectos a Inquilinos
**Conclusión con FindEdén®**: El índice de conversión de prospectos a inquilinos mejorará significativamente. FindEdén® facilitará una experiencia de búsqueda más intuitiva y personalizada, lo que atraerá a más prospectos y los convertirá en inquilinos satisfechos, mejorando la efectividad de las estrategias de marketing y ventas.

###  Nivel de Desocupación
**Conclusión con FindEdén®**: El nivel de desocupación se reducirá. FindEdén® permitirá que las propiedades sean vistas por usuarios que están activamente buscando un hogar que cumpla con sus necesidades de bienestar, incrementando las posibilidades de ocupación y reduciendo el número de propiedades desocupadas.
