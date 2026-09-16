import random


def generar_real_aleatorio():
    """real aleatorio en [0, 1)."""
    return random.random()


def generar_entero_aleatorio(minimo, maximo):
    """entero aleatorio en [minimo, maximo], ambos extremos incluidos."""
    return random.randint(minimo, maximo)
