import customtkinter as ctk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import sys
import os

# Añadir el directorio raíz al path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.motor_model import motor_dc_model
from core.rk4_solver import rk4_step
from core.pid_controller import PID

# Inicialización
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")


class MotorSimulatorApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Unidad 3 - Motor DC con PID (RK4)")
        self.geometry("900x600")
        self.motor_params = {}
        self.show_motor_page()

    def show_motor_page(self):
        self.clear_window()
        self.motor_frame = ctk.CTkFrame(self)
        self.motor_frame.pack(padx=20, pady=20)

        ctk.CTkLabel(self.motor_frame, text="Parámetros del Motor DC", font=("Arial", 18)).pack(pady=10)

        self.entries_motor = {}
        for name, default in zip(["R", "L", "J", "b", "K"], [2.0, 0.5, 0.02, 0.1, 0.05]):
            frame = ctk.CTkFrame(self.motor_frame)
            frame.pack(pady=5, fill="x")
            ctk.CTkLabel(frame, text=f"{name}:", width=50).pack(side="left", padx=10)
            entry = ctk.CTkEntry(frame, placeholder_text=str(default))
            entry.pack(side="left", fill="x", expand=True)
            self.entries_motor[name] = entry

        ctk.CTkButton(self.motor_frame, text="Continuar →", command=self.show_pid_page).pack(pady=15)

    def show_pid_page(self):
        # Guardar parámetros del motor
        try:
            self.motor_params = {k: float(e.get()) for k, e in self.entries_motor.items()}
        except ValueError:
            ctk.CTkLabel(self.motor_frame, text="⚠️ Verifica que todos los valores sean numéricos.").pack()
            return

        self.clear_window()
        self.pid_frame = ctk.CTkFrame(self)
        self.pid_frame.pack(padx=20, pady=20, fill="both", expand=True)

        ctk.CTkLabel(self.pid_frame, text="Controlador PID y Setpoint", font=("Arial", 18)).pack(pady=10)

        self.setpoint = ctk.CTkEntry(self.pid_frame, placeholder_text="Setpoint (rad)", width=100)
        self.setpoint.pack(pady=10)

        self.entries_pid = {}
        for name, default in zip(["Kp", "Ki", "Kd"], [30.0, 1.0, 20.0]):
            frame = ctk.CTkFrame(self.pid_frame)
            frame.pack(pady=5, fill="x")
            ctk.CTkLabel(frame, text=f"{name}:", width=50).pack(side="left", padx=10)
            entry = ctk.CTkEntry(frame, placeholder_text=str(default))
            entry.pack(side="left", fill="x", expand=True)
            self.entries_pid[name] = entry

        ctk.CTkButton(self.pid_frame, text="Simular", command=self.simular_motor).pack(pady=20)

        self.result_frame = ctk.CTkFrame(self.pid_frame)
        self.result_frame.pack(fill="both", expand=True)

    def simular_motor(self):
        try:
            setpoint = float(self.setpoint.get())
            Kp = float(self.entries_pid["Kp"].get())
            Ki = float(self.entries_pid["Ki"].get())
            Kd = float(self.entries_pid["Kd"].get())
        except ValueError:
            ctk.CTkLabel(self.pid_frame, text="⚠️ Verifica que los valores del PID y setpoint sean numéricos.").pack()
            return

        # Parámetros y estado inicial
        R, L, J, b, K = [self.motor_params[k] for k in ["R", "L", "J", "b", "K"]]
        x = np.array([0.0, 0.0, 0.0])
        x_hist = [x]
        h = 0.001
        t_values = np.arange(0, 5.0 + h, h)
        error_hist = [setpoint - x[0]]

        # Controlador PID
        pid = PID(Kp, Ki, Kd)

        def motor_controlado(t, x, *args):
            theta = x[0]
            error = setpoint - theta
            V = pid.update(error, h)
            V = np.clip(V, -24, 24)
            return motor_dc_model(t, x, lambda t: V, R, L, J, b, K)

        for t in t_values[:-1]:
            x = rk4_step(motor_controlado, t, x, h)
            x_hist.append(x)
            error_hist.append(setpoint - x[0])

        x_hist = np.array(x_hist)

        def calcular_aceleracion(omega, h):
            a = np.zeros_like(omega)
            a[1:-1] = (omega[2:] - omega[:-2]) / (2 * h)
            a[0] = a[1]
            a[-1] = a[-2]
            return a

        alpha = calcular_aceleracion(x_hist[:, 1], h)

        # Graficar
        fig, axs = plt.subplots(5, 1, figsize=(8, 9))
        axs[0].plot(t_values, x_hist[:, 0])
        axs[0].axhline(setpoint, color='gray', linestyle='--')
        axs[0].set_ylabel("θ(t) [rad]")
        axs[0].set_title("Posición angular")
        axs[0].grid(True)

        axs[1].plot(t_values, x_hist[:, 1])
        axs[1].set_ylabel("ω(t) [rad/s]")
        axs[1].set_title("Velocidad angular")
        axs[1].grid(True)

        axs[2].plot(t_values, alpha)
        axs[2].set_ylabel("α(t) [rad/s²]")
        axs[2].set_title("Aceleración angular")
        axs[2].grid(True)

        axs[3].plot(t_values, x_hist[:, 2])
        axs[3].set_ylabel("i(t) [A]")
        axs[3].set_title("Corriente")
        axs[3].grid(True)

        axs[4].plot(t_values, error_hist)
        axs[4].set_ylabel("Error [rad]")
        axs[4].set_xlabel("Tiempo [s]")
        axs[4].set_title("Error de seguimiento")
        axs[4].grid(True)

        plt.tight_layout()

        # Mostrar en la GUI
        for widget in self.result_frame.winfo_children():
            widget.destroy()

        canvas = FigureCanvasTkAgg(fig, master=self.result_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

    def clear_window(self):
        for widget in self.winfo_children():
            widget.destroy()


if __name__ == "__main__":
    app = MotorSimulatorApp()
    app.mainloop()
