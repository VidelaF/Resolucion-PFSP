from aleatorios import generar_entero_aleatorio


def mutar_intercambio(individuo):
    """swap de dos posiciones al azar. retorna una copia, no modifica el original."""
    n = len(individuo)
    mutado = list(individuo)
    pos1 = generar_entero_aleatorio(0, n - 1)
    pos2 = generar_entero_aleatorio(0, n - 1)
    mutado[pos1], mutado[pos2] = mutado[pos2], mutado[pos1]
    return mutado


if __name__ == "__main__":
    import random
    random.seed(7)

    original = [0, 1, 2, 3, 4, 5, 6, 7]
    for _ in range(5):
        mutado = mutar_intercambio(original)
        es_valido = sorted(mutado) == list(range(8))
        print(f"original={original}  mutado={mutado}", "- válido" if es_valido else "- INVÁLIDO")
        assert es_valido

    print("original sin modificar:", original)
