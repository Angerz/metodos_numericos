import numpy as np
import sympy as sp

def newton_raphson_system(equations, variables, initial_guess, tol=1e-6, max_iter=200):
    """
    Resuelve un sistema de ecuaciones no lineales usando Newton-Raphson multivariable.

    :param equations: lista de expresiones simbólicas (sympy)
    :param variables: lista de variables simbólicas (sympy)
    :param initial_guess: lista de valores iniciales (float)
    :param tol: tolerancia para el error
    :param max_iter: número máximo de iteraciones
    :return: solución aproximada, historial de errores, número de iteraciones
    """
    F = sp.Matrix(equations)
    J = F.jacobian(variables)

    # Convertimos F y J a funciones numéricas (lambdify)
    f_lambd = sp.lambdify(variables, F, 'numpy')
    J_lambd = sp.lambdify(variables, J, 'numpy')

    x = np.array(initial_guess, dtype=float)
    errors = []

    for i in range(max_iter):
        Fx = np.array(f_lambd(*x), dtype=float).flatten()
        Jx = np.array(J_lambd(*x), dtype=float)

        try:
            delta = np.linalg.solve(Jx, -Fx)
        except np.linalg.LinAlgError:
            raise ValueError("El Jacobiano no es invertible en la iteración", i)

        x_new = x + delta
        error = np.linalg.norm(delta)
        errors.append(error)

        if error < tol:
            return x_new, errors, i + 1

        x = x_new

    raise ValueError("El método no convergió en el número máximo de iteraciones.")

