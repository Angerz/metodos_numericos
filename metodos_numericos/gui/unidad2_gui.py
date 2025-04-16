import customtkinter as ctk
from tkinter import filedialog
import pandas as pd
import matplotlib.pyplot as plt
import sys
import os

# Permitir imports desde la raíz del proyecto
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from core.regresion import calibrar_y_evaluar

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class CalibracionApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Unidad 2 - Calibración de Sensores")
        self.geometry("950x500")
        self.resizable(False, False)

        self.label = ctk.CTkLabel(self, text="Calibración de Sensores con Mínimos Cuadrados", font=ctk.CTkFont(size=18, weight="bold"))
        self.label.pack(pady=15)

        # Contenedor horizontal: gráfica + texto
        self.contenedor = ctk.CTkFrame(self)
        self.contenedor.pack(pady=5, padx=10, fill="both", expand=True)

        # Canvas para matplotlib
        self.canvas_frame = ctk.CTkFrame(self.contenedor)
        self.canvas_frame.pack(side="left", fill="both", expand=True, padx=10)

        self.resultado_texto = ctk.CTkTextbox(self.contenedor, width=250, font=("Courier", 13))
        self.resultado_texto.pack(side="right", fill="y", padx=10)

        # Botón para cargar CSV
        self.boton_cargar = ctk.CTkButton(self, text="Cargar archivo CSV", command=self.cargar_csv)
        self.boton_cargar.pack(pady=15)

        self.canvas = None

    def cargar_csv(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if not file_path:
            return

        try:
            df = pd.read_csv(file_path)
            nombre = file_path.split("/")[-1].replace(".csv", "")
            resultados = calibrar_y_evaluar(df, nombre=nombre)

            # Mostrar resultados
            self.resultado_texto.delete("0.0", "end")
            self.resultado_texto.insert("end", f"Archivo: {nombre}\n\n")
            self.resultado_texto.insert("end", f"Ecuación:\n{resultados['ecuacion']}\n\n")
            self.resultado_texto.insert("end", f"RMSE: {resultados['rmse']:.4f}\n")
            self.resultado_texto.insert("end", f"R²:   {resultados['r2']:.4f}\n")

            # Mostrar la imagen guardada por calibrar_y_evaluar()
            self.mostrar_grafica(nombre)

        except Exception as e:
            self.resultado_texto.delete("0.0", "end")
            self.resultado_texto.insert("end", f"❌ Error al procesar: {str(e)}\n")

    def mostrar_grafica(self, nombre):
        import os
        from matplotlib.image import imread

        imagen_path = f"metodos_numericos/data/resultados/{nombre}_ajuste.png"
        img = plt.imread(imagen_path)

        fig, ax = plt.subplots(figsize=(5.5, 4.5))
        ax.imshow(img)
        ax.axis("off")

        if self.canvas:
            self.canvas.get_tk_widget().destroy()

        self.canvas = FigureCanvasTkAgg(fig, master=self.canvas_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

if __name__ == "__main__":
    app = CalibracionApp()
    app.mainloop()
