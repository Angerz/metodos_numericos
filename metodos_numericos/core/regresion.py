import json
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error
import matplotlib.pyplot as plt
import pandas as pd

def calibrar_y_evaluar(df, col_real='real', col_sensor='sensor', nombre='sensor', output_dir='metodos_numericos/data/resultados', test_size=0.2, random_state=42):
    '''
    Realiza calibración de sensor por mínimos cuadrados:
    - Divide el dataset en entrenamiento/test
    - Ajusta modelo lineal con mínimos cuadrados
    - Evalúa RMSE, MAE, R²
    - Guarda resultados, gráfico y modelo
    '''
    import os
    import numpy as np
    from numpy.polynomial.polynomial import Polynomial
    from sklearn.metrics import mean_squared_error, r2_score

    os.makedirs(output_dir, exist_ok=True)

    X = df[col_sensor].values
    y = df[col_real].values

    # División en train/test
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=random_state)

    # Ajuste por mínimos cuadrados (lineal)
    coefs = Polynomial.fit(X_train, y_train, deg=1).convert().coef
    a, b = coefs

    # Predicciones sobre test
    y_pred = a + b * X_test

    # Métricas
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    mae = mean_absolute_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)

    # Guardar gráfico
    plt.figure(figsize=(6, 4))
    plt.scatter(X_test, y_test, label='Valores reales', alpha=0.6)
    plt.plot(X_test, y_pred, color='red', label='Regresión ajustada')
    plt.xlabel('Sensor')
    plt.ylabel('Real')
    plt.title(f'Motor: {nombre} | RMSE={rmse:.2f}, R²={r2:.2f}')
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plot_path = os.path.join(output_dir, f'{nombre}_ajuste.png')
    plt.savefig(plot_path)
    plt.close()

    # Guardar CSV con resultados
    df_result = pd.DataFrame({
        'real': y_test,
        'sensor': X_test,
        'estimado': y_pred,
        'error': y_test - y_pred
    })
    df_result.to_csv(os.path.join(output_dir, f'{nombre}_resultados.csv'), index=False)

    # Guardar modelo (coeficientes)
    modelo = {
        'ecuacion': f'y = {a:.4f} + {b:.4f}·x',
        'coeficientes': {'a': a, 'b': b},
        'rmse': rmse,
        'mae': mae,
        'r2': r2
    }
    with open(os.path.join(output_dir, f'{nombre}_modelo.json'), 'w') as f:
        json.dump(modelo, f, indent=4)

    print(f"✅ Motor {nombre} | y = {a:.4f} + {b:.4f}·x | RMSE={rmse:.4f} | R²={r2:.4f}")
    return modelo
