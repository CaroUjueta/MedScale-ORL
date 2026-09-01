from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.utils import get_color_from_hex
from kivy.metrics import dp, sp

from frontend.scales import SCALES, AREAS, AREA_ORDEN
from frontend.widgets.app_header import SimpleHeader
from frontend.widgets.bottom_nav import BottomNavigation
from frontend.widgets.scale_row import ScaleRow
from frontend.widgets.ui import content_column, scroll_with, section_title


C_TEXT_SEC = get_color_from_hex("#6B7280")


class GuiasScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        root = BoxLayout(orientation="vertical")

        self._header = SimpleHeader("Guias rapidas", back_target=None)
        root.add_widget(self._header)

        self._content = content_column()
        root.add_widget(scroll_with(self._content))

        self._nav = BottomNavigation()
        root.add_widget(self._nav)

        self.add_widget(root)

    def on_enter(self):
        self._nav.set_active(2)
        self._rebuild()

    def _rebuild(self):
        self._content.clear_widgets()

        intro = Label(
            text="Guia rapida por area clinica. Toca una escala\npara abrirla y completar la evaluacion.",
            font_size=sp(12),
            color=C_TEXT_SEC,
            halign="center",
            valign="middle",
            size_hint_y=None,
            height=dp(52),
        )
        intro.bind(size=lambda s, sz: setattr(s, "text_size", (sz[0], None)))
        self._content.add_widget(intro)

        for area in AREA_ORDEN:
            info = AREAS[area]
            self._content.add_widget(section_title(info["titulo"]))

            desc = Label(
                text=info["desc"],
                font_size=sp(12),
                color=C_TEXT_SEC,
                halign="left",
                valign="middle",
                size_hint_y=None,
                height=dp(20),
            )
            desc.bind(size=lambda s, sz: setattr(s, "text_size", (sz[0], None)))
            self._content.add_widget(desc)

            for s in SCALES:
                if s["area"] == area:
                    self._content.add_widget(ScaleRow(s, show_star=False))