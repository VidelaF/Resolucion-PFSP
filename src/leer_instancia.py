import numpy as np


def leer_instancia(ruta):
    archivo = open(ruta, "r")
    lineas = archivo.readlines()
    archivo.close()

    lineas_utiles = []
    for linea in lineas:
        linea = linea.strip()
        if linea != "" and not linea.startswith("#"):
            lineas_utiles.append(linea)

    primera_linea = lineas_utiles[0].split()
    n_trabajos = int(primera_linea[0])
    n_maquinas = int(primera_linea[1])

    tiempos = []
    for i in range(n_maquinas):
        fila = lineas_utiles[1 + i].split()
        fila_numeros = [int(x) for x in fila]
        tiempos.append(fila_numeros)

    
    tiempos = np.array(tiempos)

    return n_trabajos, n_maquinas, tiempos


if __name__ == "__main__":
    n, m, tiempos = leer_instancia("instances/taillard/ta001.txt")
    print("n_trabajos:", n)
    print("n_maquinas:", m)
    print("tipo de dato de tiempos:", type(tiempos))
    print("forma de tiempos (n_maquinas x n_trabajos):", tiempos.shape)
    print("tiempos[0] (máquina 1):", tiempos[0])
    print("tiempos[4] (máquina 5):", tiempos[4])
