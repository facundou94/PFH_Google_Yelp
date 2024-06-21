<h1 align="center"> PROYECTO FINAL HENRY: GOOGLE - YELP  </h1>
<h3 align="center"> Equipo de trabajo: Camino Federico, Londero Walter, Pizarro Hernan, Urteaga Facundo, Veron Cintia </h3>

<p align="left">
   <img src="https://img.shields.io/badge/ESTADO-EN%20DESAROLLO-green">
   </p>

## Índice

*[Descripción del proyecto](#descripción_del_proyecto)

*[Introducción](#introducción)

*[Situación problemática](#situación_problemática)

*[Propuesta de trabajo](#propuesta_de_trabajo)

*[Características de los datos](#características_de_los_datos)

*[Plan de trabajo](#plan_de_trabajo)


# Descripción del proyecto solicitado

# Contexto

<p align="justify">
"La opinión de los usuarios es un dato muy valioso, que crece día a día gracias a plataformas de reseñas. Su análisis puede ser determinante para la planificación de estratenias. Yelp es una plataforma de reseñas de todo tipo de negocios, restaurantes, hoteles, servicios entre otros. Los usuarios utilizan el servicio y luego suben su reseña según la experiencia que han recibido. Esta información es muy valiosa para las empresas, ya que les sirve para enterarse de la imagen que tienen los usuarios de los distintos locales de la empresa, siendo útil para medir el desempeño, utilidad del local, además de saber en qué aspectos hay que mejorar el servicio. Además, Google posee una plataforma de reseñas de todo tipo de negocios, restaurantes, hoteles, servicios, entre otros integrada en su servicio de localización y mapas, Google Maps. Los usuarios utilizan el servicio y luego suben su reseña según la experiencia vivida. Muchos usuarios leen las reseñas de los lugares a los que planean ir para tomar decisiones sobre dónde comprar, comer, dormir, reunirse, etc. Esta información es muy valiosa para las empresas, ya que les sirve para enterarse de la imagen que tienen los usuarios de los distintos locales de la empresa, siendo muy útil para medir el desempeño, utilidad del local, además de identificar los aspectos del servicio a mejorar."
</p>

# Propuesta de trabajo

<p align="justify">
Recopilar, depurar y disponibilizar la información: Creación de una base de datos (DataWarehouse) de diferentes fuentes, tanto provistas por Henry como incorporadas por ustedes, corriendo en local o alojada en proveedores en la nube. La base de datos depurada deberá contemplar por lo menos dos tipos diferentes de extracción de datos, ejemplo: datos estáticos, llamadas a una API, scrapping, entre otros.
Reporte y análisis significativos de la(s) línea(s) de investigación escogidas: El análisis debe contemplar las relaciones entre variables y concluir, si es que existe, una relación entre estas, y los posibles factores que causan dicha relación en la realidad.
Entrenamiento y puesta en producción de un modelo de machine learning de clasificación no supervisado o supervisado: El modelo debe resolver un problema y conectar globalmente con los objetivos propuestos que se propongan como proyecto.
</p>

## Características de las muestras

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
