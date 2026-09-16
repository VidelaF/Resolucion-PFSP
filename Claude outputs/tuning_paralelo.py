"""Versión paralela del tuning de parámetros ("un factor a la vez"), dividida en
3 bloques -uno por parámetro- para correr en 3 ventanas de CMD simultáneas,
igual que se hizo con experimento_paralelo.py.

Cada bloque prueba los 4 valores candidatos de UN parámetro (tam_poblacion,
prob_cruza o prob_mutacion), dejando los otros dos en su valor base, en
ta001 y ta041, con 10 semillas, AG y Memético.

Uso: tres ventanas de CMD distintas, cada una parada en la raíz del proyecto:
    python tuning_paralelo.py tam_poblacion
    python tuning_paralelo.py prob_cruza
    python tuning_paralelo.py prob_mutacion

Cada bloque escribe resultados/tuning_bloque_<parametro>.csv. Al terminar los
3, se juntan en un solo resultados/tuning_parametros.csv (mismo formato que la
versión secuencial) con el mismo script de unión usado para experimento.py.
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

INSTANCIAS = [
    "instances/taillard/ta001.txt",
    "instances/taillard/ta041.txt",
]
FRECUENCIA_BL_POR_INSTANCIA = {"ta001": 10, "ta041": 25}
K_MEJORES_BL = 2

SEMILLAS = list(range(1, 11))

BASE = {
    "tam_poblacion": 40,
    "prob_cruza": 0.9,
    "prob_mutacion": 0.2,
}
NUM_GENERACIONES = 100

RANGOS = {
    "tam_poblacion": [20, 40, 60, 80],
    "prob_cruza": [0.7, 0.8, 0.9, 1.0],
    "prob_mutacion": [0.05, 0.1, 0.2, 0.3],
}

RUTA_BEST_KNOWN = "instances/taillard/best_known.csv"

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
    if len(sys.argv) != 2 or sys.argv[1] not in RANGOS:
        print("Uso: python tuning_paralelo.py <tam_poblacion|prob_cruza|prob_mutacion>")
        sys.exit(1)

    parametro = sys.argv[1]
    valores = RANGOS[parametro]
    ruta_salida = f"resultados/tuning_bloque_{parametro}.csv"
    os.makedirs("resultados", exist_ok=True)

    datos_instancias = {}
    for ruta_instancia in INSTANCIAS:
        n_trabajos, n_maquinas, tiempos = leer_instancia(ruta_instancia)
        nombre_instancia = nombre_instancia_desde_ruta(ruta_instancia)
        mejor_conocido = obtener_mejor_conocido(nombre_instancia, RUTA_BEST_KNOWN)
        individuo_neh = construir_neh(tiempos)
        datos_instancias[nombre_instancia] = {
            "n_trabajos": n_trabajos,
            "n_maquinas": n_maquinas,
            "tiempos": tiempos,
            "mejor_conocido": mejor_conocido,
            "individuo_neh": individuo_neh,
            "frecuencia_bl": FRECUENCIA_BL_POR_INSTANCIA[nombre_instancia],
        }

    total_corridas = len(valores) * len(INSTANCIAS) * 2 * len(SEMILLAS)
    corrida_actual = 0
    inicio_total = time.time()

    print(f"Bloque: {parametro} -> valores {valores}")
    print(f"Total de corridas en este bloque: {total_corridas}")
    print()

    with open(ruta_salida, "w", newline="", encoding="utf-8") as archivo_csv:
        escritor = csv.DictWriter(archivo_csv, fieldnames=COLUMNAS_CSV)
        escritor.writeheader()

        for valor in valores:
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
                            f"[bloque {parametro}] [{corrida_actual}/{total_corridas}] "
                            f"{parametro}={valor} {nombre_instancia} {metodo} semilla={semilla}: "
                            f"Cmax={cmax} (RPD={rpd_impresion}) "
                            f"{tiempo_segundos:.1f}s - transcurrido {transcurrido_min:.1f} min"
                        )

    print()
    print(f"Bloque {parametro} listo. Resultados en {ruta_salida}")
    print(f"Tiempo total del bloque: {(time.time() - inicio_total) / 60:.1f} minutos")


if __name__ == "__main__":
    main()
