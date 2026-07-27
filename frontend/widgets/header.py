import os
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.image import Image as KivyImage
from kivy.utils import get_color_from_hex
from kivy.metrics import dp, sp
from kivy.graphics import Color, RoundedRectangle, Rectangle, Ellipse, Line

_CWD = os.path.dirname(os.path.abspath(__file__))
_IMG = os.path.join(_CWD, "..", "assets")

C_DARK = get_color_from_hex("#0A4C5A")
C_LIGHT = get_color_from_hex("#146A73")
C_WHITE = get_color_from_hex("#FFFFFF")
C_W70 = (1, 1, 1, 0.7)
C_W10 = (1, 1, 1, 0.1)


class _HamburgerIcon(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (None, None)
        self.size = (dp(44), dp(44))
        self.bind(pos=self._draw, size=self._draw)

    def _draw(self, *a):
        self.canvas.before.clear()
        cx, cy = self.center_x, self.center_y
        with self.canvas.before:
            Color(*C_W10)
            Ellipse(pos=(self.x, self.y), size=self.size)
            Color(*C_WHITE)
            for i in range(3):
                y = cy + dp(6) - i * dp(6)
                Rectangle(pos=(cx - dp(10), y - dp(1.2)), size=(dp(20), dp(2.4)))


class _TopIconButton(Widget):
    def __init__(self, icon_type, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (None, None)
        self.size = (dp(40), dp(40))
        self._type = icon_type
        self.bind(pos=self._draw, size=self._draw)

    def _draw(self, *a):
        self.canvas.before.clear()
        cx, cy = self.center_x, self.center_y
        with self.canvas.before:
            Color(*C_W10)
            Ellipse(pos=(self.x, self.y), size=self.size)
            Color(*C_WHITE)
            if self._type == "search":
                r = dp(8)
                Line(circle=(cx - dp(1), cy + dp(1), r), width=dp(1.8))
                Line(points=[cx - dp(1) + r * 0.7, cy + dp(1) - r * 0.7, cx + dp(6), cy - dp(6)], width=dp(1.8))
            elif self._type == "notif":
                w, h = dp(16), dp(14)
                Line(rounded_rectangle=(cx - w / 2, cy - h / 2 + dp(2), w, h, dp(3)), width=dp(1.6))
                Line(circle=(cx, cy - h / 2 + dp(5), dp(1.8)), width=dp(1.4))
                Line(points=[cx, cy - h / 2 + dp(3), cx, cy - h / 2 + dp(0.5)], width=dp(1.4))


class HomeHeader(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint_y = None
        self.height = dp(220)

        self._hamburger = _HamburgerIcon()
        self._search = _TopIconButton("search")
        self._notif = _TopIconButton("notif")

        self._img_left = KivyImage(
            source=os.path.join(_IMG, "Inicio.png"),
            size_hint=(None, None),
            size=(dp(72), dp(72)),
            allow_stretch=True,
            keep_ratio=True,
            fit_mode="contain",
        )
        self._img_right = KivyImage(
            source=os.path.join(_IMG, "Instrumentos.png"),
            size_hint=(None, None),
            size=(dp(90), dp(90)),
            allow_stretch=True,
            keep_ratio=True,
            fit_mode="contain",
        )

        self._greeting = Label(
            text="Hola, Doctor(a)!",
            font_size=sp(28),
            bold=True,
            color=C_WHITE,
            halign="center",
            valign="bottom",
            text_size=(None, None),
        )
        self._subtitle = Label(
            text="Herramientas clinicas basadas en\nevidencia para Otorrinolaringologia",
            font_size=sp(14),
            color=C_W70,
            halign="center",
            valign="top",
            text_size=(None, None),
        )

        for w in [self._hamburger, self._search, self._notif,
                  self._img_left, self._img_right,
                  self._greeting, self._subtitle]:
            self.add_widget(w)

        self.bind(pos=self._layout, size=self._layout)

    def _layout(self, *a):
        x, y, w, h = self.x, self.y, self.width, self.height
        pad = dp(20)

        self._hamburger.pos = (x + pad, y + h - pad - dp(44))
        self._search.pos = (x + w - pad - dp(40) - dp(44), y + h - pad - dp(40))
        self._notif.pos = (x + w - pad - dp(40), y + h - pad - dp(40))

        col_w = (w - pad * 2) / 3

        self._img_left.pos = (x + pad, y + h / 2 - dp(36))

        center_x = x + col_w + col_w / 2
        self._greeting.pos = (center_x - col_w / 2, y + h - dp(110))
        self._greeting.text_size = (col_w - dp(16), None)

        self._subtitle.pos = (center_x - col_w / 2, y + dp(36))
        self._subtitle.text_size = (col_w - dp(16), None)

        self._img_right.pos = (x + w - dp(90) - pad, y + h / 2 - dp(45))

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
