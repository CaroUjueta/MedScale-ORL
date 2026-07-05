from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label


class SnotScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation="vertical", padding=20, spacing=10)
        layout.add_widget(
            Label(text="Escala SNOT-22", font_size="20sp")
        )
        layout.add_widget(
            Label(
                text="Contenido de la escala SNOT-22",
                font_size="14sp",
            )
        )
        self.add_widget(layout)
