from aleatorios import generar_entero_aleatorio


def generar_permutacion_aleatoria(n_trabajos):
    """Genera una permutación aleatoria de los índices 0..n_trabajos-1.

    Usa el algoritmo de barajado de Fisher-Yates: recorre la lista desde
    el final hacia el principio y, en cada posición i, la intercambia con
    una posición j elegida al azar entre 0 e i (inclusive). Al terminar,
    cada una de las n_trabajos! permutaciones posibles tiene la misma
    probabilidad de haber sido generada.
    """
    permutacion = list(range(n_trabajos))
    for i in range(n_trabajos - 1, 0, -1):
        j = generar_entero_aleatorio(0, i)
        permutacion[i], permutacion[j] = permutacion[j], permutacion[i]
    return permutacion


def inicializar_poblacion(tam_poblacion, n_trabajos):
    """Genera la población inicial del algoritmo genético.

    Retorna una lista de tam_poblacion individuos, donde cada individuo
    es una permutación aleatoria (lista de índices de trabajos) generada
    de forma independiente.
    """
    poblacion = []
    for _ in range(tam_poblacion):
        individuo = generar_permutacion_aleatoria(n_trabajos)
        poblacion.append(individuo)
    return poblacion


if __name__ == "__main__":
    import random

    random.seed(42)  # semilla fija solo para que este ejemplo sea reproducible

    poblacion_ejemplo = inicializar_poblacion(5, 6)
    print("Población de 5 individuos, instancia de 6 trabajos:")
    for individuo in poblacion_ejemplo:
        print(individuo)

    # cada individuo debe contener cada trabajo exactamente una vez
    for individuo in poblacion_ejemplo:
        assert sorted(individuo) == list(range(6)), "individuo inválido"
    print("OK: todos los individuos son permutaciones válidas")
