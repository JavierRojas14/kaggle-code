"""Modulo que contiene funciones para entrenar modelos de Machine Learning con optimizacion
de hiperparametros. Ademas, muestra el desempeno de modelo de clasificacion
"""

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from sklearn.metrics import classification_report
from sklearn.model_selection import GridSearchCV


# Función para entrenar modelos
def entrenar_ensamble_de_modelos_gridcv(
    grilla_gridcv_con_modelos, X_train, X_test, y_train, y_test
):
    """
     Entrena un conjunto de modelos utilizando GridSearchCV y muestra los resultados de desempeño en
     un conjunto de prueba.

    :param grilla_gridcv_con_modelos: Una lista que contiene información sobre los modelos,
    parámetros de búsqueda y nombre del modelo.
    :type grilla_gridcv_con_modelos: list of dictionaries
    :param X_train: Variables independientes del conjunto de entrenamiento.
    :type X_train: array-like
    :param X_test: Variables independientes del conjunto de prueba.
    :type X_test: array-like
    :param y_train: Variable dependiente del conjunto de entrenamiento.
    :type y_train: array-like
    :param y_test: Variable dependiente del conjunto de prueba.
    :type y_test: array-like

    :returns: None
    """
    for model_info in grilla_gridcv_con_modelos:
        print("Training", model_info["nombre"], "...")
        model = model_info["modelo"]
        param_grid = model_info["param_grid"]

        grid_search = GridSearchCV(model, param_grid, cv=5)
        grid_search.fit(X_train, y_train)
        model_info["modelo"] = grid_search

        obtener_desempeno_modelo_en_grilla(grid_search, X_test, y_test)


def obtener_desempeno_modelo_en_grilla(modelo_grilla, X_test, y_test):
    """
    Muestra el desempeño de un modelo entrenado con GridSearchCV en un conjunto de prueba.

    :param modelo_grilla: Modelo entrenado con GridSearchCV.
    :type modelo_grilla: GridSearchCV object
    :param X_test: Variables independientes del conjunto de prueba.
    :type X_test: array-like
    :param y_test: Variable dependiente del conjunto de prueba
    :type y_test: array-like
    :returns: pandas DataFrame
    """
    print("--------------Resultados Conjunto de Entrenamiento-----------------")
    print("Los resultados en la busqueda de hiperparametros son:")
    resultados_grilla = analizar_resultados_grid_cv(modelo_grilla.cv_results_)
    plt.show()
    print(f"Los mejores parametros fueron: {modelo_grilla.best_params_}")
    print(f"El mejor desempeno fue: {modelo_grilla.best_score_}")

    print("\n\n--------------Resultados Conjunto de Validacion-----------------")
    yhat = modelo_grilla.predict(X_test)
    print("Los resultados en el conjunto de validacion son:")
    print(classification_report(y_test, yhat))

    print("---------------------------------------------------------------------")

    return resultados_grilla


def resumir_resultados_grid_cv(diccionario_resultados):
    """
    Toma un diccionario de resultados de GridSearchCV y genera un DataFrame resumido con los
    resultados.

    :param diccionario_resultados: Diccionario de resultados devuelto por el atributo `cv_results_`
    de GridSearchCV.
    :type diccionario_resultados: dictionary
    :returns: pandas DataFrame
    """
    df_resultados = pd.DataFrame(diccionario_resultados)
    df_resultados["params_str"] = df_resultados["params"].astype(str)

    return df_resultados


def graficar_resultados_grid_cv(resultado_df):
    """
    Grafica los resultados de GridSearchCV en un gráfico de líneas.

    :param resultado_df: DataFrame que contiene los resultados de GridSearchCV.
    :type resultado_df: pandas DataFrame
    :returns: None
    """
    sns.lineplot(data=resultado_df, x="params_str", y="mean_test_score", marker="o")
    plt.tick_params(axis="x", labelrotation=90)


def analizar_resultados_grid_cv(diccionario_resultados):
    """
    Toma un diccionario de resultados de GridSearchCV, resume los resultados y los grafica en un
    gráfico de líneas.

    :param diccionario_resultados: Diccionario de resultados devuelto por el atributo `cv_results_`
    de GridSearchCV.
    :type diccionario_resultados: dictionary
    :returns: pandas DataFrame
    """
    df_resultados = resumir_resultados_grid_cv(diccionario_resultados)
    graficar_resultados_grid_cv(df_resultados)

    return df_resultados
