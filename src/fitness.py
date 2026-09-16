def calcular_tabla_tiempos_finalizacion(secuencia, tiempos):
    """tabla c(i,j): tiempo en que el trabajo i de la secuencia termina en la máquina j.
    c(i,j) = max(c(i-1,j), c(i,j-1)) + p(secuencia[i], j)."""
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
    """makespan (cmax): última celda de la tabla c(i,j)."""
    tabla = calcular_tabla_tiempos_finalizacion(secuencia, tiempos)
    return tabla[-1][-1]


if __name__ == "__main__":
    # ejemplo del enunciado: 3 trabajos, 2 máquinas
    # trabajo  m1  m2
    # j1        5   3
    # j2        2   6
    # j3        4   4
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

    # sanity check con ta001
    from leer_instancia import leer_instancia

    n, m, tiempos = leer_instancia("instances/taillard/ta001.txt")
    secuencia_identidad = list(range(n))
    makespan_ta001 = calcular_makespan(secuencia_identidad, tiempos)
    print(f"\nta001.txt, secuencia identidad (1..{n}) -> Cmax = {makespan_ta001}")
    print("(el mejor conocido para ta001 es 1278; la secuencia identidad no")
    print(" tiene por qué acercarse, es solo para validar que no hay errores)")
