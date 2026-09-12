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