import PySimpleGUI as sg
import numpy as np
import sympy as sp
import sys
import os

# Permitir imports desde la raíz del proyecto
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.newton_raphson import newton_raphson_system

# Variables simbólicas
theta3, theta6, theta8, theta11, R10 = sp.symbols('theta3 theta6 theta8 theta11 R10')

# Ecuaciones simbólicas
eq1 = 5.632*sp.cos(theta3) + 11.533*sp.cos(theta6) - 84.348*sp.cos(theta8) - 15
eq2 = 5.632*sp.sin(theta3) + 11.533*sp.sin(theta6) - 84.348*sp.sin(theta8) + 89.548
eq3 = 5.632*sp.cos(theta3) - 0.985*sp.cos(theta6) - 17.151*sp.sin(theta6) + 46*sp.cos(theta11) + 6.5
eq4 = 5.632*sp.sin(theta3) - 0.985*sp.sin(theta6) + 17.151*sp.cos(theta6) + 46*sp.cos(theta11) + R10

# Layout
layout = [
    [sg.Text('Análisis Posicional por Newton-Raphson', font=('Helvetica', 14), justification='center')],
    [sg.Text('Ingrese los valores iniciales (en grados):')],
    [sg.Text('θ3:'), sg.InputText('10', key='theta3'), sg.Text('θ6:'), sg.InputText('20', key='theta6')],
    [sg.Text('θ8:'), sg.InputText('30', key='theta8'), sg.Text('θ11:'), sg.InputText('40', key='theta11')],
    [sg.Text('R10:'), sg.InputText('20.0', key='R10')],
    [sg.Button('Ejecutar'), sg.Button('Salir')],
    [sg.Text('Resultado:', font=('Helvetica', 12))],
    [sg.Multiline(size=(60, 10), key='output')]
]

window = sg.Window('Unidad 1 - Newton-Raphson', layout)

while True:
    event, values = window.read()
    if event in (sg.WIN_CLOSED, 'Salir'):
        break

    if event == 'Ejecutar':
        try:
            # Parseo de entradas
            t3 = np.radians(float(values['theta3']))
            t6 = np.radians(float(values['theta6']))
            t8 = np.radians(float(values['theta8']))
            t11 = np.radians(float(values['theta11']))
            r10_val = float(values['R10'])

            initial_guess = [t3, t6, t8, t11]

            equations = [eq1, eq2, eq3, eq4.subs(R10, r10_val)]
            variables = [theta3, theta6, theta8, theta11]

            solution, errors, iterations = newton_raphson_system(equations, variables, initial_guess)

            output_text = ''
            for var, val in zip(variables, solution):
                val_norm = val % (2 * np.pi)
                output_text += f"{var} = {np.degrees(val_norm):.4f}°\n"

            output_text += f"\nIteraciones: {iterations}\nError final: {errors[-1]:.2e}"

            window['output'].update(output_text)

        except Exception as e:
            window['output'].update(f"❌ Error: {str(e)}")

window.close()
