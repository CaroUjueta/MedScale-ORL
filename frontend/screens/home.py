from kivy.uix.screenmanager import Screen
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label


class HomeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation="vertical", padding=20, spacing=10)
        layout.add_widget(
            Label(text="MedScale-ORL", font_size="24sp", bold=True)
        )
        layout.add_widget(
            Label(
                text="Seleccione una escala:",
                font_size="16sp",
            )
        )

        btn_vhi = Button(
            text="Escala VHI",
            size_hint=(1, 0.15),
            on_press=lambda _: setattr(self.manager, "current", "vhi"),
        )
        btn_snot = Button(
            text="Escala SNOT-22",
            size_hint=(1, 0.15),
            on_press=lambda _: setattr(self.manager, "current", "snot"),
        )

        layout.add_widget(btn_vhi)
        layout.add_widget(btn_snot)
        self.add_widget(layout)
