import os

import matplotlib
matplotlib.use("Agg")  # sin pantalla disponible al correr desde consola
import matplotlib.pyplot as plt
import pandas as pd
from scipy import stats

RUTA_ENTRADA = "resultados/experimento.csv"
RUTA_RESUMEN = "resultados/resumen.csv"
RUTA_GRAFICO_RPD = "resultados/comparacion_rpd.png"
RUTA_GRAFICO_TIEMPO = "resultados/comparacion_tiempo.png"

ORDEN_INSTANCIAS = ["ta001", "ta041", "ta071"]
ORDEN_METODOS = ["AG", "Memetico"]


def cargar_resultados():
    datos = pd.read_csv(RUTA_ENTRADA)
    # las instancias se ordenan de menor a mayor (20x5, 50x10, 100x10) en
    # vez de alfabéticamente, para que tablas y gráficos se lean de forma
    # consistente con el tamaño del problema.
    datos["instancia"] = pd.Categorical(datos["instancia"], categories=ORDEN_INSTANCIAS, ordered=True)
    datos["metodo"] = pd.Categorical(datos["metodo"], categories=ORDEN_METODOS, ordered=True)
    return datos


def calcular_resumen(datos):
    """Agrupa por instancia y método, y calcula estadísticas descriptivas
    de Cmax, RPD y tiempo de ejecución sobre las 30 semillas de cada
    combinación.
    """
    resumen = datos.groupby(["instancia", "metodo"], observed=True).agg(
        n_corridas=("semilla", "count"),
        cmax_promedio=("cmax", "mean"),
        cmax_std=("cmax", "std"),
        cmax_mejor=("cmax", "min"),
        rpd_promedio=("rpd", "mean"),
        rpd_std=("rpd", "std"),
        tiempo_promedio_s=("tiempo_segundos", "mean"),
    ).round(3)
    return resumen


def graficar_rpd_por_instancia(datos):
    """Un boxplot de RPD (AG vs Memético) por cada instancia, en subplots
    lado a lado. Mientras más bajo el RPD, mejor la solución.
    """
    fig, ejes = plt.subplots(1, len(ORDEN_INSTANCIAS), figsize=(12, 5), sharey=False)

    for eje, instancia in zip(ejes, ORDEN_INSTANCIAS):
        subconjunto = datos[datos["instancia"] == instancia]
        datos_ag = subconjunto[subconjunto["metodo"] == "AG"]["rpd"]
        datos_memetico = subconjunto[subconjunto["metodo"] == "Memetico"]["rpd"]

        eje.boxplot([datos_ag, datos_memetico], tick_labels=["AG", "Memético"])
        eje.set_title(instancia)
        eje.set_ylabel("RPD (%)")
        eje.grid(axis="y", linestyle="--", alpha=0.5)

    fig.suptitle("RPD por método e instancia (30 semillas c/u, más bajo es mejor)")
    fig.tight_layout()
    fig.savefig(RUTA_GRAFICO_RPD, dpi=150)
    plt.close(fig)


def graficar_tiempo_por_instancia(datos):
    """Barras con el tiempo promedio de ejecución por método e instancia.
    Sirve para discutir en el informe el costo computacional de agregar
    búsqueda local (explotación) frente al AG puro.
    """
    resumen_tiempo = datos.groupby(["instancia", "metodo"], observed=True)["tiempo_segundos"].mean().unstack()
    resumen_tiempo = resumen_tiempo.reindex(ORDEN_INSTANCIAS)[ORDEN_METODOS]

    fig, eje = plt.subplots(figsize=(7, 5))
    resumen_tiempo.plot(kind="bar", ax=eje)
    eje.set_ylabel("Tiempo promedio por corrida (s)")
    eje.set_xlabel("Instancia")
    eje.set_title("Costo computacional: AG vs Memético")
    eje.legend(title="Método")
    eje.grid(axis="y", linestyle="--", alpha=0.5)
    fig.tight_layout()
    fig.savefig(RUTA_GRAFICO_TIEMPO, dpi=150)
    plt.close(fig)


def aplicar_test_estadistico(datos):
    """Test de Wilcoxon (rangos con signo) para muestras pareadas: cada
    semilla se corrió con AG y con Memético sobre la misma instancia, así
    que se puede comparar el RPD par a par en vez de como dos muestras
    independientes. Se usa Wilcoxon (no un t-test) porque no se asume que
    el RPD siga una distribución normal.

    Hipótesis nula: no hay diferencia sistemática entre el RPD del AG y
    el del Memético. Se rechaza con un nivel de significancia de 0.05.
    """
    print("Test de Wilcoxon (RPD, AG vs Memético, pareado por semilla)")
    print("-" * 60)

    for instancia in ORDEN_INSTANCIAS:
        subconjunto = datos[datos["instancia"] == instancia]

        rpd_ag = subconjunto[subconjunto["metodo"] == "AG"].sort_values("semilla")["rpd"].to_numpy()
        rpd_memetico = subconjunto[subconjunto["metodo"] == "Memetico"].sort_values("semilla")["rpd"].to_numpy()

        estadistico, valor_p = stats.wilcoxon(rpd_ag, rpd_memetico)

        if valor_p < 0.05:
            conclusion = "diferencia estadísticamente significativa (Memético es distinto del AG)"
        else:
            conclusion = "no hay evidencia suficiente de diferencia significativa"

        print(f"{instancia}: estadístico={estadistico:.2f}, p-valor={valor_p:.6f} -> {conclusion}")

    print()


def main():
    if not os.path.isfile(RUTA_ENTRADA):
        print(f"Error: no se encontró '{RUTA_ENTRADA}'. Corre primero experimento.py.")
        return

    datos = cargar_resultados()

    resumen = calcular_resumen(datos)
    print("Resumen por instancia y método:")
    print(resumen)
    print()
    resumen.to_csv(RUTA_RESUMEN)
    print(f"Resumen guardado en {RUTA_RESUMEN}")
    print()

    aplicar_test_estadistico(datos)

    graficar_rpd_por_instancia(datos)
    print(f"Gráfico de RPD guardado en {RUTA_GRAFICO_RPD}")

    graficar_tiempo_por_instancia(datos)
    print(f"Gráfico de tiempo guardado en {RUTA_GRAFICO_TIEMPO}")


if __name__ == "__main__":
    main()
