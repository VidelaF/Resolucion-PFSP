"""Medición rápida: una corrida de Memético en ta071 con los parámetros nuevos
(frecuencia_bl=50, k_mejores=2), más el costo de NEH aparte, para estimar el
tiempo total del experimento completo (180 corridas) antes de lanzarlo.

Uso: parado en la raíz del proyecto (junto a ag.py, memetico.py):
    python timing_check.py
"""
import contextlib
import io
import os
import random
import sys
import time

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "src"))

from leer_instancia import leer_instancia
from memetico import ejecutar_memetico
from ag import ejecutar_ag
from neh import construir_neh

RUTA_TA071 = "instances/taillard/ta071.txt"

print("Leyendo ta071.txt...")
n, m, tiempos = leer_instancia(RUTA_TA071)
print(f"  {n} trabajos, {m} máquinas")

print("\nMidiendo NEH una vez (determinista, así se usa ahora en experimento.py:")
print("una sola vez por instancia, no recalculado en cada una de las 30 semillas)...")
inicio = time.time()
individuo_neh = construir_neh(tiempos)
tiempo_neh = time.time() - inicio
print(f"  NEH: {tiempo_neh:.2f}s")

print("\nMidiendo una corrida de AG completa (semilla=1, params base, NEH ya calculado)...")
random.seed(1)
inicio = time.time()
with contextlib.redirect_stdout(io.StringIO()):
    ejecutar_ag(tiempos, n, 40, 0.9, 0.2, 100, individuo_neh=individuo_neh)
tiempo_ag = time.time() - inicio
print(f"  AG: {tiempo_ag:.2f}s")

print("\nMidiendo una corrida de Memético completa (semilla=1, frecuencia_bl=50, k_mejores=2)...")
random.seed(1)
inicio = time.time()
with contextlib.redirect_stdout(io.StringIO()):
    ejecutar_memetico(tiempos, n, 40, 0.9, 0.2, 100, 50, 2, individuo_neh=individuo_neh)
tiempo_memetico = time.time() - inicio
print(f"  Memético: {tiempo_memetico:.2f}s")

print("\n--- Estimación para el experimento completo ---")
print("(asume ta001 y ta041 mucho más rápidos, aporte principal es ta071;")
print(" NEH ya no se cuenta 30 veces, solo 1 vez por instancia como en experimento.py)")
tiempo_total_ta071 = tiempo_neh + 30 * (tiempo_ag + tiempo_memetico)
print(f"Solo ta071 (NEH x1 + 30 semillas x AG+Memético): {tiempo_total_ta071/60:.1f} min")
print("Nota: con frecuencia_bl=50 y k_mejores=2 en ta071 esto es ~2x más búsqueda")
print("local que la versión anterior (frecuencia 50, k=1) -> revisa si el tiempo")
print("de Memético aquí es aprox. el doble de los ~65s promedio medidos antes.")
