def calcular_tabla_tiempos_finalizacion(secuencia, tiempos):
    """Construye la tabla completa de tiempos de finalización C(i,j) para
    una secuencia de trabajos, tal como se describe en el enunciado.

    secuencia: lista de índices de trabajos (0-indexados), en el orden
        en que se procesan. Debe ser una permutación de range(n_trabajos).
    tiempos: matriz de tiempos de procesamiento, filas = máquinas,
        columnas = trabajos (tiempos[maquina][trabajo]).

    Retorna una matriz (lista de listas) de tamaño n_trabajos x
    n_maquinas. tabla[i][j] es C(i,j): el tiempo en que el i-ésimo
    trabajo de la secuencia termina de procesarse en la máquina j.

    Se calcula con la recurrencia:
        C(i,j) = max(C(i-1,j), C(i,j-1)) + p(secuencia[i], j)
    donde C(i-1,j) es el tiempo en que la máquina j quedó libre del
    trabajo anterior, y C(i,j-1) es el tiempo en que el trabajo actual
    quedó disponible al salir de la máquina anterior. Para el primer
    trabajo (i=0) y la primera máquina (j=0) esos valores son 0.
    """
    n_trabajos = len(secuencia)
    n_maquinas = len(tiempos)

    tabla = [[0] * n_maquinas for _ in range(n_trabajos)]

    for i in range(n_trabajos):
        trabajo = secuencia[i]
        for j in range(n_maquinas):
            maquina_libre_desde = tabla[i - 1][j] if i > 0 else 0
            trabajo_disponible_desde = tabla[i][j - 1] if j > 0 else 0
            tabla[i][j] = max(maquina_libre_desde, trabajo_disponible_desde) + tiempos[j][trabajo]

    return tabla


def calcular_makespan(secuencia, tiempos):
    """Calcula el makespan (Cmax) de una secuencia de trabajos en un flow shop.

    Arma la tabla completa de tiempos de finalización C(i,j) (ver
    calcular_tabla_tiempos_finalizacion) y retorna su última celda: el
    tiempo en que termina el último trabajo de la secuencia en la
    última máquina, que es la definición de Cmax.
    """
    tabla = calcular_tabla_tiempos_finalizacion(secuencia, tiempos)
    return tabla[-1][-1]


if __name__ == "__main__":
    # Ejemplo del enunciado (sección 3): 3 trabajos, 2 máquinas.
    # Trabajo  M1  M2
    # J1        5   3
    # J2        2   6
    # J3        4   4
    tiempos_ejemplo = [
        [5, 2, 4],  # M1: J1, J2, J3
        [3, 6, 4],  # M2: J1, J2, J3
    ]

    secuencia_123 = [0, 1, 2]  # π = (J1, J2, J3)
    tabla_123 = calcular_tabla_tiempos_finalizacion(secuencia_123, tiempos_ejemplo)
    print("Tabla C(i,j) para π = (J1, J2, J3):")
    print("            M1    M2")
    for i in range(len(secuencia_123)):
        print(f"  J{secuencia_123[i] + 1}:      {tabla_123[i][0]:>4}  {tabla_123[i][1]:>4}")
    makespan_123 = calcular_makespan(secuencia_123, tiempos_ejemplo)
    print(f"Cmax = {makespan_123} (esperado: 18)")
    assert makespan_123 == 18, "el cálculo no coincide con el ejemplo del enunciado"

    print()
    secuencia_213 = [1, 0, 2]  # π = (J2, J1, J3)
    makespan_213 = calcular_makespan(secuencia_213, tiempos_ejemplo)
    print(f"π = (J2, J1, J3) -> Cmax = {makespan_213}")

    # Sanity check con una instancia real de Taillard.
    from leer_instancia import leer_instancia

    n, m, tiempos = leer_instancia("instances/taillard/ta001.txt")
    secuencia_identidad = list(range(n))
    makespan_ta001 = calcular_makespan(secuencia_identidad, tiempos)
    print(f"\nta001.txt, secuencia identidad (1..{n}) -> Cmax = {makespan_ta001}")
    print("(el mejor conocido para ta001 es 1278; la secuencia identidad no")
    print(" tiene por qué acercarse, es solo para validar que no hay errores)")
