import numpy as np


def leer_instancia(ruta):
    archivo = open(ruta, "r")
    lineas = archivo.readlines()
    archivo.close()

    # se descartan líneas vacías y líneas de comentario (empiezan con '#'),
    # que es como vienen los archivos oficiales de Taillard
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

    # matriz de tiempos como array de numpy: filas = máquinas,
    # columnas = trabajos, tal como vienen en el archivo. Se arma primero
    # como lista de listas y se convierte al final porque construir un
    # array de numpy fila por fila (con np.append o concatenate) es
    # notoriamente más lento que llenar una lista y convertir una sola vez.
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
