from aleatorios import generar_entero_aleatorio


def seleccionar_por_torneo(poblacion, fitnesses, tam_torneo=2):
    """Selecciona un individuo de la población mediante torneo.

    Se eligen tam_torneo individuos al azar (con reposición) y se retorna
    el de mejor fitness (menor makespan) entre ellos.

    poblacion: lista de individuos (permutaciones).
    fitnesses: lista de makespans, en el mismo orden que poblacion
        (fitnesses[i] es el makespan de poblacion[i]). Se recibe ya
        calculada para no volver a evaluar el makespan de cada candidato
        dentro de la selección.
    tam_torneo: cantidad de individuos que compiten en cada torneo.
        Con tam_torneo=2 (torneo binario, el valor por defecto) la
        presión de selección es baja y es la variante más simple y más
        usada como punto de partida.
    """
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
