import os
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.image import Image as KivyImage
from kivy.utils import get_color_from_hex
from kivy.metrics import dp, sp
from kivy.graphics import Color, Rectangle, Ellipse

_CWD = os.path.dirname(os.path.abspath(__file__))
_IMG = os.path.join(_CWD, "..", "assets")

C_DARK = get_color_from_hex("#0A4C5A")
C_LIGHT = get_color_from_hex("#146A73")
C_WHITE = get_color_from_hex("#FFFFFF")
C_W70 = (1, 1, 1, 0.7)


class HomeHeader(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint_y = None
        self.height = dp(260)

        self._img_left = KivyImage(
            source=os.path.join(_IMG, "Inicio.png"),
            size_hint=(None, None),
            size=(dp(130), dp(130)),
            allow_stretch=False,
            keep_ratio=True,
            fit_mode="contain",
        )
        self._img_right = KivyImage(
            source=os.path.join(_IMG, "Instrumentos.png"),
            size_hint=(None, None),
            size=(dp(150), dp(150)),
            allow_stretch=False,
            keep_ratio=True,
            fit_mode="contain",
        )

        self._greeting = Label(
            text="Hola, Doctor(a)!",
            font_size=sp(34),
            bold=True,
            color=C_WHITE,
            halign="center",
            valign="bottom",
            text_size=(None, None),
        )
        self._subtitle = Label(
            text="Herramientas clinicas basadas en\nevidencia para Otorrinolaringologia",
            font_size=sp(18),
            color=C_W70,
            halign="center",
            valign="top",
            text_size=(None, None),
        )

        for w in [self._img_left, self._img_right, self._greeting, self._subtitle]:
            self.add_widget(w)

        self.bind(pos=self._layout, size=self._layout)
        self.bind(pos=self._draw, size=self._draw)

    def _layout(self, *a):
        x, y, w, h = self.x, self.y, self.width, self.height
        pad = dp(20)

        col_w = (w - pad * 2) / 3

        self._img_left.pos = (x + pad, y + h / 2 - dp(65))

        center_x = x + col_w + col_w / 2
        self._greeting.pos = (center_x - col_w / 2, y + h - dp(130))
        self._greeting.text_size = (col_w - dp(16), None)

        self._subtitle.pos = (center_x - col_w / 2, y + dp(40))
        self._subtitle.text_size = (col_w - dp(16), None)

        self._img_right.pos = (x + w - dp(150) - pad, y + h / 2 - dp(75))

    def _draw(self, *a):
        self.canvas.before.clear()
        x, y, w, h = self.x, self.y, self.width, self.height
        radius = dp(30)
        with self.canvas.before:
            steps = 60
            for i in range(steps):
                t = i / steps
                r = C_DARK[0] + (C_LIGHT[0] - C_DARK[0]) * t
                g = C_DARK[1] + (C_LIGHT[1] - C_DARK[1]) * t
                b = C_DARK[2] + (C_LIGHT[2] - C_DARK[2]) * t
                strip_h = (h - radius) / steps + 1
                strip_y = y + radius + (h - radius) * (1 - t) - strip_h
                Color(r, g, b, 1)
                Rectangle(pos=(x, strip_y), size=(w, strip_h))

            Color(*C_LIGHT)
            Rectangle(pos=(x, y), size=(w, radius + dp(2)))

            Color(*C_DARK)
            Ellipse(pos=(x, y + h - radius - dp(1)), size=(radius * 2, radius * 2))
            Ellipse(pos=(x + w - radius * 2, y + h - radius - dp(1)), size=(radius * 2, radius * 2))
            Rectangle(pos=(x + radius, y + h - radius - dp(1)), size=(w - radius * 2, radius + dp(2)))

            Color(*C_LIGHT)
            Ellipse(pos=(x, y + h - radius - dp(1)), size=(radius * 2, radius * 2 - dp(6)))
            Ellipse(pos=(x + w - radius * 2, y + h - radius - dp(1)), size=(radius * 2, radius * 2 - dp(6)))
            Rectangle(pos=(x + radius, y + h - radius + dp(3)), size=(w - radius * 2, radius - dp(2)))
