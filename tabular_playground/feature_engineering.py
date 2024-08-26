import numpy as np


def obtener_correlaciones_apiladas(correlaciones):
    # Filtra el triangulo superior de la matriz de correlacion
    bool_triangulo_superior = np.triu(np.ones_like(correlaciones, dtype=bool))
    correlaciones_filtradas = correlaciones.mask(bool_triangulo_superior)

    # Convierte las correlaciones a formato long y filtra las que no tengan valores
    correlaciones_apiladas = correlaciones_filtradas.unstack().dropna()

    return correlaciones_apiladas


def identificar_correlaciones_mayores(correlaciones_apiladas, limite=0.8):
    # Filtrar las auto-correlaciones y los pares por debajo del umbral
    pares_alta_corr = correlaciones_apiladas[(abs(correlaciones_apiladas) > limite)]

    # Convertir la serie a una lista de tuplas
    lista_pares_alta_corr = [(index[0], index[1], corr) for index, corr in pares_alta_corr.items()]

    return lista_pares_alta_corr
