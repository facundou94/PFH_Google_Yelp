# Proyecto final HENRY
# ML_2_FC_1
# Generación de predicciones del primer conjunto de locales (pocos meses con reseñas)


#### 1. Carga de librerías

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore') # Para evitar los molestos avisos.
from statsmodels.tsa.holtwinters import SimpleExpSmoothing, Holt, ExponentialSmoothing
from sklearn.metrics import mean_absolute_error, mean_squared_error, mean_absolute_percentage_error

#### 2. Carga de datos

df_locales = pd.read_csv("locales_LA.csv")
df_reviews = pd.read_csv("reviews_LA.csv")

#### 3. Acondicionamiento de datos

# Para realizar un forecast correcto, debemos manejar los mismos intervalos de tiempo.
# Para esto, agrupamos las reviews en promedios mensuales para cada local.

# Asegurarse de que las fechas están en el formato correcto
df_reviews['date'] = pd.to_datetime(df_reviews['date'])

# Agrupar por gmap_id y mes, y calcular el promedio mensual
df_reviews['month'] = df_reviews['date'].dt.to_period('M')
monthly_reviews = df_reviews.groupby(['gmap_id', 'month']).agg({'rating': 'mean'}).reset_index()

# Contar la cantidad de ocurrencias de cada gmap_id
gmap_counts = monthly_reviews.groupby('gmap_id').size().reset_index(name='counts')

#### 4. Filtro los locales con menos de 16 reviews mensuales

gmap_pocos = gmap_counts[gmap_counts['counts'] < 16]
gmap_pocos.head()

#### 5. Implemento el algoritmo definido: Simple Exponential Smoothing con alpha 0.1

# Lista para almacenar los resultados
resultados_pocas = []

# Definir el valor de alpha
alpha = 0.1

# Iterar sobre cada gmap_id en gmap_pocos
for gmap_id in gmap_pocos['gmap_id']:
    # Filtrar las reviews correspondientes de monthly_reviews
    df = monthly_reviews[monthly_reviews['gmap_id'] == gmap_id].set_index('month')['rating']
    
    # Dividir los datos en entrenamiento y prueba (80% entrenamiento, 20% prueba)
    train_size = int(len(df) * 0.8)
    train, test = df.iloc[:train_size], df.iloc[train_size:]
    
    if len(train) < 3 or len(test) < 1:
        print(f"Not enough data for gmap_id {gmap_id}")
        continue
    
    # Ajustar el modelo SimpleExpSmoothing con el valor de alpha seleccionado
    try:
        model = SimpleExpSmoothing(train).fit(smoothing_level=alpha, optimized=False)
        forecast = model.forecast(steps=3)  # Predecir los próximos 3 meses
        
        # Aplicar límite a las predicciones entre 1 y 5
        forecast = np.clip(forecast, 1, 5)

        # Últimos tres ratings y tres predicciones
        last_three_ratings = train[-3:].tolist()
        predicted_three_ratings = forecast.round(2).tolist()  # Redondear las predicciones a 2 decimales
        
        # Guardar los resultados
        resultados_pocas.append({
            'gmap_id': gmap_id,
            'last_three_ratings': [round(rating, 2) for rating in last_three_ratings],  # Redondear los últimos tres ratings
            'predicted_three_ratings': predicted_three_ratings
        })
    except:
        print(f"Error fitting SimpleExpSmoothing model with alpha {alpha} for gmap_id {gmap_id}")
        continue

# Convertir los resultados a un DataFrame
forecast_results = pd.DataFrame(resultados_pocas)

#### 6. Guardo las predicciones en un csv

forecast_results.to_csv('fc_results_1.csv', index=False)