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

</p>
EdenFornia Solutions es una empresa innovadora que ofrece soluciones informáticas y aplicaciones especializadas para el sector inmobiliario, aprovechando el poder de la ciencia de datos y sus tecnologías asociadas. Nos dedicamos a transformar la manera en que se gestionan y operan las propiedades mediante el análisis avanzado de datos, inteligencia artificial y aprendizaje automático. Nuestro enfoque holístico se centra en el bienestar de las personas, proporcionando herramientas que optimizan la toma de decisiones, mejoran la eficiencia operativa y aumentan la rentabilidad para nuestros clientes. En EdenFornia Solutions, combinamos nuestra experiencia en tecnología con un profundo conocimiento del mercado inmobiliario para ofrecer productos que no solo satisfacen las necesidades específicas de nuestros usuarios, sino que también promueven su bienestar y calidad de vida.
<p align="justify">

## Equipo de trabajo

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

Desde EdenFornia Solutions®, se propone abordar esta problemática con la creación de la aplicación FindEdén®, integrando en su plataforma una metodología centrada en el cliente, basada en las filosofías de bienestar mencionadas. Utilizando un enfoque holístico, FindEdén® ofrecerá recomendaciones de propiedades no solo basadas en los criterios clásicos, sino también en factores clave del bienestar humano, asegurando que los usuarios encuentren un hogar que realmente se adapte a su estilo de vida y promueva su bienestar integral. Esta aplicación se podrá anexar a las bases de datos y motores de búsqueda convencionales de los servicios inmobiliarios. El usuario ingresará a la aplicación, y a partir de una serie de preguntas relacionadas a sus preferencias y modos de vida, y en conjunto con nuestra base de datos de reseñas, puntuará del 1 al 10 los inmuebles que ofrece la empresa. Los valores mas altos indicarán un mayor grado de conexión entre el inmueble y las preferencias y modo de vida del usuario.

## Propuesta de valor

* **Plataforma Innovadora**: FindEden es una plataforma web que revolucionará la búsqueda de viviendas con recomendaciones basadas en el estilo de vida del cliente.

* **Tecnología Avanzada**: Utiliza técnicas de NLP y ML para integrar datos de reseñas y comportamientos de usuarios, proporcionando recomendaciones altamente personalizadas.

* **Experiencia del Usuario**: Garantiza una experiencia excepcional, ayudando a cada individuo a encontrar su propio Edén.

* **Impacto en el Mercado**: Potencia la toma de decisiones de los inquilinos, aumentando acuerdos firmados y mejorando la tasa de renovación de contratos en el sector inmobiliario.

# Características de los datos

</p>
Para garantizar la calidad y eficacia de la integración de los datos en un sistema de almacenamiento (ETL) para su posterior uso en la plataforma, es fundamental obtener una visión general de la estructura y el contenido de los datos. Esto incluye la creación de un diccionario de datos, la elaboración del Diagrama Entidad-Relación y la realización de análisis exploratorios de los datos (EDA). Debido a la variedad de instituciones, locales, servicios y lugares públicos que tienen reseñas, estos datos son una excelente fuente para nuestra aplicación, proporcionando información valiosa que puede ser aprovechada para mejorar nuestras recomendaciones y la experiencia del usuario.
<p align="justify">

# Plan de trabajo

</p>
En nuestro plan de trabajo, nos centramos en tres aspectos clave. Primero, asignamos roles dentro del equipo para aprovechar las habilidades individuales y definir claramente las responsabilidades. Luego, a partir de la metodología Agile, se definieron las actividades a realizar en tres Sprints y creamos un cronograma detallado utilizando Notion, lo que nos permitió establecer plazos realistas y mantenernos alineados con los objetivos. Por último, definimos nuestro stack tecnológico con base en las necesidades específicas de la aplicación, asegurándonos de seleccionar las herramientas adecuadas para el desarrollo eficiente y el rendimiento óptimo. Estas estrategias fueron fundamentales para coordinar nuestros esfuerzos y avanzar de manera estructurada hacia nuestros objetivos.
<p align="justify">

## Cronograma

## Stack Tecnológico

Mediant

* Tipo de muestras: CLP y SHAM
* Días de adquisición: 1, 2, 4 y 7
* Cantidad de muestras iniciales: 303
</p>
* Metodología de adquisición: Cada muestra es sub-dividida en "réplicas biológicas" que son depositadas cada una en un pozo o "well" del equipo. Cada una de estas wells puede ser adquirida o leída mas de una vez, obteniéndose así "réplicas técnicas". La cantidad de réplicas biológicas y técnicas por muestra es variable, llegando a un máximo de 3 de cada una. Es decir, en el caso mas extremo, una muestra podría ser replicada tres veces biológicamente, y cada una adquirida otras tres veces, llegando así a un número de nueve adquisiciones correspondientes a una misma muestra.
</p>

## Características y nomenclatura de los archivos

</p>
Los lenguajes utilizados para el procesamiento y el análisis de los espectros fueron pyhton y R. Los archivos están enumerados por orden de procesamiento. A excepción del primer archivo de pre-procesamiento, los archivos están nomenclados de la siguiente manera:
</p>

*x_alg_muestras_dias*

Donde

* _x: numeración_
* _alg: algoritmos utilizados, supervisados (s) o no supervisados (ns)_
* _muestras: cantidad de muestras, indicando si se usan las réplicas biológicas (m122) o las muestras ya promediadas (m51)_
* _dias: días utilizados para el análisis, todos (d1247) o solo días 2 y 4 (d24)_

## Pre-procesamiento

### Archivo: 1_preprocesamiento.R

El pre-procesamiento está compuesto por las siguientes etapas:

* Carga de los espectros y su metadata correspondiente

  <p align="center">
     <img src="Imagenes/1_pre_crudo.jpeg" width="400">
   </p>
   <p align="center">
     <em>Figura 1: Espectro cargado sin transformar</em>
   </p>

* <p align="justify"> Control de calidad de los espectros mediante el uso de un estimador robusto Q. A fines prácticos, este control de calidad filtra espectros ruidosos o con el espectro "planchado" debido al fenómeno de supresión iónica en la etapa de adquisición. </p>

* <p align="justify"> Transformación de los espectros. Transformación de intensidad mediante la función raíz cuadrada (sqrt), suavizado del espectro mediante la función "wavelet", detección y remoción de la linea de base y alineamiento de los espectros, en ese orden. </p>

   <p align="center">
   <img src='Imagenes/1_pre_baseline.jpg' width='400'>
   </p>
   <p align="center">
     <em>Figura 2: Detección de la linea de base</em>
   </p>
   
   <p align="center">
   <img src='Imagenes/1_pre_baseline_removed.jpg' width='400'>
   </p>
   <p align="center">
     <em>Figura 3: Espectro con la línea de base removida</em>
   </p>

* Se realiza un promediado de las réplicas técnicas y biológicas.

* <p align="justify">Extracción de picos preponderantes de cada espectro. Esto se logra definiendo un umbral a partir del cual se comienzan a detectar los picos. Este umbral se define a partir de dos veces la relación señal a ruido del espectro (SNR).</p>

   <p align="center">
   <img src='Imagenes/1_pre_snr.jpeg' width='400'>
   </p>
   <p align="center">
     <em>Figura 4: Espectro con la detección del nivel de ruido (en rojo) y la definición del umbral (en azul)</em>
   </p>

   <p align="center">
   <img src='Imagenes/1_pre_picos.jpeg' width='400'>
   </p>
   <p align="center">
     <em>Figura 5: Detección de picos por encima del umbral establecido</em>
   </p>

* <p align="justify">A partir de la detección de los picos en cada espectro, se crea la matriz de intensidad, las cual contiene en sus filas las muestras y en las columnas los picos detectados. Esta matriz también es sujeta a transformaciones para preservar los picos con mayor frecuencia de aparición en los espectros y eliminar los picos "extraños", ya que lo que buscamos en esta instancia es que las variables (en este caso los picos) aporten información al sistema para su posterior análisis. Se crea también la matriz dicotómica, la cual se origina a partir de la definición de un umbral en la matriz de intensidades que transforma los valores de los picos en 1 y 0 segun la presencia o ausencia de cada pico en cada muestra.</p>

   <p align="center">
   <img src='Imagenes/1_pre_matriz_grafica.jpeg' width='400'>
   </p>
   <p align="center">
     <em>Figura 6: Representación gráfica de la matriz de intensidades dicotómica. Las filas corresponden a las muestras y las columnas a los picos. El color celeste indica presencia del pico en esa muestra</em>
   </p>

   
* <p align="justify">Por último, guardar las matrices y los metadatos. Se obtienen matrices de intensidades y dicotómicas tanto para las muestras individuales (matriz de 51 filas x 218 columnas) como para las réplicas biológicas (matriz de 122 filas x 218 columnas)</p>

## Seguimiento de cantidad de muestras

* Muestras iniciales o réplicas técnicas: 303
* Réplicas técnicas luego de control de calidad: 297
   * Réplicas biológicas: 122
   * Réplicas biológicas de días 2 y 4: 107
      * Muestras biológicas independientes: 55
      * Muestras biológicas independientes de días 2 y 4: 43

## Algoritmos No Supervisados

El procedimiento para la realización de los algoritmos No Supervisados fue el siguiente:
   1) Elección de conjunto de muestras (Réplicas biológicas o muestras independientes)
   2) Elección de los tiempos de muestreo (Todos los días o solo los días 2 y 4)
   3) Por medio de la matriz dicotómica, se aplica la función *bindaranking* con la cual se obtienen los picos que mejor variabilidad aportan a partir de un factor que se ingresa como variable de entrada. Este factor puede ser CLP vs SHAM, o días por ejemplo.
   4) Se realizan simulaciones de los modelos variando la cantidad de X primeros picos del análisis realizado en (3) y los algoritmos de clustering. Se realizaron pruebas con kmeans, HKmeans y PAM.
   5) Una vez realizada la clasificación No Supervisada, se comparan los puntos clasificados con su etiqueta de interés real (CLP, SHAM).

Resultados:

   ### Archivo: 2_ns_m122_d1247

   <p align="center">
   <img src='Imagenes/2_ranking_picos.jpg' width='400'>
   </p>
   <p align="center">
     <em>Figura 7: Picos mas preponderantes seleccionados por el algoritmo bindaranking a partir del factor CLP vs SHAM</em>
   </p>

   <p align="center">
   <img src='Imagenes/2_CLP_vs_SHAM_kmeans.jpg' width='400'>
   </p>
   <p align="center">
     <em>Figura 8: Clustering - CLP vs SHAM - Días 1, 2, 4 y 7 - TOP 20 picos - Algoritmo: kmeans</em>
   </p>

   <p align="center">
   <img src='Imagenes/2_tasa_acierto_total.jpg' width='400'>
   </p>
   <p align="center">
     <em>Figura 9: Tasa de acierto total</em>
   </p>

   <p align="center">
   <img src='Imagenes/2_tasa_acierto_por_dia.jpg' width='400'>
   </p>
   <p align="center">
     <em>Figura 10: Tasa de acierto por día</em>
   </p>
   
   ### Archivo: 4_ns_m122_d24

   <p align="center">
   <img src='Imagenes/4_picos_4clusters.jpeg' width='400'>
   </p>
   <p align="center">
     <em>Figura 11: Picos mas preponderantes seleccionados por el algoritmo bindaranking a partir del factor CLP_D2 vs CLP_D4 vs SHAM_D4 vs SHAM_D2</em>
   </p>

   <p align="center">
   <img src='Imagenes/4_hkmeans_4_grupos.jpg' width='400'>
   </p>
   <p align="center">
     <em>Figura 12: Clustering - CLP vs SHAM - Días 2 y 4 - TOP 30 picos - Algoritmo: Hkmeans</em>
   </p>

   <p align="center">
   <img src='Imagenes/4_kmeans_2_clusters_4_grupos.jpg' width='400'>
   </p>
   <p align="center">
     <em>Figura 12: Clustering - CLP vs SHAM - Días 2 y 4 - TOP 15 picos - Algoritmo: kmeans</em>
   </p>

   <p align="center">
   <img src='Imagenes/4_kmeans_top10.jpg' width='400'>
   </p>
   <p align="center">
     <em>Figura 13: Clustering - CLP vs SHAM - Días 2 y 4 - TOP 10 picos - Algoritmo: kmeans</em>
   </p>

   <p align="center">
   <img src='Imagenes/4_pam_2_clusters_4_grupos.jpg' width='400'>
   </p>
   <p align="center">
     <em>Figura 14: Clustering - CLP vs SHAM - Días 2 y 4 - TOP 20 picos - Algoritmo: PAM</em>
   </p>

   <p align="center">
   <img src='Imagenes/4_pam_3_clusters_4_grupos.jpg' width='400'>
   </p>
   <p align="center">
     <em>Figura 15: Clustering - CLP vs SHAM - Días 2 y 4 - 3 clusters - TOP 20 picos - Algoritmo: PAM</em>
   </p>

   <p align="center">
   <img src='Imagenes/4_pam_3_grupos_3_clusters.jpg' width='400'>
   </p>
   <p align="center">
     <em>Figura 16: Clustering - CLP vs SHAM - Días 2 y 4 - 3 clusters - TOP 30 picos - Algoritmo: PAM</em>
   </p>

   <p align="center">
   <img src='Imagenes/4_pam_top10.jpg' width='400'>
   </p>
   <p align="center">
     <em>Figura 17: Clustering - CLP vs SHAM - Días 2 y 4 - TOP 10 picos - Algoritmo: PAM</em>
   </p>
   

   ### Archivo: 5_ns_m51_d24

   <p align="center">
   <img src='Imagenes/5_picos.jpg' width='400'>
   </p>
   <p align="center">
     <em>Figura 18:  Picos mas preponderantes seleccionados por el algoritmo bindaranking a partir del factor CLP_D2 vs CLP_D4 vs SHAM</em>
   </p>

   <p align="center">
   <img src='Imagenes/5_pam_3clusters.jpg' width='400'>
   </p>
   <p align="center">
     <em>Figura 19: Clustering - CLP_D2 vs CLP_D4 vs SHAM - TOP 15 picos - 3 CLUSTERS - Algoritmo: PAM</em>
   </p>
   
   
   ### Archivo: 6_ns_m51_vs_varios

   <p align="center">
   <img src='Imagenes/6_picos_clpd2d4.jpg' width='400'>
   </p>
   <p align="center">
     <em>Figura 20: Picos mas preponderantes seleccionados por el algoritmo bindaranking a partir del factor CLP_D2 vs CLP_D4</em>
   </p>

   <p align="center">
   <img src='Imagenes/6_pam_clp_d2d4.jpg' width='400'>
   </p>
   <p align="center">
     <em>Figura 21:  Clustering - CLP_D2 vs CLP_D4 - TOP 15 picos - 2 CLUSTERS - Algoritmo: PAM</em>
   </p>

   <p align="center">
   <img src='Imagenes/6_picos_clp_sham_d2.jpg' width='400'>
   </p>
   <p align="center">
     <em>Figura 22: Picos mas preponderantes seleccionados por el algoritmo bindaranking a partir del factor CLP_D2 vs SHAM_D2</em>
   </p>

   <p align="center">
   <img src='Imagenes/6_pam_clp_sham_d2.jpg' width='400'>
   </p>
   <p align="center">
     <em>Figura 23:  Clustering - CLP_D2 vs SHAM_D2 - TOP 20 picos - 2 CLUSTERS - Algoritmo: PAM</em>
   </p>

   <p align="center">
   <img src='Imagenes/6_picos_clp_sham_d4.jpg' width='400'>
   </p>
   <p align="center">
     <em>Figura 24: Picos mas preponderantes seleccionados por el algoritmo bindaranking a partir del factor CLP_D4 vs SHAM_D4</em>
   </p>

   <p align="center">
   <img src='Imagenes/6_pam_clp_sham_d4.jpg' width='400'>
   </p>
   <p align="center">
     <em>Figura 25:  Clustering - CLP_D4 vs SHAM_D4 - TOP 15 picos - 2 CLUSTERS - Algoritmo: PAM</em>
   </p>
   
## Algoritmos Supervisados

   ### Archivo: 3_s_m122_d1247.R

   Se probaron modelos de aprendizaje supervisado con las 122 réplicas biológicas correspondiente a todos los días.
   
   1) <p align="justify">Se cargó la matriz dicotómica de 122 réplicas biológicas x 218 picos y se dividieron las muestras en grupo de entrenamiento y grupo de testeo bajo una relación de 60% entrenamiento y 40% testeo.</p>
   2) <p align="justify">Se seleccionan los 20 picos mas preponderantes mediante el algoritmo *bindaranking* bajo el factor CLP/SHAM con el propósito de reducir la cantidad de predictores.</p>
   3) Se entrenaron los siguientes modelos:
         * Binda (Binary Discriminant Analysis)
         * Random Forest
         * kNN (k nearest neighbor)
         * SVM Radial (Support Vector Machine con kernel radial)
   4) Se realizan las predicciones y a partir de ellas se generan las curvas ROC para cada modelo.

   <p align="center">
   <img src='Imagenes/3_sup_curvasROC.jpg' width='400'>
   </p>
   <p align="center">
     <em>Figura 26:  Curvas ROC para cada modelo de entrenamiento y valores de AUC (Área bajo la curva)</em>
   </p>

   ### Archivo: 7_s_m107_d24_top15.ipynb

   Se probaron modelos de aprendizaje supervisado con 107 réplicas biológicas correspondiente a los días 2 y 4.

   1) <p align="justify">Se representaron los porcentajes de muestras correspondiente a cada tipo de factor (CLP_D2, CLP_D4 y SHAM)</p>
   2) <p align="justify">Se entrenó un modelo de Regresión Logística</p>

      *Regresión Logística - accuracy score: 86%*

   <p align="center">
   <img src='Imagenes/7_matriz_confusion_reglog.JPG' width='400'>
   </p>
   <p align="center">
     <em>Figura 27:  Matriz de confusión de la Regresión Logística</em>
   </p>
   
   3) <p align="justify">Se entrenó un modelo de Random Forest</p>

      *Random Forest- accuracy score: 72% (A partir de validación cruzada con k=5)*

   <p align="center">
   <img src='Imagenes/7_picos_rf.JPG' width='400'>
   </p>
   <p align="center">
     <em>Figura 28:  Preponderancia de predictores del Random Forest</em>
   </p>

   <p align="center">
   <img src='Imagenes/7_arbol_decision.jpg' width='400'>
   </p>
   <p align="center">
     <em>Figura 29:  Arbol de decisión del Random Forest</em>
   </p>

## Conclusión
