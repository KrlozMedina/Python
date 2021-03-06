# Imports necesarios
import numpy as np
import pandas as pd
import seaborn as sb
import matplotlib.pyplot as plt
#%matplotlib inline
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
plt.rcParams['figure.figsize'] = (16, 9)
plt.style.use('ggplot')
from sklearn import linear_model
from sklearn.metrics import mean_squared_error, r2_score

####################################################################################################

#cargamos los datos de entrada
data = pd.read_csv("./weather_features.csv")
#veamos cuantas dimensiones y registros contiene
print(data.shape)
print(data.head())
print(data.describe())

####################################################################################################

# Visualizamos rápidamente las caraterísticas de entrada
data.drop(['clouds_all', 'rain_1h', 'rain_3h', 'snow_3h', 'temp_max', 'temp_min', 'weather_id', 'wind_deg'],1).hist()
plt.show()

####################################################################################################

colores=['orange','blue']
tamanios=[30,60]

f1 = data['temp'].values
f2 = data['wind_speed'].values

# Vamos a pintar en colores los puntos por debajo y por encima de la media de Cantidad de Palabras
plt.scatter(f1, f2)
plt.show()

####################################################################################################


# Vamos a RECORTAR los datos en la zona donde se concentran más los puntos
# esto es en el eje X: entre 0 y 3.500
# y en el eje Y: entre 0 y 80.000
filtered_data = data[(data['temp'] >= 275) &
                     (data['temp'] <= 305) &
                     (data['wind_speed'] <=20)]

colores=['orange','blue']
tamanios=[30,60]

f1 = filtered_data['temp'].values
f2 = filtered_data['wind_speed'].values

# Vamos a pintar en colores los puntos por debajo y por encima de la media de Cantidad de Palabras
asignar=[]
for index, row in filtered_data.iterrows():
    if(row['wind_speed']>20):
        asignar.append(colores[0])
    else:
        asignar.append(colores[1])
    
plt.scatter(f1, f2, c=asignar, s=tamanios[0])
plt.show()

####################################################################################################

filtered_data = data[(data['temp'] >= 275) &
                     (data['temp'] <= 305) &
                     (data['wind_speed'] <=20) &
                     (data['wind_speed'] >= 12.5)]

colores=['orange','blue']
tamanios=[30,60]

f1 = filtered_data['temp'].values
f2 = filtered_data['wind_speed'].values

# Vamos a pintar en colores los puntos por debajo y por encima de la media de Cantidad de Palabras
asignar=[]
for index, row in filtered_data.iterrows():
    if(row['wind_speed']>20):
        asignar.append(colores[0])
    else:
        asignar.append(colores[1])
    
plt.scatter(f1, f2, c=asignar, s=tamanios[0])
plt.show()

####################################################################################################

# Asignamos nuestra variable de entrada X para entrenamiento y las etiquetas Y.
dataX =filtered_data[["temp"]]
X_train = np.array(dataX)
y_train = filtered_data['wind_speed'].values

# Creamos el objeto de Regresión Linear
regr = linear_model.LinearRegression()

# Entrenamos nuestro modelo
regr.fit(X_train, y_train)

# Hacemos las predicciones que en definitiva una línea (en este caso, al ser 2D)
y_pred = regr.predict(X_train)

# Veamos los coeficienetes obtenidos, En nuestro caso, serán la Tangente
print('Coefficients: \n', regr.coef_)
# Este es el valor donde corta el eje Y (en X=0)
print('Independent term: \n', regr.intercept_)
# Error Cuadrado Medio
print("Mean squared error: %.2f" % mean_squared_error(y_train, y_pred))
# Puntaje de Varianza. El mejor puntaje es un 1.0
print('Variance score: %.2f' % r2_score(y_train, y_pred))

####################################################################################################

#Vamos a comprobar:
# Quiero predecir cuántos "Shares" voy a obtener por un artículo con 2.000 palabras,
# según nuestro modelo, hacemos:
y_Dosmil = regr.predict([[285]])
print(int(y_Dosmil))

####################################################################################################

import numpy as np
import matplotlib.pyplot as plt
x = np.arange(275,310,0.1)
y1=regr.coef_*x+regr.intercept_
plt.plot(x, y1)
plt.scatter(f1, f2, c=asignar, s=tamanios[0])
plt.show() 

####################################################################################################

#Vamos a comprobar:
# Quiero predecir cuántos "Shares" voy a obtener por un artículo con 2.000 palabras,
# según nuestro modelo, hacemos:
y_Dosmil = regr.predict([[285]])
print(int(y_Dosmil))

####################################################################################################
