from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.utils import get_color_from_hex
from kivy.metrics import dp, sp
from kivy.graphics import Color, RoundedRectangle, Line, Ellipse


class InfoBanner(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint_y = None
        self.height = dp(80)

        self._title_lbl = Label(
            text="Evidencia que guia tu practica",
            font_size=sp(13),
            bold=True,
            color=get_color_from_hex("#0D6E73"),
            halign="left",
            valign="middle",
            text_size=(None, None),
        )
        self._desc_lbl = Label(
            text="Todas las escalas estan validadas y basadas\nen guias internacionales.",
            font_size=sp(10),
            color=get_color_from_hex("#6B7280"),
            halign="left",
            valign="top",
            text_size=(None, None),
        )
        self.add_widget(self._title_lbl)
        self.add_widget(self._desc_lbl)
        self.bind(pos=self._draw, size=self._draw)
        self.bind(pos=self._layout, size=self._layout)

    def _draw(self, *a):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(*get_color_from_hex("#ECFAFC"))
            RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(16)])

            cx, cy = self.x + dp(32), self.y + self.height / 2
            Color(*get_color_from_hex("#14828A"))
            sw, sh = dp(16), dp(20)
            Line(
                points=[
                    cx - sw / 2, cy + sh / 2 - dp(2),
                    cx - sw / 2, cy - dp(2),
                    cx, cy - sh / 2,
                    cx + sw / 2, cy - dp(2),
                    cx + sw / 2, cy + sh / 2 - dp(2),
                    cx, cy + sh / 2 + dp(2),
                    cx - sw / 2, cy + sh / 2 - dp(2),
                ],
                width=dp(1.5),
            )
            Line(
                points=[
                    cx - dp(3), cy - dp(1),
                    cx - dp(1), cy + dp(1),
                    cx + dp(3), cy - dp(3),
                ],
                width=dp(1.3),
            )

            ax = self.x + self.width - dp(28)
            ay = self.y + self.height / 2
            Color(*get_color_from_hex("#14828A"))
            Line(points=[ax - dp(6), ay + dp(4), ax + dp(2), ay, ax - dp(6), ay - dp(4)], width=dp(1.6))

    def _layout(self, *a):
        tx = self.x + dp(56)
        tw = self.width - dp(90)
        self._title_lbl.pos = (tx, self.y + self.height - dp(44))
        self._title_lbl.text_size = (tw, None)
        self._desc_lbl.pos = (tx, self.y + dp(10))
        self._desc_lbl.text_size = (tw, None)
