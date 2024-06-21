<h1 align="center"> PROYECTO FINAL HENRY: GOOGLE - YELP  </h1>
<h3 align="center"> Equipo de trabajo: Camino Federico, Londero Walter, Pizarro Hernan, Urteaga Facundo, Veron Cintia </h3>

   <p align="center">
   <img src='Imagenes/1_logo.JPG' width='400'>
   </p>

<p align="left">
   <img src="https://img.shields.io/badge/ESTADO-EN%20DESAROLLO-green">
   </p>

# Índice

*[Descripción del proyecto](#descripción_del_proyecto)

*[Introducción](#introducción)

*[Situación problemática](#situación_problemática)

*[Propuesta de trabajo](#propuesta_de_trabajo)

*[Características de los datos](#características_de_los_datos)

*[Plan de trabajo](#plan_de_trabajo)


# Descripción del proyecto solicitado

## Contexto

<p align="justify">
La opinión de los usuarios es un dato muy valioso, que crece día a día gracias a plataformas de reseñas. Su análisis puede ser determinante para la planificación de estratenias. Yelp es una plataforma de reseñas de todo tipo de negocios, restaurantes, hoteles, servicios entre otros. Los usuarios utilizan el servicio y luego suben su reseña según la experiencia que han recibido. Esta información es muy valiosa para las empresas, ya que les sirve para enterarse de la imagen que tienen los usuarios de los distintos locales de la empresa, siendo útil para medir el desempeño, utilidad del local, además de saber en qué aspectos hay que mejorar el servicio. Además, Google posee una plataforma de reseñas de todo tipo de negocios, restaurantes, hoteles, servicios, entre otros integrada en su servicio de localización y mapas, Google Maps. Los usuarios utilizan el servicio y luego suben su reseña según la experiencia vivida. Muchos usuarios leen las reseñas de los lugares a los que planean ir para tomar decisiones sobre dónde comprar, comer, dormir, reunirse, etc. Esta información es muy valiosa para las empresas, ya que les sirve para enterarse de la imagen que tienen los usuarios de los distintos locales de la empresa, siendo muy útil para medir el desempeño, utilidad del local, además de identificar los aspectos del servicio a mejorar.
</p>

## Trabajo a realizar

<p align="justify">
Recopilar, depurar y disponibilizar la información: Creación de una base de datos (DataWarehouse) de diferentes fuentes, tanto provistas por Henry como incorporadas por ustedes, corriendo en local o alojada en proveedores en la nube. La base de datos depurada deberá contemplar por lo menos dos tipos diferentes de extracción de datos, ejemplo: datos estáticos, llamadas a una API, scrapping, entre otros.
Reporte y análisis significativos de la(s) línea(s) de investigación escogidas: El análisis debe contemplar las relaciones entre variables y concluir, si es que existe, una relación entre estas, y los posibles factores que causan dicha relación en la realidad.
Entrenamiento y puesta en producción de un modelo de machine learning de clasificación no supervisado o supervisado: El modelo debe resolver un problema y conectar globalmente con los objetivos propuestos que se propongan como proyecto.
</p>

# Introducción

## Quiénes somos

   <p align="center">
   <img src='Imagenes/2_logo_empresa.JPG' width='400'>
   </p>
   
</p>
EdenFornia Solutions es una empresa innovadora que ofrece soluciones informáticas y aplicaciones especializadas para el sector inmobiliario, aprovechando el poder de la ciencia de datos y sus tecnologías asociadas. Nos dedicamos a transformar la manera en que se gestionan y operan las propiedades mediante el análisis avanzado de datos, inteligencia artificial y aprendizaje automático. Nuestro enfoque holístico se centra en el bienestar de las personas, proporcionando herramientas que optimizan la toma de decisiones, mejoran la eficiencia operativa y aumentan la rentabilidad para nuestros clientes. En EdenFornia Solutions, combinamos nuestra experiencia en tecnología con un profundo conocimiento del mercado inmobiliario para ofrecer productos que no solo satisfacen las necesidades específicas de nuestros usuarios, sino que también promueven su bienestar y calidad de vida.
<p align="justify">

## Equipo de trabajo

   <p align="center">
   <img src='Imagenes/3_equipo.JPG' width='400'>
   </p>
   
</p>
Nuestro equipo de trabajo en EdenFornia Solutions está conformado por un grupo interdisciplinario con experiencia en programación, ingeniería de software y relaciones humanas. Contamos con desarrolladores expertos en algoritmos de machine learning, ingenieros especializados en sistemas escalables y profesionales en gestión de relaciones con el cliente, todos trabajando en conjunto para ofrecer soluciones innovadoras y centradas en el bienestar de nuestros usuarios.
<p align="justify">

# Situación problemática

## Generalidades

</p>
En el mercado inmobiliario actual, la búsqueda de inmuebles para compra o alquiler se basa predominantemente en criterios clásicos como el precio, la ubicación, el tamaño y las características físicas de la propiedad. Sin embargo, estos criterios no consideran de manera integral los aspectos fundamentales del bienestar humano que son cruciales para la calidad de vida de los individuos. Esta carencia en la evaluación de propiedades puede llevar a decisiones de vivienda que no satisfacen plenamente las necesidades personales de los residentes.
La filosofía del bienestar, promovida por enfoques como el Well-being Index de la OECD y el modelo de Wellness en salud pública, resalta la importancia de factores adicionales que influyen en el bienestar integral. Estos incluyen la proximidad a servicios de salud, oportunidades recreativas, acceso a educación, seguridad, transporte y calidad ambiental, entre otros. A menudo, estos factores son ignorados en las plataformas inmobiliarias tradicionales.
<p align="justify">

## Contexto: Estado de California

</p>
Un informe reciente del California Health Care Foundation (CHCF) subraya los desafíos que enfrentan los residentes del estado en relación con la vivienda y el bienestar. El estudio revela que, a pesar de tener acceso a viviendas asequibles, muchos californianos experimentan una baja calidad de vida debido a la falta de acceso a servicios esenciales como atención médica, opciones recreativas y transporte público eficiente. Estos factores han sido identificados como críticos para el bienestar general de los residentes.
Por ejemplo, en áreas urbanas como Los Ángeles y San Francisco, la proximidad a parques y centros recreativos está directamente relacionada con niveles más altos de satisfacción personal y salud física. Sin embargo, en muchas comunidades, estos recursos no están adecuadamente distribuidos, lo que crea disparidades significativas en el bienestar.
<p align="justify">

# Propuesta de trabajo

## Aplicación FindEdén®

   <p align="center">
   <img src='Imagenes/4_logo_app.png' width='400'>
   </p>
   
Desde EdenFornia Solutions®, se propone abordar esta problemática con la creación de la aplicación FindEdén®, integrando en su plataforma una metodología centrada en el cliente, basada en las filosofías de bienestar mencionadas. Utilizando un enfoque holístico, FindEdén® ofrecerá recomendaciones de propiedades no solo basadas en los criterios clásicos, sino también en factores clave del bienestar humano, asegurando que los usuarios encuentren un hogar que realmente se adapte a su estilo de vida y promueva su bienestar integral. Esta aplicación se podrá anexar a las bases de datos y motores de búsqueda convencionales de los servicios inmobiliarios. El usuario ingresará a la aplicación, y a partir de una serie de preguntas relacionadas a sus preferencias y modos de vida, y en conjunto con nuestra base de datos de reseñas, puntuará del 1 al 10 los inmuebles que ofrece la empresa. Los valores mas altos indicarán un mayor grado de conexión entre el inmueble y las preferencias y modo de vida del usuario.

## Propuesta de valor

* **Plataforma Innovadora**: FindEden es una plataforma web que revolucionará la búsqueda de viviendas con recomendaciones basadas en el estilo de vida del cliente.

* **Tecnología Avanzada**: Utiliza técnicas de NLP y ML para integrar datos de reseñas y comportamientos de usuarios, proporcionando recomendaciones altamente personalizadas.

* **Experiencia del Usuario**: Garantiza una experiencia excepcional, ayudando a cada individuo a encontrar su propio Edén.

* **Impacto en el Mercado**: Potencia la toma de decisiones de los inquilinos, aumentando acuerdos firmados y mejorando la tasa de renovación de contratos en el sector inmobiliario.

   <p align="center">
   <img src='Imagenes/5_propuesta.JPG' width='400'>
   </p>
   
# Características de los datos

</p>
Para garantizar la calidad y eficacia de la integración de los datos en un sistema de almacenamiento (ETL) para su posterior uso en la plataforma, es fundamental obtener una visión general de la estructura y el contenido de los datos. Esto incluye la creación de un diccionario de datos, la elaboración del Diagrama Entidad-Relación y la realización de análisis exploratorios de los datos (EDA). Debido a la variedad de instituciones, locales, servicios y lugares públicos que tienen reseñas, estos datos son una excelente fuente para nuestra aplicación, proporcionando información valiosa que puede ser aprovechada para mejorar nuestras recomendaciones y la experiencia del usuario.
<p align="justify">

   <p align="center">
   <img src='Imagenes/6_calidad_google.JPG' width='400'>
   </p>

   <p align="center">
   <img src='Imagenes/7_calidad_yelp.JPG' width='400'>
   </p>
   
# Plan de trabajo

</p>
En nuestro plan de trabajo, nos centramos en tres aspectos clave. Primero, asignamos roles dentro del equipo para aprovechar las habilidades individuales y definir claramente las responsabilidades. Luego, a partir de la metodología Agile, se definieron las actividades a realizar en tres Sprints y creamos un cronograma detallado utilizando Notion, lo que nos permitió establecer plazos realistas y mantenernos alineados con los objetivos. Por último, definimos nuestro stack tecnológico con base en las necesidades específicas de la aplicación, asegurándonos de seleccionar las herramientas adecuadas para el desarrollo eficiente y el rendimiento óptimo. Estas estrategias fueron fundamentales para coordinar nuestros esfuerzos y avanzar de manera estructurada hacia nuestros objetivos.
<p align="justify">

## Cronograma

   <p align="center">
   <img src='Imagenes/8_notion.JPG' width='400'>
   </p>
   <p align="center">
   <em>Figura: Entorno de NOTION </em>
   </p>
   
## Stack Tecnológico

   <p align="center">
   <img src='Imagenes/9_stack.JPG' width='400'>
   </p>
   <p align="center">
     <em>Figura: Stack Tecnológico </em>
   </p>
