import os
from kivy.uix.widget import Widget
from kivy.uix.image import Image as KivyImage
from kivy.uix.label import Label
from kivy.utils import get_color_from_hex
from kivy.metrics import dp, sp
from kivy.graphics import Color, Rectangle

_CWD = os.path.dirname(os.path.abspath(__file__))
_IMG = os.path.join(_CWD, "..", "assets")

C_ACTIVE = get_color_from_hex("#14828A")
C_INACTIVE = get_color_from_hex("#9CA3AF")


class BottomNavigation(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint_y = None
        self.height = dp(72)
        self._active = 0

        self._items = [
            ("Inicio", "home", "casagris.png", "casazul.png"),
            ("Escalas", "escalas", "escalasgris.png", "escalasazul.png"),
            ("Guias", "guias", "guiasgris.png", "guiasazul.png"),
            ("Perfil", "perfil", "perfilgris.png", "perfilazul.png"),
        ]

        self._icons = []
        self._labels = []
        for text, _, gris, _azul in self._items:
            icon = KivyImage(
                source=os.path.join(_IMG, gris),
                size_hint=(None, None),
                size=(dp(28), dp(28)),
                allow_stretch=False,
                keep_ratio=True,
                fit_mode="contain",
            )
            self._icons.append(icon)
            self.add_widget(icon)

            lbl = Label(
                text=text,
                font_size=sp(12),
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

        for i, (text, target, gris, azul) in enumerate(self._items):
            active = i == self._active
            self._icons[i].source = os.path.join(_IMG, azul if active else gris)
            c = C_ACTIVE if active else C_INACTIVE
            self._labels[i].color = c
            self._labels[i].bold = active

    def _layout(self, *a):
        item_w = self.width / len(self._items)
        icon_h = dp(28)
        gap = dp(4)
        text_h = dp(20)
        block_h = icon_h + gap + text_h
        top_base = self.y + (self.height - block_h) / 2
        for i, (text, target, gris, azul) in enumerate(self._items):
            item_x = self.x + item_w * i
            cx = self.x + item_w * i + item_w / 2
            icon = self._icons[i]
            icon.center = (cx, top_base + block_h - icon_h / 2)
            self._labels[i].pos = (item_x, top_base)
            self._labels[i].size = (item_w, text_h)
            self._labels[i].text_size = (item_w, text_h)

    def on_touch_down(self, touch):
        if not self.collide_point(*touch.pos):
            return False
        item_w = self.width / len(self._items)
        idx = int((touch.x - self.x) // item_w)
        if 0 <= idx < len(self._items):
            _, target, _, _ = self._items[idx]
            self.set_active(idx)
            from kivy.app import App
            App.get_running_app().root.current = target
        return True
