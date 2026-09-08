import csv
import os


def obtener_mejor_conocido(nombre_instancia, ruta_csv):
    """Busca el mejor makespan conocido (UB) para una instancia en el CSV
    de valores de referencia.

    nombre_instancia: nombre de la instancia sin extensión, ej. "ta001".
    ruta_csv: ruta al archivo best_known.csv (columnas Name,n,m,LB,UB,Optimal).

    Retorna el valor UB como entero, o None si la instancia no está en
    el archivo.
    """
    with open(ruta_csv, "r") as archivo:
        lector = csv.DictReader(archivo)
        for fila in lector:
            if fila["Name"] == nombre_instancia:
                return int(fila["UB"])
    return None


def calcular_rpd(cmax_obtenido, mejor_conocido):
    """Calcula el RPD (Relative Percentage Deviation) de una solución.

    RPD(%) = (Cmax_obtenido - Cmax_mejor_conocido) / Cmax_mejor_conocido * 100

    Un RPD de 0 significa que se igualó el mejor valor conocido; valores
    mayores indican qué tan lejos, en porcentaje, quedó la solución
    obtenida respecto al mejor conocido (nunca debería dar negativo,
    salvo que se encuentre una solución mejor que la reportada en el CSV).
    """
    return (cmax_obtenido - mejor_conocido) / mejor_conocido * 100


def nombre_instancia_desde_ruta(ruta_instancia):
    """Extrae el nombre de la instancia (ej. "ta001") desde la ruta de su
    archivo (ej. "instances/taillard/ta001.txt")."""
    nombre_archivo = os.path.basename(ruta_instancia)
    nombre_sin_extension, _ = os.path.splitext(nombre_archivo)
    return nombre_sin_extension


if __name__ == "__main__":
    ub_ta001 = obtener_mejor_conocido("ta001", "instances/taillard/best_known.csv")
    print(f"mejor conocido para ta001: {ub_ta001} (esperado: 1278)")
    assert ub_ta001 == 1278

    rpd_ejemplo = calcular_rpd(1332, ub_ta001)
    print(f"RPD de una solución con Cmax=1332: {rpd_ejemplo:.2f}%")

    nombre = nombre_instancia_desde_ruta("instances/taillard/ta001.txt")
    print(f"nombre extraído de la ruta: {nombre}")
    assert nombre == "ta001"

    ub_inexistente = obtener_mejor_conocido("ta999", "instances/taillard/best_known.csv")
    print(f"instancia inexistente: {ub_inexistente} (esperado: None)")
    assert ub_inexistente is None
