from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.clock import Clock
from kivy.core.audio import SoundLoader
from kivy.uix.image import Image
from kivy.resources import resource_find
from datetime import datetime
from graph_utils import generar_grafico
import os
import sys
import json

def resource_path(relative_path):
    """Obtiene la ruta absoluta del recurso, compatible con PyInstaller."""
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

class PantallaPrincipal(Screen):
    def __init__(self, **kwargs):
        super(PantallaPrincipal, self).__init__(**kwargs)
        self.contenedor = BoxLayout(orientation='vertical', spacing=10, padding=20)

        # Entradas de tiempo
        self.entrada_pomodoro = TextInput(text='40', multiline=False, hint_text='Minutos Pomodoro', size_hint=(1, 0.03))
        self.entrada_descanso = TextInput(text='5', multiline=False, hint_text='Minutos Descanso', size_hint=(1, 0.03))
        self.contenedor.add_widget(self.entrada_pomodoro)
        self.contenedor.add_widget(self.entrada_descanso)

        # Etiqueta del temporizador
        self.etiqueta_tiempo = Label(text="00:00", font_size=52, size_hint=(1, 0.2))
        self.contenedor.add_widget(self.etiqueta_tiempo)

        # Botón para iniciar o pausar
        self.boton_toggle = Button(text="Iniciar", size_hint=(1, 0.03))
        self.boton_toggle.bind(on_press=self.iniciar_o_pausar)
        self.contenedor.add_widget(self.boton_toggle)

        # Botón para cambiar de modo
        self.boton_modo = Button(text="Modo: Pomodoro", size_hint=(1, 0.03))
        self.boton_modo.bind(on_press=self.cambiar_modo)
        self.contenedor.add_widget(self.boton_modo)

        # Botón para ver gráfico
        self.boton_grafico = Button(text="Ver Gráfico Semanal", size_hint=(1, 0.03))
        self.boton_grafico.bind(on_press=self.mostrar_grafico)
        self.contenedor.add_widget(self.boton_grafico)

        self.add_widget(self.contenedor)

        # Variables internas
        self.temporizador_activo = False
        self.segundos_restantes = 0
        self.evento_reloj = None
        self.modo_actual = 'pomodoro'

        self.archivo_sesiones = 'sesiones.json'
        self.sesiones_diarias = self.cargar_sesiones()

        # Cargar el sonido de la alarma
        ruta_sonido = resource_path('alarma.mp3')
        self.alarma = SoundLoader.load(resource_find('alarma.mp3'))

    def cargar_sesiones(self):
        if os.path.exists(self.archivo_sesiones):
            with open(self.archivo_sesiones, 'r') as f:
                return json.load(f)
        return {}

    def guardar_sesiones(self):
        with open(self.archivo_sesiones, 'w') as f:
            json.dump(self.sesiones_diarias, f)

    def cambiar_modo(self, instancia):
        if self.modo_actual == 'pomodoro':
            self.modo_actual = 'descanso'
            self.boton_modo.text = 'Modo: Descanso'
        else:
            self.modo_actual = 'pomodoro'
            self.boton_modo.text = 'Modo: Pomodoro'

    def iniciar_o_pausar(self, instancia):
        if not self.temporizador_activo:
            try:
                minutos = int(self.entrada_pomodoro.text if self.modo_actual == 'pomodoro' else self.entrada_descanso.text)
                self.segundos_restantes = minutos * 60
            except ValueError:
                self.etiqueta_tiempo.text = "Entrada inválida"
                return
            self.temporizador_activo = True
            self.boton_toggle.text = "Pausar"
            self.evento_reloj = Clock.schedule_interval(self.actualizar_tiempo, 1)
        else:
            self.temporizador_activo = False
            self.boton_toggle.text = "Reanudar"
            if self.evento_reloj:
                self.evento_reloj.cancel()

    def actualizar_tiempo(self, dt):
        if self.segundos_restantes > 0:
            self.segundos_restantes -= 1
            minutos, segundos = divmod(self.segundos_restantes, 60)
            self.etiqueta_tiempo.text = f"{minutos:02d}:{segundos:02d}"
        else:
            self.etiqueta_tiempo.text = "¡Tiempo terminado!"
            self.boton_toggle.text = "Iniciar"
            self.temporizador_activo = False
            if self.evento_reloj:
                self.evento_reloj.cancel()

            # Reproducir sonido cuando el tiempo termine
            if self.alarma:
                self.alarma.play()

            # Si terminó un pomodoro, registrar sesión
            if self.modo_actual == 'pomodoro':
                hoy = datetime.now().strftime('%Y-%m-%d')
                self.sesiones_diarias[hoy] = self.sesiones_diarias.get(hoy, 0) + 1
                self.guardar_sesiones()

    def mostrar_grafico(self, instancia):
        generar_grafico(self.sesiones_diarias)
        self.manager.current = 'grafico'


class PantallaGrafico(Screen):
    def __init__(self, **kwargs):
        super(PantallaGrafico, self).__init__(**kwargs)
        contenedor = BoxLayout(orientation='vertical', spacing=10, padding=20)

        if os.path.exists('grafico_semanal.png'):
            self.imagen = Image(source='grafico_semanal.png', size_hint=(1, 0.9))
        else:
            self.imagen = Label(text="No se encontró el gráfico.", size_hint=(1, 0.9))

        contenedor.add_widget(self.imagen)

        boton_volver = Button(text="Volver", size_hint=(1, 0.1))
        boton_volver.bind(on_press=self.volver)
        contenedor.add_widget(boton_volver)

        self.add_widget(contenedor)

    def volver(self, instancia):
        self.manager.current = 'principal'


class AplicacionPomodoro(App):
    def build(self):
        gestor = ScreenManager()
        gestor.add_widget(PantallaPrincipal(name='principal'))
        gestor.add_widget(PantallaGrafico(name='grafico'))
        return gestor


if __name__ == '__main__':
    AplicacionPomodoro().run()