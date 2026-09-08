from fitness import calcular_makespan


def busqueda_local_insercion(individuo, tiempos):
    """Mejora un individuo mediante búsqueda local por inserción.

    Para cada trabajo de la secuencia, se prueba sacarlo de su posición
    actual e insertarlo en cada una de las demás posiciones. Apenas se
    encuentra un movimiento que reduce el makespan, se aplica de
    inmediato y se reinicia la búsqueda desde el principio (estrategia
    "first-improvement": más simple y más rápida por movimiento que
    evaluar todos los movimientos posibles antes de elegir el mejor).

    El proceso se repite hasta que una pasada completa no encuentra
    ningún movimiento que mejore el makespan actual, es decir, hasta
    llegar a un óptimo local respecto al vecindario de inserción.

    No modifica el individuo recibido: retorna una copia mejorada.

    Costo: cada movimiento evaluado cuesta O(n_trabajos * n_maquinas)
    (una llamada a calcular_makespan), y se pueden evaluar hasta
    n_trabajos^2 movimientos por pasada. Para instancias grandes (100+
    trabajos) conviene no aplicar esta función a toda la población en
    cada generación, sino con una frecuencia controlada (por ejemplo,
    solo al mejor individuo, o cada cierto número de generaciones).
    """
    mejor = list(individuo)
    fitness_mejor = calcular_makespan(mejor, tiempos)
    n = len(mejor)

    mejora_encontrada = True
    while mejora_encontrada:
        mejora_encontrada = False
        for pos_origen in range(n):
            trabajo = mejor[pos_origen]
            for pos_destino in range(n):
                if pos_destino == pos_origen:
                    continue
                candidato = list(mejor)
                candidato.pop(pos_origen)
                candidato.insert(pos_destino, trabajo)
                fitness_candidato = calcular_makespan(candidato, tiempos)
                if fitness_candidato < fitness_mejor:
                    mejor = candidato
                    fitness_mejor = fitness_candidato
                    mejora_encontrada = True
                    break
            if mejora_encontrada:
                break

    return mejor


if __name__ == "__main__":
    # Ejemplo del enunciado: con π=(J2,J1,J3) el makespan ya daba 15
    # (mejor que π=(J1,J2,J3), que da 18). Verificamos que la búsqueda
    # local, partida desde la peor, converge a la misma o mejor solución.
    tiempos_ejemplo = [
        [5, 2, 4],
        [3, 6, 4],
    ]
    peor_secuencia = [0, 1, 2]  # π = (J1, J2, J3), Cmax = 18
    mejorado = busqueda_local_insercion(peor_secuencia, tiempos_ejemplo)
    print(f"antes: {peor_secuencia} -> Cmax = {calcular_makespan(peor_secuencia, tiempos_ejemplo)}")
    print(f"después: {mejorado} -> Cmax = {calcular_makespan(mejorado, tiempos_ejemplo)}")

    # Sanity check con una instancia real de Taillard.
    from leer_instancia import leer_instancia

    n, m, tiempos = leer_instancia("instances/taillard/ta001.txt")
    secuencia_identidad = list(range(n))
    fitness_antes = calcular_makespan(secuencia_identidad, tiempos)
    mejorado_ta001 = busqueda_local_insercion(secuencia_identidad, tiempos)
    fitness_despues = calcular_makespan(mejorado_ta001, tiempos)
    print(f"\nta001.txt, secuencia identidad: Cmax {fitness_antes} -> {fitness_despues}")
    print("(mejor conocido: 1278)")
    assert fitness_despues <= fitness_antes
