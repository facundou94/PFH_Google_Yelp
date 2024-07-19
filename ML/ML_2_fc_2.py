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
from statsmodels.tsa.arima.model import ARIMA
from itertools import product

#### 2. Carga de datos

df_locales = pd.read_csv("archivos/locales_LA.csv")
df_reviews = pd.read_csv("archivos/reviews_LA.csv")

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

#### 4. Filtro los locales con reviews mensuales entre 16 y 30

gmap_moderadas = gmap_counts.loc[(gmap_counts['counts'] >= 16) & (gmap_counts['counts'] <= 30)]
gmap_moderadas.head()

#### 5. Implemento el algoritmo definido: Simple Exponential Smoothing con alpha 0.1

# Implemento el el modelo ARIMA con uno de los conjuntos de hiperparámetros con mejor desempeño: (5,2,5)

import pandas as pd
import numpy as np
from statsmodels.tsa.arima.model import ARIMA
from sklearn.metrics import mean_absolute_error, mean_squared_error, mean_absolute_percentage_error
import matplotlib.pyplot as plt

# Lista para almacenar los resultados
resultados_moderadas = []

# Orden del modelo ARIMA
order = (1, 2, 0)

# Iterar sobre cada gmap_id en gmap_moderadas
for gmap_id in gmap_moderadas['gmap_id']:
    # Filtrar las reviews correspondientes de monthly_reviews
    df = monthly_reviews[monthly_reviews['gmap_id'] == gmap_id].set_index('month')['rating']
    
    # Convertir el índice de Period a Timestamp
    # df.index = df.index.to_timestamp()
    
    # Dividir los datos en entrenamiento y prueba (80% entrenamiento, 20% prueba)
    train_size = int(len(df) * 0.8)
    train, test = df.iloc[:train_size], df.iloc[train_size:]
    
    if len(train) < 3 or len(test) < 1:
        print(f"Not enough data for gmap_id {gmap_id}")
        continue
    
    # Ajustar el modelo ARIMA con el orden seleccionado
    try:
        model = ARIMA(train, order=order)
        model_fit = model.fit()
        forecast = model_fit.forecast(steps=3)  # Predecir los próximos 3 meses

        # Aplicar límite a las predicciones entre 1 y 5
        forecast = np.clip(forecast, 1, 5)
        
        # Últimos tres ratings y tres predicciones
        last_three_ratings = train[-3:].tolist()
        predicted_three_ratings = forecast.round(2).tolist()  # Redondear las predicciones a 2 decimales
        
        # Guardar los resultados
        resultados_moderadas.append({
            'gmap_id': gmap_id,
            'last_three_ratings': [round(rating, 2) for rating in last_three_ratings],  # Redondear los últimos tres ratings
            'predicted_three_ratings': predicted_three_ratings
        })
    except Exception as e:
        print(f"Error fitting ARIMA model with order {order} for gmap_id {gmap_id}: {e}")
        continue

# Convertir los resultados a un DataFrame
forecast_results = pd.DataFrame(resultados_moderadas)

#### 6. Guardo las predicciones en un csv

forecast_results.to_csv('fc_results_2.csv', index=False)