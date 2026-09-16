# PFSP - Algoritmo Genético y Algoritmo Memético

Resolución del *Permutation Flow Shop Scheduling Problem* (PFSP) mediante
algoritmos evolutivos: un Algoritmo Genético (AG) y un Algoritmo Memético
(AG + búsqueda local).

## El problema

Dados n trabajos que deben pasar, en el mismo orden, por m máquinas, se
busca la permutación (secuencia de trabajos) que minimiza el makespan
(Cmax): el tiempo en que termina el último trabajo en la última máquina.

## Estructura del proyecto

Programas ejecutables (raíz del proyecto):

- `ag.py` — Algoritmo Genético puro.
- `memetico.py` — Algoritmo Memético (AG + búsqueda local aplicada al
  mejor individuo cada N generaciones).

Módulos reutilizables (biblioteca), en `src/`:

- `leer_instancia.py` — parsea instancias en formato Taillard.
- `leer_parametros_ag.py` — parseo y validación de parámetros de `ag.py`.
- `leer_parametros_memetico.py` — parseo y validación de parámetros de
  `memetico.py`.
- `aleatorios.py` — generadores de número real/entero aleatorio.
- `poblacion.py` — inicialización de la población (permutaciones aleatorias).
- `fitness.py` — cálculo del makespan (tabla de tiempos de finalización C(i,j)).
- `seleccion.py` — selección por torneo.
- `cruce.py` — cruce OX (Order Crossover), válido para permutaciones.
- `mutacion.py` — mutación por intercambio (swap).
- `busqueda_local.py` — insertion local search, first-improvement
  (usada por el Memético).
- `reemplazo.py` — genera la siguiente generación (selección + cruce +
  mutación), con elitismo opcional.
- `neh.py` — heurística constructiva NEH (Nawaz, Enscore y Ham, 1983),
  usada para sembrar un individuo de buena calidad en la población
  inicial del AG y del Memético.
- `rpd.py` — cálculo del RPD (Relative Percentage Deviation) contra el
  mejor valor conocido de cada instancia.

Mejoras incorporadas sobre la versión base (ver también la sección
"Trabajo de Investigación" del informe):

- **Semilla NEH**: en `ag.py` y `memetico.py`, un individuo de la
  población inicial se reemplaza por la solución de `neh.construir_neh`
  en vez de ser aleatorio.
- **Mutación adaptativa**: `prob_mutacion` se interpreta como valor
  inicial y decae linealmente hasta el 10% de ese valor en la última
  generación (más exploración al principio, más explotación al final).

`ag.py` y `memetico.py` agregan `src/` a `sys.path` al iniciar, así que
importan estos módulos igual que si estuvieran en la misma carpeta.

Datos:

- `instances/taillard/` — instancias estándar de Taillard (1993) y
  `best_known.csv` con los mejores valores conocidos (LB, UB, y si el
  óptimo está confirmado), actualizado con resultados de
  Gmys (2022, *INFORMS Journal on Computing*).

## Requisitos

```
pip install -r requirements.txt
```

## Uso

Algoritmo Genético:

```
python ag.py <semilla> <instancia> <tam_poblacion> <prob_cruza> <prob_mutacion> <num_generaciones>
```

Ejemplo:

```
python ag.py 7 instances/taillard/ta001.txt 40 0.9 0.2 15
```

Algoritmo Memético (agrega la frecuencia de búsqueda local, y opcionalmente
cuántos de los mejores individuos la reciben en cada aplicación):

```
python memetico.py <semilla> <instancia> <tam_poblacion> <prob_cruza> <prob_mutacion> <num_generaciones> <frecuencia_bl> [k_mejores]
```

Ejemplo (k_mejores omitido, por defecto 1: solo el mejor individuo):

```
python memetico.py 7 instances/taillard/ta001.txt 40 0.9 0.2 15 3
```

Ejemplo aplicando búsqueda local a los 2 mejores individuos en cada aplicación:

```
python memetico.py 7 instances/taillard/ta001.txt 40 0.9 0.2 15 3 2
```

Ambos programas imprimen el progreso por generación, la mejor secuencia
encontrada, su makespan y el RPD respecto al mejor valor conocido para
esa instancia.
