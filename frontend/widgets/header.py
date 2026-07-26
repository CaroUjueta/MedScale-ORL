import math
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.utils import get_color_from_hex
from kivy.metrics import dp, sp
from kivy.graphics import Color, RoundedRectangle, Rectangle, Ellipse, Line

C_DARK = get_color_from_hex("#0A4C5A")
C_LIGHT = get_color_from_hex("#146A73")
C_ILLUST = get_color_from_hex("#78D5D7")
C_TURQ = get_color_from_hex("#14828A")
C_WHITE = get_color_from_hex("#FFFFFF")
C_W70 = (1, 1, 1, 0.7)
C_W40 = (1, 1, 1, 0.4)
C_W20 = (1, 1, 1, 0.2)
C_W10 = (1, 1, 1, 0.1)
C_W05 = (1, 1, 1, 0.05)


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
                Rectangle(pos=(cx - dp(9), y - dp(1)), size=(dp(18), dp(2)))


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
                r = dp(7)
                Line(circle=(cx - dp(1), cy + dp(1), r), width=dp(1.5))
                Line(points=[cx - dp(1) + r * 0.7, cy + dp(1) - r * 0.7, cx + dp(5), cy - dp(5)], width=dp(1.5))
            elif self._type == "notif":
                w, h = dp(14), dp(12)
                Line(rounded_rectangle=(cx - w / 2, cy - h / 2 + dp(2), w, h, dp(3)), width=dp(1.4))
                Line(circle=(cx, cy - h / 2 + dp(4), dp(1.5)), width=dp(1.2))
                Line(points=[cx, cy - h / 2 + dp(2.5), cx, cy - h / 2 + dp(0.5)], width=dp(1.2))


class _HeadProfileIcon(Widget):
    """Head/neck profile outline highlighting ear, nose, throat in #78D5D7."""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (None, None)
        self.size = (dp(80), dp(110))
        self.bind(pos=self._draw, size=self._draw)

    def _draw(self, *a):
        self.canvas.before.clear()
        cx, cy = self.center_x, self.center_y
        with self.canvas.before:
            Color(*C_ILLUST)
            head_r = dp(22)
            head_cy = cy + dp(24)

            Line(circle=(cx - dp(2), head_cy, head_r), width=dp(1.4))

            Line(
                points=[
                    cx - dp(2) - head_r, head_cy,
                    cx - dp(2) - head_r - dp(3), head_cy - dp(4),
                    cx - dp(2) - head_r - dp(2), head_cy - dp(10),
                ],
                width=dp(1.2),
            )

            nose_x = cx - dp(2) - head_r + dp(4)
            nose_y = head_cy - dp(8)
            Line(
                points=[
                    cx - dp(2) - head_r + dp(2), head_cy - dp(6),
                    nose_x - dp(6), nose_y,
                    nose_x - dp(4), nose_y - dp(6),
                    nose_x, nose_y - dp(4),
                ],
                width=dp(1.3),
            )

            mouth_x = cx - dp(2) - head_r + dp(6)
            mouth_y = head_cy - dp(16)
            Line(
                points=[mouth_x - dp(4), mouth_y, mouth_x + dp(2), mouth_y - dp(1)],
                width=dp(1.1),
            )

            neck_top = head_cy - head_r
            for s in [-1, 1]:
                Line(
                    points=[
                        cx - dp(2) + s * dp(6), neck_top,
                        cx - dp(2) + s * dp(7), neck_top - dp(18),
                        cx - dp(2) + s * dp(12), neck_top - dp(24),
                    ],
                    width=dp(1.3),
                )

            ear_x = cx - dp(2) + head_r + dp(3)
            ear_y = head_cy
            Line(ellipse=(ear_x - dp(3), ear_y - dp(7), dp(6), dp(14)), width=dp(1.2))

            Color(*C_W20)
            throat_cx = cx - dp(2)
            throat_cy = neck_top - dp(10)
            Line(circle=(throat_cx, throat_cy, dp(4)), width=dp(1))


class _OrlInstrumentsCircle(Widget):
    """90dp circular illustration with ORL instruments on turquoise bg."""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (None, None)
        self.size = (dp(90), dp(90))
        self.bind(pos=self._draw, size=self._draw)

    def _draw(self, *a):
        self.canvas.before.clear()
        cx, cy = self.center_x, self.center_y
        r = dp(40)
        with self.canvas.before:
            Color(0.08, 0.51, 0.54, 0.15)
            Ellipse(pos=(cx - r - dp(5), cy - r - dp(5)), size=(2 * r + dp(10), 2 * r + dp(10)))
            Color(0.08, 0.51, 0.54, 0.1)
            Ellipse(pos=(cx - r - dp(2), cy - r - dp(2)), size=(2 * r + dp(4), 2 * r + dp(4)))
            Color(*C_TURQ)
            Ellipse(pos=(cx - r - dp(1), cy - r - dp(1)), size=(2 * r + dp(2), 2 * r + dp(2)))
            Color(*C_W40)
            Line(circle=(cx, cy, r), width=dp(1.2))

            Color(*C_WHITE)
            ox, oy = cx - dp(14), cy + dp(10)
            Line(points=[ox, oy + dp(10), ox, oy, ox + dp(4), oy - dp(3)], width=dp(1.5))
            Line(circle=(ox, oy + dp(12), dp(3)), width=dp(1.2))

            Color(*C_W70)
            mx, my = cx + dp(8), cy + dp(8)
            Line(circle=(mx, my, dp(5)), width=dp(1.2))
            Line(points=[mx, my - dp(5), mx, my - dp(10)], width=dp(1.2))
            Line(points=[mx - dp(3), my - dp(10), mx + dp(3), my - dp(10)], width=dp(1))
            Color(*C_WHITE)
            Line(points=[mx - dp(1), my + dp(2), mx + dp(1), my + dp(2)], width=dp(0.8))

            Color(*C_W40)
            sx, sy = cx - dp(2), cy - dp(14)
            Line(points=[sx - dp(6), sy + dp(4), sx, sy, sx + dp(6), sy + dp(4)], width=dp(1.3))
            Line(points=[sx, sy, sx, sy + dp(8)], width=dp(1.1))
            Line(circle=(sx, sy + dp(10), dp(2.5)), width=dp(1))


class MedScaleHeader(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint_y = None
        self.height = dp(280)

        self._hamburger = _HamburgerIcon()
        self._search = _TopIconButton("search")
        self._notif = _TopIconButton("notif")
        self._head_icon = _HeadProfileIcon()
        self._orl_circle = _OrlInstrumentsCircle()

        self._greeting = Label(
            text="Hola, Doctor(a)!",
            font_size=sp(26),
            bold=True,
            color=C_WHITE,
            halign="center",
            valign="bottom",
            text_size=(None, None),
        )
        self._subtitle = Label(
            text="Herramientas clinicas basadas en\nevidencia para Otorrinolaringologia",
            font_size=sp(13),
            color=C_W70,
            halign="center",
            valign="top",
            text_size=(None, None),
        )

        for w in [self._hamburger, self._search, self._notif,
                  self._head_icon, self._orl_circle,
                  self._greeting, self._subtitle]:
            self.add_widget(w)

        self.bind(pos=self._layout, size=self._layout)

    def _layout(self, *a):
        x, y, w, h = self.x, self.y, self.width, self.height
        pad = dp(16)

        self._hamburger.pos = (x + pad, y + h - pad - dp(44))
        self._search.pos = (x + w - pad - dp(40) - dp(44), y + h - pad - dp(40))
        self._notif.pos = (x + w - pad - dp(40), y + h - pad - dp(40))

        col_w = (w - pad * 2) / 3

        self._head_icon.pos = (x + pad + dp(2), y + dp(20))

        center_x = x + col_w + col_w / 2
        self._greeting.pos = (center_x - col_w / 2, y + h - dp(130))
        self._greeting.text_size = (col_w - dp(16), None)

        self._subtitle.pos = (center_x - col_w / 2, y + dp(40))
        self._subtitle.text_size = (col_w - dp(16), None)

        self._orl_circle.pos = (x + w - dp(90) - pad, y + dp(24))

    def _draw(self, *a):
        self.canvas.before.clear()
        x, y, w, h = self.x, self.y, self.width, self.height
        radius = dp(24)
        with self.canvas.before:
            steps = 50
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
