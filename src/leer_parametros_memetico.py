import sys
import os


def leer_parametros_memetico(argumentos):
    """parsea y valida los parámetros del memético por línea de comandos.
    frecuencia_bl: cada cuántas generaciones se aplica la búsqueda local.
    k_mejores (opcional, por defecto 1): a cuántos de los mejores individuos se aplica cada vez.
    retorna la tupla de parámetros, o termina el programa si alguno es inválido."""
    if len(argumentos) not in (7, 8):
        print("Error: número incorrecto de parámetros")
        print(
            "Uso: python memetico.py semilla instancia tam_poblacion prob_cruza "
            "prob_mutacion num_generaciones frecuencia_bl [k_mejores]"
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
        k_mejores = int(argumentos[7]) if len(argumentos) == 8 else 1
    except ValueError:
        print("Error: uno de los parámetros numéricos no tiene un formato válido")
        print(
            "Uso: python memetico.py semilla instancia tam_poblacion prob_cruza "
            "prob_mutacion num_generaciones frecuencia_bl [k_mejores]"
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

    if k_mejores <= 0:
        print("Error: k_mejores debe ser un entero positivo (a cuántos de los mejores individuos se aplica la búsqueda local)")
        sys.exit(1)

    if k_mejores > tam_poblacion:
        print(f"Error: k_mejores ({k_mejores}) no puede ser mayor que tam_poblacion ({tam_poblacion})")
        sys.exit(1)

    return semilla, instancia, tam_poblacion, prob_cruza, prob_mutacion, num_generaciones, frecuencia_bl, k_mejores


if __name__ == "__main__":
    parametros = leer_parametros_memetico(sys.argv[1:])
    semilla, instancia, tam_poblacion, prob_cruza, prob_mutacion, num_generaciones, frecuencia_bl, k_mejores = parametros

    print("semilla:", semilla)
    print("instancia:", instancia)
    print("tam_poblacion:", tam_poblacion)
    print("prob_cruza:", prob_cruza)
    print("prob_mutacion:", prob_mutacion)
    print("num_generaciones:", num_generaciones)
    print("frecuencia_bl:", frecuencia_bl)
    print("k_mejores:", k_mejores)
