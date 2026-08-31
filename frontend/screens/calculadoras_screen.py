from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout

from frontend.scales import escala_por_id
from frontend.widgets.app_header import SimpleHeader
from frontend.widgets.bottom_nav import BottomNavigation
from frontend.widgets.scale_row import ScaleRow
from frontend.widgets.ui import content_column, scroll_with, section_title

_ORDER = ["imc", "ess", "stop_bang", "snot22", "lund_mackay", "thi", "etdq7", "vhi10", "grbas"]


class CalculadorasScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        root = BoxLayout(orientation="vertical")

        root.add_widget(SimpleHeader("Calculadoras", back_target=None))

        self._content = content_column()
        root.add_widget(scroll_with(self._content))

        self._nav = BottomNavigation()
        root.add_widget(self._nav)

        self.add_widget(root)

    def on_enter(self):
        self._nav.set_active(3)
        self._rebuild()

    def _rebuild(self):
        self._content.clear_widgets()
        self._content.add_widget(section_title("Calculo rapido"))

        for escala_id in _ORDER:
            s = escala_por_id(escala_id)
            if s is not None:
                self._content.add_widget(ScaleRow(s, show_star=False))