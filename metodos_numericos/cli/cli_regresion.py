import pandas as pd
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from core.regresion import simular_sensores, aplicar_regresion

# Configuración inicial
csv_path = "metodos_numericos/data/datos_motores.csv"
sep = ";"  # Separador del archivo original

# 1. Leer el archivo CSV
df = pd.read_csv(csv_path, sep=sep, encoding="latin1")

# 2. Definir columnas de entrada (real)
columnas_reales = [f"Posición Motor {i}" for i in range(1, 3)]

# 3. Generar sensores simulados
df_sim = simular_sensores(df, columnas_reales)

# 4. Aplicar regresión y mostrar resultados para cada motor
for i in range(1, 5):
    col_real = f"Posición Motor {i}"
    col_sim = f"Sensor Simulado {i}"

    print(f"\n📌 Motor {i}")
    resultados = aplicar_regresion(df_sim, col_real, col_sim, graficar=True)

    print(f"Regresión: {resultados['ecuacion']}")
    print(f"RMSE = {resultados['rmse']:.4f}")
    print(f"R² = {resultados['r2']:.4f}")
