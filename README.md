# AeroCargo-Matrix: Auditoria y Balance Matricial de Carga en Bahía de Aeronave

## 1. Explicación del Problema (Ingeniería Aeronáutica)
En la aviación de carga y comercial, el control de masas en bodega es crítico para la seguridad y la aeronavegabilidad:
* **Capacidad Estructural del Piso:** Cada compartimiento o celda del fuselaje cuenta con límites de carga máxima permitida por área. Superar el 100% de ocupación induce esfuerzos cortantes y de flexión que pueden producir deformaciones plásticas o fatiga prematura de la estructura.
* **Balance Lateral y Simetría:** Mantener balanceados los pesos entre babor (izquierda) y estribor (derecha) evita la generación de momentos de alabeo asimétricos, minimizando la necesidad de trimado continuo en los alerones y optimizando el consumo de combustible.
* **Distribución Longitudinal:** La suma de pesos por fila longitudinal permite monitorear la distribución del centro de gravedad (CG) respecto a los límites de estabilidad de la aeronave.

## 2. Diagrama de Arquitectura Modular
```text
               +-------------------------------------------+
               | Entradas: Cargas [NxM] y Capacidad [NxM]  |
               +-------------------------------------------+
                                     |
                                     v
                          [ validar_coherencia() ]
                                     |  (True / False)
                                     v
       +-----------------------------+-----------------------------+
       |                                                           |
       v                                                           v
[ calcular_ocupacion() ]                                  [ evaluar_balance() ]
       |                                                           |
       +--> Matriz Ocupacion (%)                                   +--> Pesos Longitudinales
       |    & Celdas Sobrecargadas                                 +--> Desbalance Lateral (kg)
       v                                                           +--> Aprobación de Balance
[ extraer_submatriz_critica(k, p) ]
       |
       +--> Submatriz k x p crítica
Análisis de Complejidad Computacional
Complejidad Temporal O(N x M):

Las funciones validar_coherencia(), calcular_ocupacion() y evaluar_balance() recorren la cuadrícula de dimensiones N x M una única vez mediante bucles anidados con operaciones aritméticas elementales de costo constante O(1).

La función extraer_submatriz_critica() evalúa (N - k + 1) x (M - p + 1) ventanas contiguas. Al tratarse de dimensiones de ventana k x p constantes respecto al tamaño total de la bodega, la cota asintótica superior se mantiene en O(N x M).

Uso de Memoria O(N x M):

Se preserva la pureza e inmutabilidad de las matrices originales al instanciar nuevas estructuras independientes para los porcentajes de ocupación (N x M) y para el vector de distribución longitudinal (N).
