from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.utils import get_color_from_hex
from kivy.metrics import dp, sp
from kivy.graphics import Color, Line, Rectangle

C_ACTIVE = get_color_from_hex("#14828A")
C_INACTIVE = get_color_from_hex("#9CA3AF")


class BottomNavigation(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint_y = None
        self.height = dp(64)
        self._active = 0

        self._items = [
            ("Inicio", "home"),
            ("Escalas", "scales"),
            ("Guias", "guides"),
            ("Calculadoras", "calculators"),
            ("Perfil", "profile"),
        ]

        self._labels = []
        for text, _ in self._items:
            lbl = Label(
                text=text,
                font_size=sp(9),
                color=C_INACTIVE,
                halign="center",
                valign="middle",
                text_size=(None, None),
            )
            self._labels.append(lbl)
            self.add_widget(lbl)

        self.bind(pos=self._draw, size=self._draw)
        self.bind(pos=self._layout, size=self._layout)

    def set_active(self, idx):
        self._active = idx
        self._draw()

    def _draw(self, *a):
        self.canvas.before.clear()
        x, y, w, h = self.x, self.y, self.width, self.height
        with self.canvas.before:
            Color(1, 1, 1, 1)
            Rectangle(pos=(x, y), size=(w, h))
            Color(0, 0, 0, 0.06)
            Rectangle(pos=(x, y + h - dp(0.5)), size=(w, dp(0.5)))

        item_w = w / len(self._items)
        for i in range(len(self._items)):
            cx = x + item_w * i + item_w / 2
            icon_y = y + h - dp(36)
            active = i == self._active
            c = C_ACTIVE if active else C_INACTIVE
            with self.canvas.before:
                Color(*c)
                self._draw_icon(cx, icon_y, i)
            if i < len(self._labels):
                self._labels[i].color = c
                self._labels[i].bold = active

    def _draw_icon(self, cx, cy, idx):
        if idx == 0:
            Line(points=[cx - dp(7), cy - dp(2), cx - dp(3), cy + dp(6), cx + dp(3), cy + dp(6), cx + dp(7), cy - dp(2), cx - dp(7), cy - dp(2)], width=dp(1.3))
            Line(points=[cx - dp(5), cy - dp(2), cx - dp(5), cy - dp(6)], width=dp(1.1))
            Line(points=[cx + dp(5), cy - dp(2), cx + dp(5), cy - dp(6)], width=dp(1.1))
        elif idx == 1:
            Line(rounded_rectangle=(cx - dp(8), cy - dp(7), dp(16), dp(14), dp(2)), width=dp(1.2))
            Line(points=[cx - dp(8), cy, cx + dp(8), cy], width=dp(0.8))
            Line(points=[cx, cy - dp(7), cx, cy + dp(7)], width=dp(0.8))
        elif idx == 2:
            Line(points=[cx - dp(6), cy + dp(6), cx - dp(6), cy - dp(6)], width=dp(1.3))
            Line(points=[cx - dp(6), cy + dp(6), cx + dp(2), cy + dp(6)], width=dp(1.3))
            Line(points=[cx - dp(6), cy + dp(2), cx + dp(6), cy + dp(2)], width=dp(1))
            Line(points=[cx - dp(6), cy - dp(2), cx + dp(4), cy - dp(2)], width=dp(1))
            Line(points=[cx - dp(6), cy - dp(6), cx + dp(2), cy - dp(6)], width=dp(1))
        elif idx == 3:
            Line(points=[cx - dp(5), cy + dp(6), cx - dp(8), cy, cx - dp(5), cy - dp(6), cx + dp(5), cy - dp(6), cx + dp(8), cy, cx + dp(5), cy + dp(6), cx - dp(5), cy + dp(6)], width=dp(1.3))
            Line(points=[cx - dp(2), cy - dp(2), cx + dp(2), cy + dp(2)], width=dp(1.1))
        elif idx == 4:
            Line(circle=(cx, cy + dp(3), dp(5)), width=dp(1.3))
            Line(points=[cx - dp(8), cy - dp(6), cx, cy - dp(1), cx + dp(8), cy - dp(6)], width=dp(1.3))

    def _layout(self, *a):
        item_w = self.width / len(self._items)
        for i, lbl in enumerate(self._labels):
            lbl.pos = (item_w * i, self.y + dp(4))
            lbl.text_size = (item_w, None)
