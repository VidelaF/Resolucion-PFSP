import sys
import os


def leer_parametros_memetico(argumentos):
    """Parsea y valida los parámetros del Algoritmo Memético recibidos
    por línea de comandos.

    argumentos: lista de argumentos posicionales, sin el nombre del
        script (sys.argv[1:]), en el orden semilla, instancia,
        tam_poblacion, prob_cruza, prob_mutacion, num_generaciones,
        frecuencia_bl.

    frecuencia_bl indica cada cuántas generaciones se aplica la
    búsqueda local al mejor individuo de la población (ej. 1 = todas
    las generaciones, 5 = una de cada cinco).

    Retorna la tupla (semilla, instancia, tam_poblacion, prob_cruza,
    prob_mutacion, num_generaciones, frecuencia_bl) si todos los
    parámetros son válidos. Si alguno es inválido, imprime un mensaje
    describiendo el problema y termina el programa (sys.exit(1)).
    """
    if len(argumentos) != 7:
        print("Error: número incorrecto de parámetros")
        print(
            "Uso: python memetico.py semilla instancia tam_poblacion prob_cruza "
            "prob_mutacion num_generaciones frecuencia_bl"
        )
        sys.exit(1)

    try:
        semilla = int(argumentos[0])
        instancia = argumentos[1]
        tam_poblacion = int(argumentos[2])
        prob_cruza = float(argumentos[3].replace(",", "."))
        prob_mutacion = float(argumentos[4].replace(",", "."))
        num_generaciones = int(argumentos[5])
        frecuencia_bl = int(argumentos[6])
    except ValueError:
        print("Error: uno de los parámetros numéricos no tiene un formato válido")
        print(
            "Uso: python memetico.py semilla instancia tam_poblacion prob_cruza "
            "prob_mutacion num_generaciones frecuencia_bl"
        )
        sys.exit(1)

    if not os.path.isfile(instancia):
        print(f"Error: no se encontró el archivo de instancia '{instancia}'")
        sys.exit(1)

    if tam_poblacion <= 0:
        print("Error: tam_poblacion debe ser un entero positivo")
        sys.exit(1)

    if num_generaciones <= 0:
        print("Error: num_generaciones debe ser un entero positivo")
        sys.exit(1)

    if not (0.0 <= prob_cruza <= 1.0):
        print("Error: prob_cruza debe estar entre 0 y 1")
        sys.exit(1)

    if not (0.0 <= prob_mutacion <= 1.0):
        print("Error: prob_mutacion debe estar entre 0 y 1")
        sys.exit(1)

    if frecuencia_bl <= 0:
        print("Error: frecuencia_bl debe ser un entero positivo (cada cuántas generaciones se aplica la búsqueda local)")
        sys.exit(1)

    return semilla, instancia, tam_poblacion, prob_cruza, prob_mutacion, num_generaciones, frecuencia_bl


if __name__ == "__main__":
    parametros = leer_parametros_memetico(sys.argv[1:])
    semilla, instancia, tam_poblacion, prob_cruza, prob_mutacion, num_generaciones, frecuencia_bl = parametros

    print("semilla:", semilla)
    print("instancia:", instancia)
    print("tam_poblacion:", tam_poblacion)
    print("prob_cruza:", prob_cruza)
    print("prob_mutacion:", prob_mutacion)
    print("num_generaciones:", num_generaciones)
    print("frecuencia_bl:", frecuencia_bl)
