import os
import pandas as pd
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.regresion import calibrar_y_evaluar

# Ruta donde están los archivos simulados
entrada_dir = "metodos_numericos/data/data_procesada"
salida_dir = "metodos_numericos/data/resultados"

# Evaluar cada archivo de motor (motor_1.csv, motor_2.csv, motor_3.csv)
for i in range(1, 4):
    nombre_archivo = f"motor_{i}.csv"
    path_archivo = os.path.join(entrada_dir, nombre_archivo)

    if not os.path.exists(path_archivo):
        print(f"❌ Archivo no encontrado: {path_archivo}")
        continue

    df = pd.read_csv(path_archivo)

    print(f"\n🔍 Procesando archivo: {nombre_archivo}")
    calibrar_y_evaluar(
        df,
        col_real="real",
        col_sensor="sensor",
        nombre=f"motor_{i}",
        output_dir=salida_dir
    )
