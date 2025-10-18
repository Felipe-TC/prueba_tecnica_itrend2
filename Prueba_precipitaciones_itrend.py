# Importar librerias
from scipy.integrate import odeint
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


archivo_precipitaciones_read = pd.read_csv('precipitaciones_7.csv')
#print(archivo_precipitaciones_read)

archivo_precipitaciones_array = np.array(archivo_precipitaciones_read)
# print(archivo_precipitaciones_array[0])
# rint(archivo_precipitaciones_array[0].size)


numero_estacion = 7384002

index = np.where(archivo_precipitaciones_array[:, 0] == numero_estacion)[0]
# print(index)
# print(archivo_precipitaciones_array[index[0], -3][-4:])
primer_agno = int(archivo_precipitaciones_array[index[0], -3][-4:])
ultimo_agno = int(archivo_precipitaciones_array[index[-1], -3][-4:])


Lista_sumas = []
for agno in range(primer_agno, ultimo_agno + 1):
    #print(archivo_precipitaciones_array[index, -3])
    index_agno = np.where([str(agno) in fecha for fecha in archivo_precipitaciones_array[index, -3]])[0]
    # print(index_agno)
    sumas = np.sum([float(x) for x in archivo_precipitaciones_array[index[index_agno], -2]])
    Lista_sumas.append([agno, sumas])
print(Lista_sumas)


