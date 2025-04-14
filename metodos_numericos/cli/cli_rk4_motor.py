import numpy as np
import matplotlib.pyplot as plt
import sys
import os

# Permitir imports desde la raíz del proyecto
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.motor_model import motor_dc_model
from core.rk4_solver import rk4_integrate

# Función de entrada: escalón de 24V constante
def V_constante(t):
    return 24.0

# Condiciones iniciales
x0 = np.array([0.0, 0.0, 0.0])  # theta, omega, i
t0, tf = 0.0, 5.0
h = 0.001

# Simulación
print("🔧 Simulando motor DC con RK4...")
t, x = rk4_integrate(motor_dc_model, x0, (t0, tf), h, V_constante)

# Resultados
theta = x[:, 0]
omega = x[:, 1]
corriente = x[:, 2]

# Gráficos
plt.figure(figsize=(10, 7))

plt.subplot(3, 1, 1)
plt.plot(t, theta)
plt.ylabel("θ(t) [rad]")
plt.grid(True)
plt.title("Posición angular")

plt.subplot(3, 1, 2)
plt.plot(t, omega)
plt.ylabel("ω(t) [rad/s]")
plt.grid(True)
plt.title("Velocidad angular")

plt.subplot(3, 1, 3)
plt.plot(t, corriente)
plt.ylabel("i(t) [A]")
plt.xlabel("Tiempo [s]")
plt.grid(True)
plt.title("Corriente del motor")

plt.tight_layout()
plt.show()
