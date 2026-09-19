import csv
import os


def obtener_mejor_conocido(nombre_instancia, ruta_csv):
    with open(ruta_csv, "r") as archivo:
        lector = csv.DictReader(archivo)
        for fila in lector:
            if fila["Name"] == nombre_instancia:
                return int(fila["UB"])
    return None


def calcular_rpd(cmax_obtenido, mejor_conocido):
    """rpd(%) = (cmax_obtenido - mejor_conocido) / mejor_conocido * 100. 0% = igualó el mejor conocido."""
    return (cmax_obtenido - mejor_conocido) / mejor_conocido * 100


def nombre_instancia_desde_ruta(ruta_instancia):
    """nombre de la instancia sin extensión, ej. ta001, a partir de su ruta de archivo."""
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
