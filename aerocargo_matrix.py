cat << 'EOF' > aerocargo_matrix.py
"""
Modulo de procesamiento matricial y balance de carga en bodega de aeronaves.
"""
from typing import List, Tuple, Dict, Any

def validar_coherencia(cargas: List[List[float]], capacidades: List[List[float]]) -> bool:
    if not cargas or not capacidades:
        return False
    n_cargas, n_cap = len(cargas), len(capacidades)
    if n_cargas < 2 or n_cargas != n_cap:
        return False
    m_cargas, m_cap = len(cargas[0]), len(capacidades[0])
    if m_cargas < 2 or m_cargas != m_cap:
        return False

    for i in range(n_cargas):
        fila_carga, fila_cap = cargas[i], capacidades[i]
        if len(fila_carga) != m_cargas or len(fila_cap) != m_cap:
            return False
        for p, c in zip(fila_carga, fila_cap):
            if not isinstance(p, (int, float)) or not isinstance(c, (int, float)):
                return False
            if p < 0.0 or c <= 0.0:
                return False
    return True

def calcular_ocupacion(cargas: List[List[float]], capacidades: List[List[float]]) -> Dict[str, Any]:
    n = len(cargas)
    m = len(cargas[0])
    matriz_ocupacion = [[0.0 for _ in range(m)] for _ in range(n)]
    celdas_sobrecarga: List[Tuple[int, int]] = []

    for i in range(n):
        for j in range(m):
            porcentaje = (cargas[i][j] / capacidades[i][j]) * 100.0
            matriz_ocupacion[i][j] = round(porcentaje, 2)
            if porcentaje > 100.0:
                celdas_sobrecarga.append((i, j))

    return {
        "matriz_ocupacion": matriz_ocupacion,
        "celdas_sobrecarga": celdas_sobrecarga
    }
EOF
git add aerocargo_matrix.py
git commit -m "feat: implementar validacion dimensional y calculo de ocupacion local"
git log --oneline

def evaluar_balance(cargas: List[List[float]], tolerancia_kg: float) -> Dict[str, Any]:
    """
    Calcula pesos longitudinales por fila y el desbalance lateral en kg.
    Si M es impar, omite la columna central (eje de simetria).
    """
    n = len(cargas)
    m = len(cargas[0])
    
    pesos_longitudinales = [round(sum(fila), 2) for fila in cargas]
    
    mitad = m // 2
    suma_izq = 0.0
    suma_der = 0.0

    if m % 2 == 0:
        for fila in cargas:
            suma_izq += sum(fila[:mitad])
            suma_der += sum(fila[mitad:])
    else:
        for fila in cargas:
            suma_izq += sum(fila[:mitad])
            suma_der += sum(fila[mitad + 1:])

    desbalance_lateral = round(abs(suma_izq - suma_der), 2)
    aprobado = desbalance_lateral <= tolerancia_kg

    return {
        "pesos_longitudinales": pesos_longitudinales,
        "desbalance_lateral": desbalance_lateral,
        "balance_aprobado": aprobado
    }


def extraer_submatriz_critica(matriz_ocupacion: List[List[float]], k: int, p: int) -> List[List[float]]:
    """
    Extrae la submatriz contigua k x p con mayor promedio de ocupacion.
    """
    n = len(matriz_ocupacion)
    m = len(matriz_ocupacion[0])

    if k > n or p > m or k <= 0 or p <= 0:
        raise ValueError("Dimensiones de submatriz fuera de los limites de la matriz.")

    mejor_promedio = -1.0
    mejor_origen = (0, 0)
    total_celdas = k * p

    for i in range(n - k + 1):
        for j in range(m - p + 1):
            suma_actual = sum(
                matriz_ocupacion[i + r][j + c]
                for r in range(k)
                for c in range(p)
            )
            promedio_actual = suma_actual / total_celdas

            if promedio_actual > mejor_promedio:
                mejor_promedio = promedio_actual
                mejor_origen = (i, j)

    fila_ini, col_ini = mejor_origen
    return [
        [matriz_ocupacion[fila_ini + r][col_ini + c] for c in range(p)]
        for r in range(k)
    ]
