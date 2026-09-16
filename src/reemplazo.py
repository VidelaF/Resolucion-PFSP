from aleatorios import generar_real_aleatorio
from fitness import calcular_makespan
from seleccion import seleccionar_por_torneo
from cruce import cruce_ox
from mutacion import mutar_intercambio


def generar_nueva_poblacion(poblacion, fitnesses, tiempos, prob_cruza, prob_mutacion, con_elitismo=True):
    """selección + cruce + mutación para armar la siguiente generación.
    con_elitismo=true: el mejor individuo actual reemplaza al peor de la nueva población
    si es mejor que este, para que el mejor fitness nunca empeore entre generaciones."""
    tam_poblacion = len(poblacion)

    if con_elitismo:
        indice_mejor = fitnesses.index(min(fitnesses))
        mejor_individuo = list(poblacion[indice_mejor])

    nueva_poblacion = []
    while len(nueva_poblacion) < tam_poblacion:
        padre1 = seleccionar_por_torneo(poblacion, fitnesses)
        padre2 = seleccionar_por_torneo(poblacion, fitnesses)

        if generar_real_aleatorio() < prob_cruza:
            hijo = cruce_ox(padre1, padre2)
        else:
            hijo = list(padre1)

        if generar_real_aleatorio() < prob_mutacion:
            hijo = mutar_intercambio(hijo)

        nueva_poblacion.append(hijo)

    if con_elitismo:
        fitnesses_nueva = [calcular_makespan(individuo, tiempos) for individuo in nueva_poblacion]
        indice_peor_nuevo = fitnesses_nueva.index(max(fitnesses_nueva))
        fitness_mejor_anterior = calcular_makespan(mejor_individuo, tiempos)
        if fitness_mejor_anterior < fitnesses_nueva[indice_peor_nuevo]:
            nueva_poblacion[indice_peor_nuevo] = mejor_individuo

    return nueva_poblacion


if __name__ == "__main__":
    import random
    random.seed(123)

    from leer_instancia import leer_instancia
    from poblacion import inicializar_poblacion

    n, m, tiempos = leer_instancia("instances/taillard/ta001.txt")

    poblacion = inicializar_poblacion(30, n)
    fitnesses = [calcular_makespan(individuo, tiempos) for individuo in poblacion]

    print(f"generación 0: mejor fitness = {min(fitnesses)} (mejor conocido: 1278)")

    mejor_anterior = min(fitnesses)
    for generacion in range(1, 21):
        poblacion = generar_nueva_poblacion(poblacion, fitnesses, tiempos, prob_cruza=0.9, prob_mutacion=0.2)
        fitnesses = [calcular_makespan(individuo, tiempos) for individuo in poblacion]
        mejor_actual = min(fitnesses)
        assert mejor_actual <= mejor_anterior, "el elitismo debería impedir que el mejor empeore"
        mejor_anterior = mejor_actual
        if generacion % 5 == 0:
            print(f"generación {generacion}: mejor fitness = {mejor_actual}")

    print("OK: el mejor fitness nunca empeoró entre generaciones (elitismo funcionando)")
