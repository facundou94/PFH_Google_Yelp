# Proyecto final HENRY
# ML_2_FC_1
# Generación de predicciones del primer conjunto de locales (pocos meses con reseñas)


#### 1. Carga de librerías

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore') # Para evitar los molestos avisos.
from sklearn.metrics import mean_absolute_error, mean_squared_error, mean_absolute_percentage_error
from statsmodels.tsa.statespace.sarimax import SARIMAX
from itertools import product

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

#### 4. Filtro los locales con mas de 30 reviews mensuales

gmap_muchos = gmap_counts[gmap_counts['counts'] > 30]
gmap_muchos.head()

#### 5. Implemento el algoritmo definido: Simple Exponential Smoothing con alpha 0.1

# Definir los hiperparámetros seleccionados
order = (1, 1, 2)
seasonal_order = (0, 0, 0, 12)

# Lista para almacenar los resultados de los últimos tres ratings y las predicciones
all_predictions = []

# Iterar sobre cada gmap_id en gmap_muchos
for gmap_id in gmap_muchos['gmap_id']:
    # Filtrar las reviews correspondientes de monthly_reviews
    df = monthly_reviews[monthly_reviews['gmap_id'] == gmap_id][['month', 'rating']]
    
    # Convertir el índice de Period a Timestamp
    #df['month'] = df['month'].dt.to_timestamp()
    
    # Renombrar columnas
    df.rename(columns={'month': 'ds', 'rating': 'y'}, inplace=True)
    
    # Dividir los datos en entrenamiento y prueba (80% entrenamiento, 20% prueba)
    train_size = int(len(df) * 0.8)
    train, test = df.iloc[:train_size], df.iloc[train_size:]
    
    if len(train) < 3 or len(test) < 1:
        print(f"Not enough data for gmap_id {gmap_id}")
        continue
    
    # Ajustar el modelo SARIMAX con los hiperparámetros seleccionados
    try:
        model = SARIMAX(train['y'], order=order, seasonal_order=seasonal_order, enforce_stationarity=False, enforce_invertibility=False)
        model_fit = model.fit(disp=False)
        
        # Realizar predicciones en el conjunto de prueba
        forecast = model_fit.forecast(steps=len(test))
        
        # Aplicar límite a las predicciones entre 1 y 5
        forecast = np.clip(forecast, 1, 5)

        # Evaluar el rendimiento del modelo
        mae = mean_absolute_error(test['y'], forecast)
        rmse = np.sqrt(mean_squared_error(test['y'], forecast))
        mape = mean_absolute_percentage_error(test['y'], forecast)
        
        # Obtener los últimos tres ratings y las predicciones para los siguientes tres meses
        last_three_ratings = test['y'].iloc[-3:].tolist()
        next_three_forecast = model_fit.forecast(steps=3).tolist()
        
        # Guardar los resultados
        all_predictions.append({
            'gmap_id': gmap_id,
            'last_three_ratings': last_three_ratings,
            'next_three_forecast': next_three_forecast,
            'mae': mae,
            'rmse': rmse,
            'mape': mape
        })
        
    except Exception as e:
        print(f"Failed to fit SARIMAX model for gmap_id {gmap_id}: {e}")

# Convertir los resultados a un DataFrame
all_predictions_df = pd.DataFrame(all_predictions)

all_predictions_df = all_predictions_df[["gmap_id","last_three_ratings","next_three_forecast"]]
# Redondear los valores dentro de las listas
all_predictions_df['last_three_ratings'] = all_predictions_df['last_three_ratings'].apply(lambda x: [round(elem, 2) for elem in x])
all_predictions_df['next_three_forecast'] = all_predictions_df['next_three_forecast'].apply(lambda x: [round(elem, 2) for elem in x])

all_predictions_df

#### 6. Guardo las predicciones en un csv

all_predictions_df.to_csv('fc_results_3.csv', index=False)