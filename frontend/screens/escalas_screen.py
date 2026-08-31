from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.metrics import dp, sp

from frontend.scales import SCALES, AREAS
from frontend.widgets.app_header import SimpleHeader
from frontend.widgets.bottom_nav import BottomNavigation
from frontend.widgets.scale_row import ScaleRow
from frontend.widgets.ui import content_column, scroll_with, section_title, empty_message


class EscalasScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.filtro = None
        root = BoxLayout(orientation="vertical")

        self._header = SimpleHeader("Escalas", back_target=None)
        root.add_widget(self._header)

        self._content = content_column()
        root.add_widget(scroll_with(self._content))

        self._nav = BottomNavigation()
        root.add_widget(self._nav)

        self.add_widget(root)

    def on_enter(self):
        self._nav.set_active(1)
        self._rebuild()

    def set_filtro(self, area):
        self.filtro = area
        if area in AREAS:
            self._header.set_title(AREAS[area]["titulo"])

    def _rebuild(self):
        self._content.clear_widgets()

        if self.filtro in AREAS:
            info = AREAS[self.filtro]
            selected = [s for s in SCALES if s["area"] == self.filtro]
            self._content.add_widget(section_title(info["titulo"]))
            from kivy.uix.label import Label
            from kivy.utils import get_color_from_hex
            sub = Label(
                text=info["desc"],
                font_size=sp(12),
                color=get_color_from_hex("#6B7280"),
                halign="left",
                size_hint_y=None,
                height=dp(20),
            )
            sub.bind(size=lambda s, sz: setattr(s, "text_size", (sz[0], None)))
            self._content.add_widget(sub)
        else:
            selected = list(SCALES)
            self._content.add_widget(section_title("Escalas disponibles"))

        if not selected:
            empty_message(self._content, "No hay escalas en esta area.")

        for s in selected:
            row = ScaleRow(s, show_star=True, on_toggle=self._rebuild)
            self._content.add_widget(row)