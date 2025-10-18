# Importar librerías
from scipy.integrate import odeint
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


# Cargar datos (el separador es "|")
colegios = pd.read_csv("colegios.csv", sep="|")
archivo_precipitaciones_read = pd.read_csv('precipitaciones_7.csv')

# Filtrar Región del Maule (código 7)
coleg_maule = colegios[colegios['COD_REG_RB'] == 7].copy()

# Convertir fecha y filtrar año 2020
archivo_precipitaciones_read['FECHA'] = pd.to_datetime(
    archivo_precipitaciones_read['FECHA'],
    format='%d/%m/%Y', errors='coerce'
)
prec_2020 = archivo_precipitaciones_read[
    archivo_precipitaciones_read['FECHA'].dt.year == 2020
].copy()

# Sumar precipitaciones por comuna
prec_por_comuna = prec_2020.groupby('COMUNA')['Precipitación_diaria'].sum().reset_index()
prec_por_comuna.rename(columns={'Precipitación_diaria': 'LLUVIA_2020_MM'}, inplace=True)

# Normalizar nombres de comuna
def norm(s):
    if pd.isna(s):
        return ''
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

# Ordenar por nivel de exposición
coleg_maule_prec = coleg_maule_prec.sort_values('LLUVIA_2020_MM', ascending=False)

# Seleccionar columnas relevantes
out_cols = ['RBD', 'NOM_RBD', 'NOM_COM_RB', 'COD_COM_RB', 'COD_REG_RB', 'LLUVIA_2020_MM']

# ===============================================================
# 📊 RESUMEN DE COLEGIOS EXPUESTOS A LLUVIAS EN LA REGIÓN DEL MAULE (2020)
# ===============================================================
total_colegios_maule = len(coleg_maule_prec)
colegios_con_dato = coleg_maule_prec['LLUVIA_2020_MM'].notna().sum()
lluvia_max = coleg_maule_prec['LLUVIA_2020_MM'].max()
lluvia_min = coleg_maule_prec['LLUVIA_2020_MM'].min()
lluvia_prom = coleg_maule_prec['LLUVIA_2020_MM'].mean()

print("==============================================")
print("📍 RESUMEN REGIÓN DEL MAULE – PRECIPITACIONES 2020")
print("==============================================")
print(f"Total de colegios en la región: {total_colegios_maule}")
print(f"Colegios con dato de precipitación: {colegios_con_dato}")
print(f"Lluvia máxima registrada: {lluvia_max:.1f} mm")
print(f"Lluvia mínima registrada: {lluvia_min:.1f} mm")
print(f"Lluvia promedio regional: {lluvia_prom:.1f} mm")
print("==============================================\n")

# Mostrar los 10 colegios más expuestos
print("🏫 Top 10 colegios más expuestos a precipitaciones en 2020:")
print(coleg_maule_prec[out_cols].head(100).to_string(index=False))
