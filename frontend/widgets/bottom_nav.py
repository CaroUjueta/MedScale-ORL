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
        self.height = dp(72)
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
                font_size=sp(13),
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
            icon_y = y + h - dp(44)
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
            Line(points=[cx - dp(13), cy - dp(4), cx - dp(6), cy + dp(11), cx + dp(6), cy + dp(11), cx + dp(13), cy - dp(4), cx - dp(13), cy - dp(4)], width=dp(1.8))
            Line(points=[cx - dp(9), cy - dp(4), cx - dp(9), cy - dp(11)], width=dp(1.6))
            Line(points=[cx + dp(9), cy - dp(4), cx + dp(9), cy - dp(11)], width=dp(1.6))
        elif idx == 1:
            Line(rounded_rectangle=(cx - dp(13), cy - dp(12), dp(26), dp(24), dp(3)), width=dp(1.8))
            Line(points=[cx - dp(13), cy, cx + dp(13), cy], width=dp(1.2))
            Line(points=[cx, cy - dp(12), cx, cy + dp(12)], width=dp(1.2))
        elif idx == 2:
            Line(points=[cx - dp(10), cy + dp(10), cx - dp(10), cy - dp(10)], width=dp(1.8))
            Line(points=[cx - dp(10), cy + dp(10), cx + dp(4), cy + dp(10)], width=dp(1.8))
            Line(points=[cx - dp(10), cy + dp(3), cx + dp(10), cy + dp(3)], width=dp(1.5))
            Line(points=[cx - dp(10), cy - dp(3), cx + dp(7), cy - dp(3)], width=dp(1.5))
            Line(points=[cx - dp(10), cy - dp(10), cx + dp(4), cy - dp(10)], width=dp(1.5))
        elif idx == 3:
            Line(points=[cx - dp(9), cy + dp(10), cx - dp(14), cy, cx - dp(9), cy - dp(10), cx + dp(9), cy - dp(10), cx + dp(14), cy, cx + dp(9), cy + dp(10), cx - dp(9), cy + dp(10)], width=dp(1.8))
            Line(points=[cx - dp(3), cy - dp(3), cx + dp(3), cy + dp(3)], width=dp(1.5))
        elif idx == 4:
            Line(circle=(cx, cy + dp(5), dp(9)), width=dp(1.8))
            Line(points=[cx - dp(14), cy - dp(11), cx, cy - dp(2), cx + dp(14), cy - dp(11)], width=dp(1.8))

    def _layout(self, *a):
        item_w = self.width / len(self._items)
        for i, lbl in enumerate(self._labels):
            lbl.pos = (item_w * i, self.y + dp(8))
            lbl.text_size = (item_w, None)

    def on_touch_down(self, touch):
        if not self.collide_point(*touch.pos):
            return False
        item_w = self.width / len(self._items)
        idx = int((touch.x - self.x) // item_w)
        if 0 <= idx < len(self._items):
            _, target = self._items[idx]
            self.set_active(idx)
            from kivy.app import App
            App.get_running_app().root.current = target
        return True
