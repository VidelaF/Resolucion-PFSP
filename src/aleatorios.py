import random


def generar_real_aleatorio():
    """Genera un número real aleatorio en el intervalo [0, 1)."""
    return random.random()


def generar_entero_aleatorio(minimo, maximo):
    """Genera un número entero aleatorio en el intervalo [minimo, maximo],
    con ambos extremos incluidos.
    """
    return random.randint(minimo, maximo)
