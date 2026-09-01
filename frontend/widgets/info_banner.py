import os

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.utils import get_color_from_hex
from kivy.metrics import dp, sp
from kivy.graphics import Color, RoundedRectangle

_CWD = os.path.dirname(os.path.abspath(__file__))
_IMG = os.path.join(_CWD, "..", "assets")


class EvidenceBanner(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "horizontal"
        self.size_hint_y = None
        self.height = dp(110)
        self.padding = [dp(20), dp(16), dp(20), dp(16)]
        self.spacing = dp(16)

        self.add_widget(Image(
            source=os.path.join(_IMG, "evidencia.png"),
            size_hint=(None, None),
            size=(dp(52), dp(52)),
            allow_stretch=False,
            keep_ratio=True,
            fit_mode="contain",
        ))

        col = BoxLayout(
            orientation="vertical",
            size_hint_x=1,
            spacing=dp(4),
        )

        self._title_lbl = Label(
            text="Evidencia que guia tu practica",
            font_size=sp(18),
            bold=True,
            color=get_color_from_hex("#0D6E73"),
            halign="left",
            valign="middle",
            size_hint_y=None,
            height=dp(26),
        )
        col.add_widget(self._title_lbl)

        self._desc_lbl = Label(
            text="Todas las escalas estan validadas y basadas\nen guias internacionales.",
            font_size=sp(15),
            color=get_color_from_hex("#6B7280"),
            halign="left",
            valign="top",
            size_hint_y=None,
            height=dp(40),
        )
        col.add_widget(self._desc_lbl)

        self.add_widget(col)

        arrow_lbl = Label(
            text=">",
            font_size=sp(20),
            bold=True,
            color=get_color_from_hex("#14828A"),
            size_hint=(None, None),
            size=(dp(30), dp(30)),
            halign="center",
            valign="middle",
        )
        self.add_widget(arrow_lbl)

        self.bind(pos=self._draw, size=self._draw)

    def _draw(self, *a):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(*get_color_from_hex("#ECFAFC"))
            RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(18)])
