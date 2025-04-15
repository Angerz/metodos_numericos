import numpy as np

# Parámetros físicos reales del motor DC (puedes ajustar estos valores)
R = 2.0     # Resistencia (Ohm)
L = 0.5     # Inductancia (H)
J = 0.02    # Momento de inercia (kg.m^2)
b = 0.1     # Fricción viscosa (N.m.s)
K = 0.05    # Constante de torque y fuerza contraelectromotriz (Nm/A)

def motor_dc_model(t, x, V_func, R=2.0, L=0.5, J=0.02, b=0.1, K=0.05):
    """
    Modelo de un motor DC en espacio de estados.
    x[0] = theta (posición)
    x[1] = omega = d(theta)/dt (velocidad angular)
    x[2] = i (corriente del motor)
    
    V_func: función que devuelve la entrada V(t) en el tiempo t
    """
    theta, omega, i = x
    V = V_func(t)

    dx1 = omega
    dx2 = (K * i - b * omega) / J
    dx3 = (V - R * i - K * omega) / L

    return np.array([dx1, dx2, dx3])
