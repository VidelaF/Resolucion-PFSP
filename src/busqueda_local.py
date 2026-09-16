from fitness import calcular_makespan


def busqueda_local_insercion(individuo, tiempos):
    """mueve cada trabajo a cada posición posible; aplica la primera mejora encontrada
    (first-improvement) y reinicia, hasta llegar a un óptimo local."""
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
    # ejemplo del enunciado: π=(J2,J1,J3) da cmax=15, mejor que π=(J1,J2,J3) con cmax=18
    tiempos_ejemplo = [
        [5, 2, 4],
        [3, 6, 4],
    ]
    peor_secuencia = [0, 1, 2]  # π = (J1, J2, J3), Cmax = 18
    mejorado = busqueda_local_insercion(peor_secuencia, tiempos_ejemplo)
    print(f"antes: {peor_secuencia} -> Cmax = {calcular_makespan(peor_secuencia, tiempos_ejemplo)}")
    print(f"después: {mejorado} -> Cmax = {calcular_makespan(mejorado, tiempos_ejemplo)}")

    from leer_instancia import leer_instancia

    n, m, tiempos = leer_instancia("instances/taillard/ta001.txt")
    secuencia_identidad = list(range(n))
    fitness_antes = calcular_makespan(secuencia_identidad, tiempos)
    mejorado_ta001 = busqueda_local_insercion(secuencia_identidad, tiempos)
    fitness_despues = calcular_makespan(mejorado_ta001, tiempos)
    print(f"\nta001.txt, secuencia identidad: Cmax {fitness_antes} -> {fitness_despues}")
    print("(mejor conocido: 1278)")
    assert fitness_despues <= fitness_antes
