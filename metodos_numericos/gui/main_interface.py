import customtkinter as ctk
import subprocess
import os

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class MainMenu(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Métodos Numéricos en Ingeniería Mecatrónica")
        self.geometry("500x400")
        self.build_ui()

    def build_ui(self):
        ctk.CTkLabel(self, text="Proyecto Final - Métodos Numéricos", font=("Arial", 20, "bold")).pack(pady=30)

        ctk.CTkButton(self, text="🔧 Unidad 1: Newton-Raphson",
                      command=self.abrir_unidad1).pack(pady=10, fill="x", padx=50)

        ctk.CTkButton(self, text="📈 Unidad 2: Regresión por Mínimos Cuadrados",
                      command=self.abrir_unidad2).pack(pady=10, fill="x", padx=50)

        ctk.CTkButton(self, text="⚙️ Unidad 3: Runge-Kutta + PID",
                      command=self.abrir_unidad3).pack(pady=10, fill="x", padx=50)

        ctk.CTkLabel(self, text="Por: [Tu nombre]", font=("Arial", 12)).pack(side="bottom", pady=10)

    def abrir_unidad1(self):
        self.ejecutar_gui("unidad1_gui.py")

    def abrir_unidad2(self):
        self.ejecutar_gui("unidad2_gui.py")

    def abrir_unidad3(self):
        self.ejecutar_gui("unidad3_gui.py")

    def ejecutar_gui(self, filename):
        ruta = os.path.join("gui", filename)
        subprocess.Popen(["python3", ruta])


if __name__ == "__main__":
    app = MainMenu()
    app.mainloop()
