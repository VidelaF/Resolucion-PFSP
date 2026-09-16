from aleatorios import generar_entero_aleatorio


def generar_permutacion_aleatoria(n_trabajos):
    """fisher-yates: cada una de las n_trabajos! permutaciones tiene la misma probabilidad de salir."""
    permutacion = list(range(n_trabajos))
    for i in range(n_trabajos - 1, 0, -1):
        j = generar_entero_aleatorio(0, i)
        permutacion[i], permutacion[j] = permutacion[j], permutacion[i]
    return permutacion


def inicializar_poblacion(tam_poblacion, n_trabajos):
    """lista de tam_poblacion permutaciones aleatorias independientes."""
    poblacion = []
    for _ in range(tam_poblacion):
        individuo = generar_permutacion_aleatoria(n_trabajos)
        poblacion.append(individuo)
    return poblacion


if __name__ == "__main__":
    import random

    random.seed(42)

    poblacion_ejemplo = inicializar_poblacion(5, 6)
    print("Población de 5 individuos, instancia de 6 trabajos:")
    for individuo in poblacion_ejemplo:
        print(individuo)

    for individuo in poblacion_ejemplo:
        assert sorted(individuo) == list(range(6)), "individuo inválido"
    print("OK: todos los individuos son permutaciones válidas")
