"""
Script principal de demostracion para AeroCargo-Matrix.
"""
from aerocargo_matrix import (
    validar_coherencia,
    calcular_ocupacion,
    evaluar_balance,
    extraer_submatriz_critica
)

def imprimir_matriz(matriz, formato="{:8.2f}"):
    for fila in matriz:
        print("  " + " ".join(formato.format(val) for val in fila))

def main():
    print("=" * 60)
    print("     AEROCARGO-MATRIX: AUDITORIA DE CARGA Y BALANCE")
    print("=" * 60)

    cargas = [
        [450.0, 300.0, 500.0, 290.0, 460.0],
        [620.0, 580.0, 400.0, 600.0, 590.0],
        [310.0, 305.0, 200.0, 310.0, 320.0],
        [750.0, 800.0, 450.0, 200.0, 250.0]
    ]

    capacidades = [
        [500.0, 500.0, 500.0, 500.0, 500.0],
        [600.0, 600.0, 600.0, 600.0, 600.0],
        [400.0, 400.0, 400.0, 400.0, 400.0],
        [700.0, 700.0, 700.0, 700.0, 700.0]
    ]

    tolerancia_lateral = 150.0

    print("\n[1] Validacion de Matrices:")
    es_valido = validar_coherencia(cargas, capacidades)
    print(f"  Estado: {'APROBADA' if es_valido else 'RECHAZADA'}")
    if not es_valido:
        return

    res_ocupacion = calcular_ocupacion(cargas, capacidades)
    print("\n[2] Matriz de Ocupacion Local (%):")
    imprimir_matriz(res_ocupacion["matriz_ocupacion"])
    print(f"\nCeldas sobrecargadas (> 100%): {res_ocupacion['celdas_sobrecarga']}")

    res_balance = evaluar_balance(cargas, tolerancia_lateral)
    print("\n[3] Analisis de Balance:")
    print(f"  - Cargas longitudinales por fila: {res_balance['pesos_longitudinales']} kg")
    print(f"  - Desbalance lateral: {res_balance['desbalance_lateral']} kg")
    print(f"  - Tolerancia permitida: {tolerancia_lateral} kg")
    print(f"  - Estado de balance: {'APROBADO' if res_balance['balance_aprobado'] else 'EXCEDIDO'}")

    k, p = 2, 2
    submatriz = extraer_submatriz_critica(res_ocupacion["matriz_ocupacion"], k, p)
    print(f"\n[4] Submatriz Critica ({k}x{p}) con Mayor Ocupacion Promedio:")
    imprimir_matriz(submatriz)

if __name__ == "__main__":
    main()
