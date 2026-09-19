from aleatorios import generar_entero_aleatorio


def cruce_ox(padre1, padre2):
    """ con order crossover copiamos un segmento de padre1 y completa con el orden de padre2,
    saltando lo ya copiado. evita duplicados, a diferencia de un cruce de un punto normal."""
    n = len(padre1)
    punto1 = generar_entero_aleatorio(0, n - 1)
    punto2 = generar_entero_aleatorio(0, n - 1)
    if punto1 > punto2:
        punto1, punto2 = punto2, punto1

    hijo = [None] * n
    for i in range(punto1, punto2 + 1):
        hijo[i] = padre1[i]

    trabajos_copiados = set(padre1[punto1:punto2 + 1])

    posicion_hijo = (punto2 + 1) % n
    posicion_padre2 = (punto2 + 1) % n
    while None in hijo:
        trabajo = padre2[posicion_padre2]
        if trabajo not in trabajos_copiados:
            hijo[posicion_hijo] = trabajo
            posicion_hijo = (posicion_hijo + 1) % n
        posicion_padre2 = (posicion_padre2 + 1) % n

    return hijo


if __name__ == "__main__":
    import random
    random.seed(3)

    padre1 = [0, 1, 2, 3, 4, 5, 6, 7, 8]
    padre2 = [8, 7, 6, 5, 4, 3, 2, 1, 0]

    for _ in range(5):
        hijo = cruce_ox(padre1, padre2)
        es_valido = sorted(hijo) == list(range(9))
        print(hijo, "- válido" if es_valido else "- INVÁLIDO")
        assert es_valido
