
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

#Mismos parámetros base que experimento.py: tam_poblacion=40, prob_cruza=0.9,
#prob_mutacion=0.2, num_generaciones=100, k_mejores=2.
#frecuencia_bl=50 es la que se usó para ta071 (la instancia más grande del
#set original); se reutiliza acá como punto de partida razonable, a falta
#de un valor calibrado específico para estas instancias nuevas.
FRECUENCIA_BL = 50
K_MEJORES = 2

INSTANCIAS_A_MEDIR = [
    "instances/taillard/ta090.txt",  #100x20, la más rápida del set duro reportado (78s con 128 GPUs)
    "instances/taillard/ta058.txt",  #50x20, la más costosa del set duro reportado (13h17 con 256 GPUs)
]

for ruta in INSTANCIAS_A_MEDIR:
    print(f"\n{'='*60}")
    print(f"Instancia: {ruta}")
    n, m, tiempos = leer_instancia(ruta)
    print(f"  {n} trabajos, {m} máquinas")

    print("Midiendo NEH (una vez, determinista)...")
    inicio = time.time()
    individuo_neh = construir_neh(tiempos)
    tiempo_neh = time.time() - inicio
    print(f"  NEH: {tiempo_neh:.2f}s")

    print("Midiendo una corrida de AG completa (semilla=1)...")
    random.seed(1)
    inicio = time.time()
    with contextlib.redirect_stdout(io.StringIO()):
        ejecutar_ag(tiempos, n, 40, 0.9, 0.2, 100, individuo_neh=individuo_neh)
    tiempo_ag = time.time() - inicio
    print(f"  AG: {tiempo_ag:.2f}s")

    print(f"Midiendo una corrida de Memético completa (semilla=1, frecuencia_bl={FRECUENCIA_BL}, k_mejores={K_MEJORES})...")
    random.seed(1)
    inicio = time.time()
    with contextlib.redirect_stdout(io.StringIO()):
        ejecutar_memetico(tiempos, n, 40, 0.9, 0.2, 100, FRECUENCIA_BL, K_MEJORES, individuo_neh=individuo_neh)
    tiempo_memetico = time.time() - inicio
    print(f"  Memético: {tiempo_memetico:.2f}s")

    print("\n  --- Estimación para distintos números de semillas ---")
    for n_semillas in (5, 10, 30):
        total = tiempo_neh + n_semillas * (tiempo_ag + tiempo_memetico)
        print(f"  {n_semillas} semillas (AG+Memético) + NEH x1: {total/60:.1f} min")
