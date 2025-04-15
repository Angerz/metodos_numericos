class PID:
    def __init__(self, Kp=1.0, Ki=0.0, Kd=0.0):
        self.Kp = Kp
        self.Ki = Ki
        self.Kd = Kd
        self.integral = 0.0
        self.prev_error = 0.0

    def reset(self):
        """Reinicia el estado interno del controlador."""
        self.integral = 0.0
        self.prev_error = 0.0

    def update(self, error, dt):
        """Calcula la salida del PID dado un error y un paso de tiempo."""
        self.integral += error * dt
        derivative = (error - self.prev_error) / dt if dt > 0 else 0.0
        self.prev_error = error

        u = (
            self.Kp * error +
            self.Ki * self.integral +
            self.Kd * derivative
        )
        return u
