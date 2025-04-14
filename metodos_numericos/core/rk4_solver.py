import numpy as np

def rk4_step(f, t, x, h, *args):
    """
    Realiza un solo paso de integración Runge-Kutta 4° orden.
    f: función del sistema f(t, x, *args)
    t: tiempo actual
    x: vector de estado actual
    h: tamaño de paso
    *args: argumentos adicionales que requiere f (como funciones externas o parámetros)
    """
    k1 = f(t, x, *args)
    k2 = f(t + h/2, x + h/2 * k1, *args)
    k3 = f(t + h/2, x + h/2 * k2, *args)
    k4 = f(t + h, x + h * k3, *args)

    return x + (h / 6) * (k1 + 2*k2 + 2*k3 + k4)

def rk4_integrate(f, x0, t_span, h, *args):
    """
    Integra el sistema f(t, x) con método RK4 desde t_span[0] hasta t_span[1].
    x0: condición inicial (array)
    h: paso de integración
    *args: argumentos adicionales para f
    """
    t0, tf = t_span
    t_values = np.arange(t0, tf + h, h)
    x_values = [x0]

    x = x0
    for t in t_values[:-1]:
        x = rk4_step(f, t, x, h, *args)
        x_values.append(x)

    return np.array(t_values), np.array(x_values)
