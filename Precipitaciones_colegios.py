# Importar librerias
from scipy.integrate import odeint
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd



# Cargar datos (el separador es "|")
colegios = pd.read_csv("colegios.csv", sep="|")
archivo_precipitaciones_read = pd.read_csv('precipitaciones_7.csv')

# Filtrar Región del Maule (código 7 o nombre 'MAU')
coleg_maule = colegios[colegios['COD_REG_RB'] == 7].copy()


# Convertimos fecha
archivo_precipitaciones_read['FECHA'] = pd.to_datetime(archivo_precipitaciones_read['FECHA'], format='%d/%m/%Y', errors='coerce')
# Filtramos año 2020
prec_2020 = archivo_precipitaciones_read[archivo_precipitaciones_read['FECHA'].dt.year == 2020].copy()


# Sumar precipitaciones por comuna
prec_por_comuna = prec_2020.groupby('COMUNA')['Precipitación_diaria'].sum().reset_index()
prec_por_comuna.rename(columns={'Precipitación_diaria': 'LLUVIA_2020_MM'}, inplace=True)


# Normalizamos nombres de comuna para evitar errores por mayúsculas/minúsculas
def norm(s):
    if pd.isna(s): return ''
    return str(s).strip().upper()

coleg_maule['NOM_COM_RB_NORM'] = coleg_maule['NOM_COM_RB'].apply(norm)
prec_por_comuna['COMUNA_NORM'] = prec_por_comuna['COMUNA'].apply(norm)


# Merge colegios con precipitaciones
coleg_maule_prec = coleg_maule.merge(
    prec_por_comuna[['COMUNA_NORM', 'LLUVIA_2020_MM']],
    left_on='NOM_COM_RB_NORM',
    right_on='COMUNA_NORM',
    how='left'
)


# Ordenamos para ver los colegios más expuestos
coleg_maule_prec = coleg_maule_prec.sort_values('LLUVIA_2020_MM', ascending=False)


# Seleccionamos columnas relevantes para mostrar
out_cols = ['RBD', 'NOM_RBD', 'NOM_COM_RB', 'COD_COM_RB', 'COD_REG_RB', 'LLUVIA_2020_MM']
print(coleg_maule_prec[out_cols].head(20))  # top 20 colegios más expuestos

#print(archivo_precipitaciones_read)

# archivo_precipitaciones_array = np.array(archivo_precipitaciones_read)
# # print(archivo_precipitaciones_array[0])
# # rint(archivo_precipitaciones_array[0].size)


# numero_estacion = 7384002

# index = np.where(archivo_precipitaciones_array[:, 0] == numero_estacion)[0]
# # print(index)
# # print(archivo_precipitaciones_array[index[0], -3][-4:])
# primer_agno = int(archivo_precipitaciones_array[index[0], -3][-4:])
# ultimo_agno = int(archivo_precipitaciones_array[index[-1], -3][-4:])


# Lista_sumas = []
# for agno in range(primer_agno, ultimo_agno + 1):
#     #print(archivo_precipitaciones_array[index, -3])
#     index_agno = np.where([str(agno) in fecha for fecha in archivo_precipitaciones_array[index, -3]])[0]
#     # print(index_agno)
#     sumas = np.sum([float(x) for x in archivo_precipitaciones_array[index[index_agno], -2]])
#     Lista_sumas.append([agno, sumas])
# # print(Lista_sumas)


# Sumas_precipitaciones_array = np.array(Lista_sumas)

# print(Sumas_precipitaciones_array)

# # Graficar

# plt.plot(Sumas_precipitaciones_array[:, 0], Sumas_precipitaciones_array[:, 1], 'b')
# plt.xticks(np.arange(primer_agno, ultimo_agno + 1, 2))
# plt.legend(loc='best')
# plt.xlabel('Agnos')
# plt.ylabel('mm')
# plt.grid()
# plt.show()