import os
import random
import sys

from leer_parametros_ag import leer_parametros_ag
from leer_instancia import leer_instancia
from poblacion import inicializar_poblacion
from fitness import calcular_makespan
from reemplazo import generar_nueva_poblacion
from rpd import obtener_mejor_conocido, calcular_rpd, nombre_instancia_desde_ruta


def ejecutar_ag(tiempos, n_trabajos, tam_poblacion, prob_cruza, prob_mutacion, num_generaciones):
    """Ejecuta el Algoritmo Genético completo sobre una instancia ya leída.

    Retorna una tupla (mejor_individuo, mejor_fitness) con la mejor
    secuencia encontrada y su makespan.
    """
    poblacion = inicializar_poblacion(tam_poblacion, n_trabajos)
    fitnesses = [calcular_makespan(individuo, tiempos) for individuo in poblacion]

    for generacion in range(1, num_generaciones + 1):
        poblacion = generar_nueva_poblacion(poblacion, fitnesses, tiempos, prob_cruza, prob_mutacion)
        fitnesses = [calcular_makespan(individuo, tiempos) for individuo in poblacion]
        print(f"generación {generacion}/{num_generaciones}: mejor fitness = {min(fitnesses)}")

    indice_mejor = fitnesses.index(min(fitnesses))
    return poblacion[indice_mejor], fitnesses[indice_mejor]


def main():
    semilla, ruta_instancia, tam_poblacion, prob_cruza, prob_mutacion, num_generaciones = leer_parametros_ag(sys.argv[1:])

    random.seed(semilla)

    try:
        n_trabajos, n_maquinas, tiempos = leer_instancia(ruta_instancia)
    except (OSError, ValueError, IndexError) as error:
        print(f"Error: no se pudo leer la instancia '{ruta_instancia}': {error}")
        sys.exit(1)

    print(f"Instancia: {ruta_instancia} ({n_trabajos} trabajos, {n_maquinas} máquinas)")
    print(
        f"Parámetros: semilla={semilla}, tam_poblacion={tam_poblacion}, "
        f"prob_cruza={prob_cruza}, prob_mutacion={prob_mutacion}, "
        f"num_generaciones={num_generaciones}"
    )
    print()

    mejor_individuo, mejor_fitness = ejecutar_ag(
        tiempos, n_trabajos, tam_poblacion, prob_cruza, prob_mutacion, num_generaciones
    )

    print()
    print(f"Mejor secuencia encontrada: {mejor_individuo}")
    print(f"Makespan (Cmax): {mejor_fitness}")

    ruta_best_known = os.path.join(os.path.dirname(ruta_instancia), "best_known.csv")
    nombre_instancia = nombre_instancia_desde_ruta(ruta_instancia)
    mejor_conocido = obtener_mejor_conocido(nombre_instancia, ruta_best_known)

    if mejor_conocido is not None:
        rpd = calcular_rpd(mejor_fitness, mejor_conocido)
        print(f"Mejor conocido (UB): {mejor_conocido}")
        print(f"RPD: {rpd:.2f}%")
    else:
        print(f"(no se encontró un valor de referencia para '{nombre_instancia}' en {ruta_best_known})")


if __name__ == "__main__":
    main()
