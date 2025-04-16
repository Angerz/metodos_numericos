import customtkinter as ctk
import numpy as np
import sympy as sp
import sys
import os

# Agregar el path del core
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.newton_raphson import newton_raphson_system

# Configuración inicial de la GUI
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

# Ventana principal
class NewtonGUI(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Unidad 1 - Newton-Raphson")
        self.geometry("600x480")

        # Título
        self.title_label = ctk.CTkLabel(self, text="Análisis Posicional - Newton-Raphson", font=ctk.CTkFont(size=20, weight="bold"))
        self.title_label.pack(pady=12)

        # Inputs
        self.inputs_frame = ctk.CTkFrame(self)
        self.inputs_frame.pack(pady=10)

        self.r10 = self._create_input("R10:", "20")
        # Botón de ejecución
        self.solve_button = ctk.CTkButton(self, text="Ejecutar", command=self.solve_system)
        self.solve_button.pack(pady=10)

        # Área de resultados
        self.result_box = ctk.CTkTextbox(self, height=160, width=500)
        self.result_box.pack(pady=10)

    def _create_input(self, label, default):
        frame = ctk.CTkFrame(self.inputs_frame)
        frame.pack(pady=4, padx=10, fill="x")
        lbl = ctk.CTkLabel(frame, text=label)
        lbl.pack(side="left", padx=10)
        entry = ctk.CTkEntry(frame)
        entry.insert(0, default)
        entry.pack(side="right", expand=True, fill="x", padx=10)
        return entry

    def solve_system(self):
        try:
            # Variables simbólicas
            theta3, theta6, theta8, theta11, R10 = sp.symbols('theta3 theta6 theta8 theta11 R10')

            # Ecuaciones
            eq1 = 5.632*sp.cos(theta3) + 11.533*sp.cos(theta6) - 84.348*sp.cos(theta8) - 15
            eq2 = 5.632*sp.sin(theta3) + 11.533*sp.sin(theta6) - 84.348*sp.sin(theta8) + 89.548
            eq3 = 5.632*sp.cos(theta3) - 0.985*sp.cos(theta6) - 17.151*sp.sin(theta6) + 46*sp.cos(theta11) + 6.5
            eq4 = 5.632*sp.sin(theta3) - 0.985*sp.sin(theta6) + 17.151*sp.cos(theta6) + 46*sp.cos(theta11) + R10

            equations = [eq1, eq2, eq3, eq4.subs(R10, float(self.r10.get()))]
            variables = [theta3, theta6, theta8, theta11]

            initial_guess = [np.radians(10), np.radians(20), np.radians(30), np.radians(40)]

            solution, errors, iterations = newton_raphson_system(equations, variables, initial_guess)

            output = "✅ Solución encontrada (en grados):\n"
            for var, val in zip(variables, solution):
                val_norm = val % (2 * np.pi)
                output += f"{var} = {np.degrees(val_norm):.4f}°\n"

            output += f"\n📈 Iteraciones: {iterations}\n📉 Error final: {errors[-1]:.2e}"

            self.result_box.delete("0.0", "end")
            self.result_box.insert("0.0", output)

        except Exception as e:
            self.result_box.delete("0.0", "end")
            self.result_box.insert("0.0", f"❌ Error: {str(e)}")

if __name__ == "__main__":
    app = NewtonGUI()
    app.mainloop()
