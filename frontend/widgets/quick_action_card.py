import math
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.utils import get_color_from_hex
from kivy.metrics import dp, sp
from kivy.graphics import Color, RoundedRectangle, Ellipse, Line


class QuickActionCard(Widget):
    def __init__(self, title, description, icon_type, **kwargs):
        super().__init__(**kwargs)
        self.size_hint_y = None
        self.height = dp(100)
        self._icon_type = icon_type

        self._title_lbl = Label(
            text=title,
            font_size=sp(12),
            bold=True,
            color=get_color_from_hex("#1F2937"),
            halign="center",
            valign="middle",
            text_size=(None, None),
        )
        self._desc_lbl = Label(
            text=description,
            font_size=sp(9),
            color=get_color_from_hex("#6B7280"),
            halign="center",
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
            Color(0, 0, 0, 0.04)
            RoundedRectangle(pos=(self.x + dp(1), self.y - dp(1)), size=self.size, radius=[dp(18)])
            Color(1, 1, 1, 1)
            RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(18)])
            Color(*get_color_from_hex("#F3F4F6"))
            Line(rounded_rectangle=(self.x, self.y, self.width, self.height, dp(18)), width=dp(0.7))

            cx = self.x + self.width / 2
            cy = self.y + self.height - dp(30)

            self._draw_icon(cx, cy)

    def _draw_icon(self, cx, cy):
        c = get_color_from_hex("#14828A")
        with self.canvas:
            Color(*c)
            if self._icon_type == "bookmark":
                Line(
                    points=[
                        cx - dp(6), cy + dp(8),
                        cx, cy + dp(4),
                        cx + dp(6), cy + dp(8),
                        cx + dp(6), cy - dp(8),
                        cx, cy - dp(4),
                        cx - dp(6), cy - dp(8),
                        cx - dp(6), cy + dp(8),
                    ],
                    width=dp(1.3),
                )
            elif self._icon_type == "history":
                Line(circle=(cx, cy, dp(9)), width=dp(1.3))
                Line(points=[cx, cy, cx, cy + dp(5)], width=dp(1.2))
                Line(points=[cx, cy, cx + dp(4), cy + dp(2)], width=dp(1.2))
            elif self._icon_type == "groups":
                Line(circle=(cx - dp(5), cy + dp(3), dp(4)), width=dp(1.2))
                Line(circle=(cx + dp(5), cy + dp(3), dp(4)), width=dp(1.2))
                Line(
                    points=[
                        cx - dp(9), cy - dp(6),
                        cx - dp(5), cy - dp(2),
                        cx + dp(5), cy - dp(2),
                        cx + dp(9), cy - dp(6),
                    ],
                    width=dp(1.2),
                )
                Line(points=[cx - dp(5), cy - dp(2), cx - dp(5), cy - dp(8)], width=dp(1.1))
                Line(points=[cx + dp(5), cy - dp(2), cx + dp(5), cy - dp(8)], width=dp(1.1))
            elif self._icon_type == "book":
                x0, y0 = cx - dp(8), cy - dp(7)
                w, h = dp(16), dp(14)
                Line(points=[x0 + dp(2), y0 + h, x0, y0, x0 + w, y0, x0 + w - dp(2), y0 + h], width=dp(1.3))
                Line(points=[x0 + dp(2), y0 + h, x0 + w - dp(2), y0 + h], width=dp(1))
                Line(points=[cx, y0, cx, y0 + h], width=dp(0.8))

    def _layout(self, *a):
        self._title_lbl.pos = (self.x, self.y + dp(30))
        self._title_lbl.text_size = (self.width - dp(8), None)
        self._desc_lbl.pos = (self.x + dp(4), self.y + dp(8))
        self._desc_lbl.text_size = (self.width - dp(8), None)
