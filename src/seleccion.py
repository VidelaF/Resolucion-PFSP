from aleatorios import generar_entero_aleatorio


def seleccionar_por_torneo(poblacion, fitnesses, tam_torneo=2):
    """elige tam_torneo individuos al azar (con reposición) y retorna el de menor makespan.
    tam_torneo=2: torneo binario, presión de selección baja."""
    mejor_indice = generar_entero_aleatorio(0, len(poblacion) - 1)
    for _ in range(tam_torneo - 1):
        indice_candidato = generar_entero_aleatorio(0, len(poblacion) - 1)
        if fitnesses[indice_candidato] < fitnesses[mejor_indice]:
            mejor_indice = indice_candidato
    return poblacion[mejor_indice]


if __name__ == "__main__":
    import random
    random.seed(1)

    poblacion_ejemplo = [[0, 1, 2], [2, 1, 0], [1, 0, 2], [0, 2, 1]]
    fitnesses_ejemplo = [50, 30, 80, 20]  # [0,2,1] es el mejor (fitness 20)

    seleccionados = [seleccionar_por_torneo(poblacion_ejemplo, fitnesses_ejemplo) for _ in range(10)]
    for individuo in seleccionados:
        print(individuo)
