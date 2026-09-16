"""Fase de ajuste de parámetros ("un factor a la vez"), pedida explícitamente por
el profesor: variar prob_cruza, prob_mutacion y tam_poblacion de a uno, dejando
los demás en el valor base, para ver cuál configuración se acerca más al UB.

Fase exploratoria (no la comparación final del paper): instancias baratas
(ta001, ta041), 10 semillas por configuración en vez de 30. Una vez identificada
la mejor configuración de cada parámetro, se valida aparte con el protocolo
completo (30 semillas, todas las instancias) antes de reportarla como resultado.

Rangos de exploración (criterio propio, centrados en los valores base ya usados
en el experimento principal — ver nota en el paper: no se citan como tomados de
un estudio puntual):
    tam_poblacion:  20, 40 (base), 60, 80
    prob_cruza:     0.7, 0.8, 0.9 (base), 1.0
    prob_mutacion:  0.05, 0.1, 0.2 (base), 0.3

Uso: parado en la raíz del proyecto (junto a ag.py, memetico.py):
    python tuning_parametros.py
"""
import contextlib
import csv
import io
import os
import random
import sys
import time

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "src"))

from ag import ejecutar_ag
from memetico import ejecutar_memetico
from leer_instancia import leer_instancia
from neh import construir_neh
from rpd import obtener_mejor_conocido, calcular_rpd, nombre_instancia_desde_ruta

# instancias baratas para la fase exploratoria
INSTANCIAS = [
    "instances/taillard/ta001.txt",
    "instances/taillard/ta041.txt",
]
FRECUENCIA_BL_POR_INSTANCIA = {"ta001": 10, "ta041": 25}
K_MEJORES_BL = 2

SEMILLAS = list(range(1, 11))  # 10 semillas en fase exploratoria (no 30)

# valores base = los mismos del experimento principal
BASE = {
    "tam_poblacion": 40,
    "prob_cruza": 0.9,
    "prob_mutacion": 0.2,
}
NUM_GENERACIONES = 100

# un factor a la vez: para cada parámetro, la lista de valores a probar
# (incluye el valor base para tener el punto de referencia en la misma tabla)
RANGOS = {
    "tam_poblacion": [20, 40, 60, 80],
    "prob_cruza": [0.7, 0.8, 0.9, 1.0],
    "prob_mutacion": [0.05, 0.1, 0.2, 0.3],
}

RUTA_BEST_KNOWN = "instances/taillard/best_known.csv"
RUTA_SALIDA = "resultados/tuning_parametros.csv"

COLUMNAS_CSV = [
    "parametro_variado", "valor", "instancia", "n_trabajos", "n_maquinas",
    "metodo", "semilla", "cmax", "mejor_conocido", "rpd", "tiempo_segundos",
]


def ejecutar_una_corrida(metodo, tiempos, n_trabajos, semilla, tam_poblacion,
                          prob_cruza, prob_mutacion, frecuencia_bl, individuo_neh):
    random.seed(semilla)
    inicio = time.time()
    with contextlib.redirect_stdout(io.StringIO()):
        if metodo == "AG":
            _, cmax = ejecutar_ag(
                tiempos, n_trabajos, tam_poblacion, prob_cruza, prob_mutacion,
                NUM_GENERACIONES, individuo_neh=individuo_neh
            )
        else:
            _, cmax = ejecutar_memetico(
                tiempos, n_trabajos, tam_poblacion, prob_cruza, prob_mutacion,
                NUM_GENERACIONES, frecuencia_bl, K_MEJORES_BL, individuo_neh=individuo_neh
            )
    tiempo_segundos = time.time() - inicio
    return cmax, tiempo_segundos


def main():
    os.makedirs(os.path.dirname(RUTA_SALIDA), exist_ok=True)

    # instancias precargadas una sola vez (no una vez por combinación de parámetro)
    datos_instancias = {}
    for ruta_instancia in INSTANCIAS:
        n_trabajos, n_maquinas, tiempos = leer_instancia(ruta_instancia)
        nombre_instancia = nombre_instancia_desde_ruta(ruta_instancia)
        mejor_conocido = obtener_mejor_conocido(nombre_instancia, RUTA_BEST_KNOWN)
        individuo_neh = construir_neh(tiempos)  # NEH es determinista: una vez por instancia
        datos_instancias[nombre_instancia] = {
            "ruta": ruta_instancia,
            "n_trabajos": n_trabajos,
            "n_maquinas": n_maquinas,
            "tiempos": tiempos,
            "mejor_conocido": mejor_conocido,
            "individuo_neh": individuo_neh,
            "frecuencia_bl": FRECUENCIA_BL_POR_INSTANCIA[nombre_instancia],
        }

    # total de corridas: por cada parámetro, por cada valor, por cada instancia,
    # por cada método, por cada semilla
    total_corridas = sum(len(v) for v in RANGOS.values()) * len(INSTANCIAS) * 2 * len(SEMILLAS)
    corrida_actual = 0
    inicio_total = time.time()

    print(f"Total de corridas de tuning: {total_corridas}")
    print(f"({sum(len(v) for v in RANGOS.values())} valores de parámetro x "
          f"{len(INSTANCIAS)} instancias x 2 métodos x {len(SEMILLAS)} semillas)")
    print()

    with open(RUTA_SALIDA, "w", newline="", encoding="utf-8") as archivo_csv:
        escritor = csv.DictWriter(archivo_csv, fieldnames=COLUMNAS_CSV)
        escritor.writeheader()

        for parametro, valores in RANGOS.items():
            for valor in valores:
                # arranca de los valores base y solo cambia el parámetro que toca
                config = dict(BASE)
                config[parametro] = valor

                for nombre_instancia, datos in datos_instancias.items():
                    for metodo in ("AG", "Memetico"):
                        for semilla in SEMILLAS:
                            corrida_actual += 1
                            cmax, tiempo_segundos = ejecutar_una_corrida(
                                metodo, datos["tiempos"], datos["n_trabajos"], semilla,
                                config["tam_poblacion"], config["prob_cruza"], config["prob_mutacion"],
                                datos["frecuencia_bl"], datos["individuo_neh"]
                            )

                            mejor_conocido = datos["mejor_conocido"]
                            if mejor_conocido is not None:
                                rpd = calcular_rpd(cmax, mejor_conocido)
                                rpd_texto = f"{rpd:.4f}"
                                rpd_impresion = f"{rpd:.2f}%"
                            else:
                                rpd_texto = ""
                                rpd_impresion = "sin referencia"

                            escritor.writerow({
                                "parametro_variado": parametro,
                                "valor": valor,
                                "instancia": nombre_instancia,
                                "n_trabajos": datos["n_trabajos"],
                                "n_maquinas": datos["n_maquinas"],
                                "metodo": metodo,
                                "semilla": semilla,
                                "cmax": cmax,
                                "mejor_conocido": mejor_conocido if mejor_conocido is not None else "",
                                "rpd": rpd_texto,
                                "tiempo_segundos": f"{tiempo_segundos:.3f}",
                            })
                            archivo_csv.flush()

                            transcurrido_min = (time.time() - inicio_total) / 60
                            print(
                                f"[{corrida_actual}/{total_corridas}] {parametro}={valor} "
                                f"{nombre_instancia} {metodo} semilla={semilla}: "
                                f"Cmax={cmax} (RPD={rpd_impresion}) "
                                f"{tiempo_segundos:.1f}s - transcurrido {transcurrido_min:.1f} min"
                            )

    print()
    print(f"Listo. Resultados guardados en {RUTA_SALIDA}")
    print(f"Tiempo total: {(time.time() - inicio_total) / 60:.1f} minutos")


if __name__ == "__main__":
    main()
