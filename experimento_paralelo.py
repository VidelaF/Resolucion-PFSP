"""se define experimento paralelo para correr el experimento simultanemante en 3 ventanas cmd distintas para agilizar el proceso.
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

SEMILLAS = list(range(1, 31))
TAM_POBLACION = 40
PROB_CRUZA = 0.9
PROB_MUTACION = 0.2
NUM_GENERACIONES = 100
FRECUENCIA_BL_POR_INSTANCIA = {
    "ta001": 10,
    "ta041": 25,
    "ta071": 50,
    "ta090": 50,
    "ta058": 30,
}
K_MEJORES_BL = 2
RUTA_BEST_KNOWN = "instances/taillard/best_known.csv"

# mismos 3 bloques
BLOQUES = {
    "1": ["instances/taillard/ta071.txt"],
    "2": ["instances/taillard/ta090.txt"],
    "3": ["instances/taillard/ta001.txt", "instances/taillard/ta041.txt", "instances/taillard/ta058.txt"],
}

COLUMNAS_CSV = [
    "instancia", "n_trabajos", "n_maquinas", "metodo", "semilla",
    "cmax", "mejor_conocido", "rpd", "tiempo_segundos",
]


def ejecutar_una_corrida(metodo, tiempos, n_trabajos, semilla, frecuencia_bl, individuo_neh):
    random.seed(semilla)
    inicio = time.time()
    with contextlib.redirect_stdout(io.StringIO()):
        if metodo == "AG":
            _, cmax = ejecutar_ag(
                tiempos, n_trabajos, TAM_POBLACION, PROB_CRUZA, PROB_MUTACION, NUM_GENERACIONES,
                individuo_neh=individuo_neh
            )
        else:
            _, cmax = ejecutar_memetico(
                tiempos, n_trabajos, TAM_POBLACION, PROB_CRUZA, PROB_MUTACION,
                NUM_GENERACIONES, frecuencia_bl, K_MEJORES_BL, individuo_neh=individuo_neh
            )
    tiempo_segundos = time.time() - inicio
    return cmax, tiempo_segundos


def main():
    if len(sys.argv) != 2 or sys.argv[1] not in BLOQUES:
        print("Uso: python experimento_paralelo.py <1|2|3>")
        sys.exit(1)

    bloque_id = sys.argv[1]
    instancias = BLOQUES[bloque_id]
    ruta_salida = f"resultados/experimento_bloque{bloque_id}.csv"
    os.makedirs("resultados", exist_ok=True)

    total_corridas = len(instancias) * len(SEMILLAS) * 2
    corrida_actual = 0
    inicio_total = time.time()

    print(f"Bloque {bloque_id}: {instancias}")
    print(f"Total de corridas en este bloque: {total_corridas}")
    print()

    with open(ruta_salida, "w", newline="", encoding="utf-8") as archivo_csv:
        escritor = csv.DictWriter(archivo_csv, fieldnames=COLUMNAS_CSV)
        escritor.writeheader()

        for ruta_instancia in instancias:
            n_trabajos, n_maquinas, tiempos = leer_instancia(ruta_instancia)
            nombre_instancia = nombre_instancia_desde_ruta(ruta_instancia)
            mejor_conocido = obtener_mejor_conocido(nombre_instancia, RUTA_BEST_KNOWN)
            frecuencia_bl = FRECUENCIA_BL_POR_INSTANCIA[nombre_instancia]

            individuo_neh = construir_neh(tiempos)

            for metodo in ("AG", "Memetico"):
                for semilla in SEMILLAS:
                    corrida_actual += 1
                    cmax, tiempo_segundos = ejecutar_una_corrida(
                        metodo, tiempos, n_trabajos, semilla, frecuencia_bl, individuo_neh
                    )

                    if mejor_conocido is not None:
                        rpd = calcular_rpd(cmax, mejor_conocido)
                        rpd_texto = f"{rpd:.4f}"
                        rpd_impresion = f"{rpd:.2f}%"
                    else:
                        rpd_texto = ""
                        rpd_impresion = "sin referencia"

                    escritor.writerow({
                        "instancia": nombre_instancia,
                        "n_trabajos": n_trabajos,
                        "n_maquinas": n_maquinas,
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
                        f"[bloque {bloque_id}] [{corrida_actual}/{total_corridas}] {nombre_instancia} {metodo} "
                        f"semilla={semilla}: Cmax={cmax} (RPD={rpd_impresion}) "
                        f"{tiempo_segundos:.1f}s - transcurrido {transcurrido_min:.1f} min"
                    )

    print()
    print(f"Bloque {bloque_id} listo. Resultados en {ruta_salida}")
    print(f"Tiempo total del bloque: {(time.time() - inicio_total) / 60:.1f} minutos")


if __name__ == "__main__":
    main()
