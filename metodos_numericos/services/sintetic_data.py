import pandas as pd
import numpy as np
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def generar_datos_sinteticos(
    csv_path,
    salida_dir="metodos_numericos/data/data_procesada",
    sep=";",
    ruido_std=0.5,
    semilla=42
):
    np.random.seed(semilla) #* para que los datos sean reproducibles, comentar para datos aleatorios
    df = pd.read_csv(csv_path, sep=sep, encoding="latin1")
    os.makedirs(salida_dir, exist_ok=True)

    for i in range(1, 4):
        col = f"Posición Motor {i}"
        if col not in df.columns:
            print(f"Columna no encontrada: {col}")
            continue

        real = df[col].values

        alpha = np.random.uniform(0.9, 1.1  )   # ganancia
        beta = np.random.uniform(-1, 1)     # offset
        ruido = np.random.normal(0, ruido_std, size=len(real))

        sensor = alpha * real + beta + ruido

        df_out = pd.DataFrame({
            "real": real,
            "sensor": sensor
        })

        out_path = os.path.join(salida_dir, f"motor_{i}.csv")
        df_out.to_csv(out_path, index=False)

        print(f"✅ Archivo generado: {out_path} | α = {alpha:.4f}, β = {beta:.4f}, ruido = {ruido_std:.4f}")

if __name__ == "__main__":
    csv_path = "metodos_numericos/data/datos_motores.csv"
    generar_datos_sinteticos(csv_path)

