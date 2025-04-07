import numpy as np
import sympy as sp
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from core.newton_raphson import newton_raphson_system

# Definimos las variables simbólicas
theta3, theta6, theta8, theta11, R10 = sp.symbols('theta3 theta6 theta8 theta11 R10')

# Parámetros constantes del mecanismo
R10_val = 35  # puedes cambiar este valor como entrada
theta4_expr = theta6 + np.deg2rad(138.74)

# Ecuaciones simbólicas (usamos radianes)
eq1 = 5.632*sp.cos(theta3) + 11.533*sp.cos(theta6) - 84.348*sp.cos(theta8) - 15
eq2 = 5.632*sp.sin(theta3) + 11.533*sp.sin(theta6) - 84.348*sp.sin(theta8) + 89.548
eq3 = 5.632*sp.cos(theta3) - 0.985*sp.cos(theta6) - 17.151*sp.sin(theta6) + 46*sp.cos(theta11) + 6.5
eq4 = 5.632*sp.sin(theta3) - 0.985*sp.sin(theta6) + 17.151*sp.cos(theta6) + 46*sp.cos(theta11) + R10

# Sistema y variables (nota que R10 es constante, se sustituye)
equations = [eq1, eq2, eq3, eq4.subs(R10, R10_val)]
variables = [theta3, theta6, theta8, theta11]

# Estimación inicial (en radianes)
initial_guess = [np.radians(10), np.radians(20), np.radians(30), np.radians(40)]

# Resolver el sistema
solution, errors, iterations = newton_raphson_system(equations, variables, initial_guess)

# Mostrar resultados
print("\n✅ Solución encontrada (en grados):")
for var, val in zip(variables, solution):
    val_norm = val % (2 * np.pi)
    print(f"{var} = {np.degrees(val_norm):.4f}°")

print(f"\n📈 Iteraciones: {iterations}")
print(f"📉 Error final: {errors[-1]:.2e}")
