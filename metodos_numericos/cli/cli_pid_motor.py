import numpy as np
import matplotlib.pyplot as plt
import sys
import os

# Añadir el directorio raíz al path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.motor_model import motor_dc_model
from core.rk4_solver import rk4_step
from core.pid_controller import PID

# Parámetros de simulación
t0, tf = 5.0, 10.0
h = 0.001
t_values = np.arange(t0, tf + h, h)

# Condiciones iniciales
x0 = np.array([0.0, 0.0, 0.0])  # [theta, omega, i]
x = x0.copy()
x_hist = [x]
V_hist = []

# Setpoint fijo
theta_ref = 1.0  # radianes
error_hist = [theta_ref - x[0]]

# PID definido por el usuario
pid = PID(Kp=30.0, Ki=1.0, Kd=20.0)

# Función para simular en lazo cerrado
def motor_controlado(t, x, *args):
    theta = x[0]
    error = theta_ref - theta
    V = pid.update(error, h)
    V = np.clip(V, -24, 24)  # Saturación opcional
    return motor_dc_model(t, x, lambda t: V)

def calcular_aceleracion(omega, h):
    a = np.zeros_like(omega)
    a[1:-1] = (omega[2:] - omega[:-2]) / (2 * h)
    a[0] = a[1]    # evitar borde
    a[-1] = a[-2]  # evitar borde
    return a


# Simulación paso a paso (manual para capturar evolución del PID)
for t in t_values[:-1]:
    x = rk4_step(motor_controlado, t, x, h)
    x_hist.append(x)
    error_hist.append(theta_ref - x[0])

x_hist = np.array(x_hist)
aceleracion = calcular_aceleracion(x_hist[:, 1], h)

# Gráficas
plt.figure(figsize=(10, 8))

plt.subplot(5, 1, 1)
plt.plot(t_values, x_hist[:, 0])
plt.axhline(theta_ref, color='gray', linestyle='--', label='Setpoint')
plt.ylabel("θ(t) [rad]")
plt.grid(True)
plt.title("Posición angular")
plt.legend()

plt.subplot(5, 1, 2)
plt.plot(t_values, x_hist[:, 1])
plt.ylabel("ω(t) [rad/s]")
plt.grid(True)
plt.title("Velocidad angular")

plt.subplot(5, 1, 3)
plt.plot(t_values, aceleracion)
plt.ylabel("α(t) [rad/s²]")
plt.xlabel("Tiempo [s]")
plt.grid(True)
plt.title("Aceleración angular")

plt.subplot(5, 1, 4)
plt.plot(t_values, x_hist[:, 2])
plt.ylabel("i(t) [A]")
plt.grid(True)
plt.title("Corriente")

plt.subplot(5, 1, 5)
plt.plot(t_values, error_hist)
plt.ylabel("Error [rad]")
plt.xlabel("Tiempo [s]")
plt.grid(True)
plt.title("Error de seguimiento")

plt.tight_layout()
plt.show()