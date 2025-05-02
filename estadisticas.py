import json
import os
from datetime import datetime

class EstadisticasPomodoro:
    def __init__(self, archivo='sesiones_diarias.json'):
        self.archivo = archivo
        self.sesiones_diarias = {}
        self.cargar()

    def incrementar(self, es_pomodoro):
        """Solo incrementa si es una sesión de Pomodoro."""
        if es_pomodoro:  # Solo incrementamos si es una sesión de Pomodoro
            fecha_actual = datetime.now().strftime('%Y-%m-%d')
            if fecha_actual not in self.sesiones_diarias:
                self.sesiones_diarias[fecha_actual] = 0
            self.sesiones_diarias[fecha_actual] += 1
            self.guardar()

    def obtener_sesiones(self):
        return self.sesiones_diarias

    def guardar(self):
        """Guarda las estadísticas de sesiones."""
        try:
            with open(self.archivo, 'w') as f:
                json.dump(self.sesiones_diarias, f)
        except Exception as e:
            print(f"Error al guardar estadísticas: {e}")

    def cargar(self):
        """Carga las estadísticas de sesiones."""
        if os.path.exists(self.archivo):
            try:
                with open(self.archivo, 'r') as f:
                    self.sesiones_diarias = json.load(f)
            except Exception as e:
                print(f"Error al cargar estadísticas: {e}")
                self.sesiones_diarias = {}