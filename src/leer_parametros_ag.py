import sys
import os


def leer_parametros_ag(argumentos):
    
    if len(argumentos) != 6:
        print("Error: número incorrecto de parámetros")
        print("Uso: python ag.py semilla instancia tam_poblacion prob_cruza prob_mutacion num_generaciones")
        sys.exit(1)

    try:
        semilla = int(argumentos[0])
        instancia = argumentos[1]
        tam_poblacion = int(argumentos[2])
        prob_cruza = float(argumentos[3].replace(",", "."))
        prob_mutacion = float(argumentos[4].replace(",", "."))
        num_generaciones = int(argumentos[5])
    except ValueError:
        print("Error: uno de los parámetros numéricos no tiene un formato válido")
        print("Uso: python ag.py semilla instancia tam_poblacion prob_cruza prob_mutacion num_generaciones")
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

    return semilla, instancia, tam_poblacion, prob_cruza, prob_mutacion, num_generaciones


if __name__ == "__main__":
    parametros = leer_parametros_ag(sys.argv[1:])
    semilla, instancia, tam_poblacion, prob_cruza, prob_mutacion, num_generaciones = parametros

    print("semilla:", semilla)
    print("instancia:", instancia)
    print("tam_poblacion:", tam_poblacion)
    print("prob_cruza:", prob_cruza)
    print("prob_mutacion:", prob_mutacion)
    print("num_generaciones:", num_generaciones)
