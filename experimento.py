import contextlib
import csv
import io
import os
import random
import sys
import time

# los módulos "biblioteca" viven en src/; se agrega esa carpeta a sys.path
# para poder importarlos igual que hacen ag.py y memetico.py.
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "src"))

from ag import ejecutar_ag
from memetico import ejecutar_memetico
from leer_instancia import leer_instancia
from rpd import obtener_mejor_conocido, calcular_rpd, nombre_instancia_desde_ruta


# --- Parámetros del experimento ---
# Tres tamaños de instancia, como pide el enunciado (sección 5): chica,
# mediana y grande, para poder analizar cómo escala cada método.
INSTANCIAS = [
    "instances/taillard/ta001.txt",  # 20 trabajos x 5 máquinas
    "instances/taillard/ta041.txt",  # 50 trabajos x 10 máquinas
    "instances/taillard/ta071.txt",  # 100 trabajos x 10 máquinas
]
SEMILLAS = list(range(1, 31))  # 30 repeticiones por instancia y método
TAM_POBLACION = 40
PROB_CRUZA = 0.9
PROB_MUTACION = 0.2
NUM_GENERACIONES = 100
# Cada 50 generaciones -> 2 aplicaciones de búsqueda local por corrida
# (en la generación 50 y en la 100). Se eligió este valor, en vez de uno
# más frecuente, por el costo de busqueda_local_insercion en instancias
# grandes: en ta071 (100 trabajos) una sola pasada cuesta ~43s, así que
# aplicarla cada 10 generaciones (10 veces por corrida) haría que el
# experimento completo (3 instancias x 30 semillas x 2 métodos) tomara
# varias horas en vez de minutos. Con 2 aplicaciones por corrida ya se
# observa con claridad el efecto de explotación del Memético frente al
# AG puro (ver resultados).
FRECUENCIA_BL = 50

RUTA_BEST_KNOWN = "instances/taillard/best_known.csv"
RUTA_SALIDA = "resultados/experimento.csv"

COLUMNAS_CSV = [
    "instancia", "n_trabajos", "n_maquinas", "metodo", "semilla",
    "cmax", "mejor_conocido", "rpd", "tiempo_segundos",
]


def ejecutar_una_corrida(metodo, tiempos, n_trabajos, semilla):
    """Ejecuta una corrida del AG o del Memético sobre una instancia ya
    leída. Fija la semilla antes de correr, para que cada método parta
    de la misma población inicial en cada repetición (comparación justa).

    ag.py y memetico.py imprimen el progreso por generación por diseño,
    pensado para uso interactivo; acá se silencia esa salida (no se
    modifica ninguno de los dos archivos) para no imprimir miles de
    líneas durante el experimento.

    Retorna (cmax, tiempo_segundos).
    """
    random.seed(semilla)
    inicio = time.time()

    with contextlib.redirect_stdout(io.StringIO()):
        if metodo == "AG":
            _, cmax = ejecutar_ag(
                tiempos, n_trabajos, TAM_POBLACION, PROB_CRUZA, PROB_MUTACION, NUM_GENERACIONES
            )
        else:
            _, cmax = ejecutar_memetico(
                tiempos, n_trabajos, TAM_POBLACION, PROB_CRUZA, PROB_MUTACION,
                NUM_GENERACIONES, FRECUENCIA_BL
            )

    tiempo_segundos = time.time() - inicio
    return cmax, tiempo_segundos


def main():
    os.makedirs(os.path.dirname(RUTA_SALIDA), exist_ok=True)

    total_corridas = len(INSTANCIAS) * len(SEMILLAS) * 2
    corrida_actual = 0
    inicio_total = time.time()

    print(f"Total de corridas: {total_corridas} ({len(INSTANCIAS)} instancias x {len(SEMILLAS)} semillas x 2 métodos)")
    print()

    with open(RUTA_SALIDA, "w", newline="", encoding="utf-8") as archivo_csv:
        escritor = csv.DictWriter(archivo_csv, fieldnames=COLUMNAS_CSV)
        escritor.writeheader()

        for ruta_instancia in INSTANCIAS:
            n_trabajos, n_maquinas, tiempos = leer_instancia(ruta_instancia)
            nombre_instancia = nombre_instancia_desde_ruta(ruta_instancia)
            mejor_conocido = obtener_mejor_conocido(nombre_instancia, RUTA_BEST_KNOWN)

            for metodo in ("AG", "Memetico"):
                for semilla in SEMILLAS:
                    corrida_actual += 1
                    cmax, tiempo_segundos = ejecutar_una_corrida(metodo, tiempos, n_trabajos, semilla)

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
                    # flush inmediato: si el proceso se corta a mitad de
                    # camino (son bastantes minutos de corrida), no se
                    # pierden los resultados ya calculados.
                    archivo_csv.flush()

                    transcurrido_min = (time.time() - inicio_total) / 60
                    print(
                        f"[{corrida_actual}/{total_corridas}] {nombre_instancia} {metodo} "
                        f"semilla={semilla}: Cmax={cmax} (RPD={rpd_impresion}) "
                        f"{tiempo_segundos:.1f}s - transcurrido {transcurrido_min:.1f} min"
                    )

    print()
    print(f"Listo. Resultados guardados en {RUTA_SALIDA}")
    print(f"Tiempo total: {(time.time() - inicio_total) / 60:.1f} minutos")


if __name__ == "__main__":
    main()
