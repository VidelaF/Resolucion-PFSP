from fitness import calcular_makespan


def construir_neh(tiempos):
    """heurística neh (nawaz, enscore y ham, 1983): ordena los trabajos por tiempo total
    descendente y los inserta uno a uno en la posición que da el menor makespan parcial.
    determinista, sin aleatoriedad. usada para sembrar un individuo de la población inicial."""
    n_maquinas = len(tiempos)
    n_trabajos = len(tiempos[0])

    tiempos_totales = [
        sum(tiempos[maquina][trabajo] for maquina in range(n_maquinas))
        for trabajo in range(n_trabajos)
    ]
    orden_por_tiempo_total = sorted(
        range(n_trabajos), key=lambda trabajo: tiempos_totales[trabajo], reverse=True
    )

    secuencia = [orden_por_tiempo_total[0]]
    for trabajo in orden_por_tiempo_total[1:]:
        mejor_secuencia = None
        mejor_fitness = None
        for posicion in range(len(secuencia) + 1):
            candidata = list(secuencia)
            candidata.insert(posicion, trabajo)
            fitness_candidata = calcular_makespan(candidata, tiempos)
            if mejor_fitness is None or fitness_candidata < mejor_fitness:
                mejor_fitness = fitness_candidata
                mejor_secuencia = candidata
        secuencia = mejor_secuencia

    return secuencia


if __name__ == "__main__":
    import random

    from leer_instancia import leer_instancia
    from poblacion import inicializar_poblacion

    n, m, tiempos = leer_instancia("instances/taillard/ta001.txt")

    secuencia_neh = construir_neh(tiempos)
    fitness_neh = calcular_makespan(secuencia_neh, tiempos)
    print(f"NEH sobre ta001.txt -> Cmax = {fitness_neh} (mejor conocido: 1278)")
    assert sorted(secuencia_neh) == list(range(n)), "NEH debe producir una permutación válida"

    random.seed(1)
    poblacion_aleatoria = inicializar_poblacion(40, n)
    mejor_aleatorio = min(calcular_makespan(ind, tiempos) for ind in poblacion_aleatoria)
    print(f"Mejor de 40 individuos aleatorios (semilla 1) -> Cmax = {mejor_aleatorio}")
