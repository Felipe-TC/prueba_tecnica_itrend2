import numpy as np
import pandas as pd

def lluvia_acumulada_anual(codigo_estacion):
    archivo_precipitaciones_read = pd.read_csv('precipitaciones_7.csv')
    archivo_precipitaciones_array = np.array(archivo_precipitaciones_read)

    index = np.where(archivo_precipitaciones_array[:, 0] == codigo_estacion)[0]

    primer_agno = int(archivo_precipitaciones_array[index[0], -3][-4:])
    ultimo_agno = int(archivo_precipitaciones_array[index[-1], -3][-4:])

    Lista_sumas = []

    for agno in range(primer_agno, ultimo_agno + 1):
        index_agno = np.where([
            fecha.endswith(str(agno)) or str(agno) in fecha[-4:]
            for fecha in archivo_precipitaciones_array[index, -3]
        ])[0]

        # Convertir precipitaciones a float antes de sumar
        precipitaciones = [
            float(valor) for valor in archivo_precipitaciones_array[index[index_agno], -2]
        ]
        suma_anual = np.sum(precipitaciones)
        Lista_sumas.append([agno, suma_anual])

    return Lista_sumas


# Ejemplo de uso:
resultado = lluvia_acumulada_anual(7384002)
print(resultado)
