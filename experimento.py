import contextlib
import csv
import io
import os
import random
import sys
import time

#módulos de src en el path
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "src"))

from ag import ejecutar_ag
from memetico import ejecutar_memetico
from leer_instancia import leer_instancia
from neh import construir_neh
from rpd import obtener_mejor_conocido, calcular_rpd, nombre_instancia_desde_ruta


# tres tamaños
INSTANCIAS = [
    "instances/taillard/ta001.txt",  #20 trabajos x 5 máquinas
    "instances/taillard/ta041.txt",  #50 trabajos x 10 máquinas
    "instances/taillard/ta071.txt",  #100 trabajos x 10 máquinas
]
SEMILLAS = list(range(1, 31))  #30 repeticiones por instancia y método
TAM_POBLACION = 40
PROB_CRUZA = 0.9
PROB_MUTACION = 0.2
NUM_GENERACIONES = 100

FRECUENCIA_BL_POR_INSTANCIA = {
    "ta001": 10,
    "ta041": 25,
    "ta071": 50,
}
K_MEJORES_BL = 2  #además del mejor aplicamos búsqueda local también sobre el segundo mejor

RUTA_BEST_KNOWN = "instances/taillard/best_known.csv"
RUTA_SALIDA = "resultados/experimento.csv"

COLUMNAS_CSV = [
    "instancia", "n_trabajos", "n_maquinas", "metodo", "semilla",
    "cmax", "mejor_conocido", "rpd", "tiempo_segundos",
]


def ejecutar_una_corrida(metodo, tiempos, n_trabajos, semilla, frecuencia_bl, individuo_neh):
    random.seed(semilla)  #misma semilla en ag y memético: misma población inicial, comparación justa
    inicio = time.time()

    with contextlib.redirect_stdout(io.StringIO()):  #ilencia el progreso por generación
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
            frecuencia_bl = FRECUENCIA_BL_POR_INSTANCIA[nombre_instancia]

            #NEH no depende de la semilla entonces lo calculamos una sola vez por
            #instancia y se reutiliza en las 30 semillas x 2 métodos, en vez de recalcularlo
            #60 veces por nada.
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
                        f"[{corrida_actual}/{total_corridas}] {nombre_instancia} {metodo} "
                        f"semilla={semilla}: Cmax={cmax} (RPD={rpd_impresion}) "
                        f"{tiempo_segundos:.1f}s - transcurrido {transcurrido_min:.1f} min"
                    )

    print()
    print(f"Listo. Resultados guardados en {RUTA_SALIDA}")
    print(f"Tiempo total: {(time.time() - inicio_total) / 60:.1f} minutos")


if __name__ == "__main__":
    main()
