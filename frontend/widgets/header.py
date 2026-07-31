import os
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.image import Image as KivyImage
from kivy.utils import get_color_from_hex
from kivy.metrics import dp, sp
from kivy.graphics import Color, Rectangle, Ellipse

_CWD = os.path.dirname(os.path.abspath(__file__))
_IMG = os.path.join(_CWD, "..", "assets")

C_DARK = get_color_from_hex("#033242")
C_LIGHT = get_color_from_hex("#033242")
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
            size=(dp(150), dp(150)),
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

        icon_size = dp(30)
        self._icon_menu = KivyImage(
            source=os.path.join(_IMG, "menu.png"),
            size_hint=(None, None),
            size=(icon_size, icon_size),
            allow_stretch=False,
            keep_ratio=True,
            fit_mode="contain",
        )
        self._icon_buscar = KivyImage(
            source=os.path.join(_IMG, "buscar.png"),
            size_hint=(None, None),
            size=(icon_size, icon_size),
            allow_stretch=False,
            keep_ratio=True,
            fit_mode="contain",
        )
        self._icon_campana = KivyImage(
            source=os.path.join(_IMG, "campana.png"),
            size_hint=(None, None),
            size=(icon_size, icon_size),
            allow_stretch=False,
            keep_ratio=True,
            fit_mode="contain",
        )

        for icon in [self._icon_menu, self._icon_buscar, self._icon_campana]:
            self.add_widget(icon)

        self._greeting = Label(
            text="¡Hola, Doctor(a)",
            font_size=sp(34),
            bold=True,
            color=C_WHITE,
            halign="left",
            valign="bottom",
            size_hint=(None, None),
            text_size=(None, None),
        )
        self._bang = Label(
            text="!",
            font_size=sp(34),
            bold=True,
            color=C_WHITE,
            halign="center",
            valign="bottom",
            size_hint=(None, None),
            text_size=(None, None),
        )
        self._measure = Label(
            text="¡Hola, Doctor(a)",
            font_size=sp(34),
            bold=True,
            size_hint=(None, None),
        )
        self._subtitle = Label(
            text="Herramientas clinicas basadas en\nevidencias para Otorrinolaringologia",
            font_size=sp(18),
            color=C_W70,
            halign="left",
            valign="top",
            text_size=(None, None),
        )

        for w in [self._img_left, self._img_right, self._greeting, self._bang, self._subtitle]:
            self.add_widget(w)

        self.bind(pos=self._layout, size=self._layout)
        self.bind(pos=self._draw, size=self._draw)

    def _layout(self, *a):
        x, y, w, h = self.x, self.y, self.width, self.height
        pad = dp(20)

        self._img_left.pos = (x + pad, y + h / 2 - dp(75))

        text_x = x + pad + dp(150) + dp(16)
        text_w = w - text_x - pad

        self._greeting.pos = (text_x, y + h - dp(130))
        self._greeting.size = (text_w, dp(50))
        self._greeting.text_size = (text_w, None)

        self._measure.texture_update()
        self._bang.texture_update()
        self._bang.pos = (text_x + self._measure.texture_size[0], y + h - dp(130))
        self._bang.size = (self._bang.texture_size[0] + dp(4), dp(50))

        self._subtitle.pos = (text_x, y + dp(72))
        self._subtitle.size = (text_w, dp(60))
        self._subtitle.text_size = (text_w, None)

        self._img_right.pos = (x + w - dp(150) - pad, y + h / 2 - dp(75))

        top_pad = dp(24)
        icon_size = dp(30)
        self._icon_menu.pos = (x + pad, y + h - top_pad - icon_size)
        self._icon_buscar.pos = (
            x + w - pad - icon_size * 2 - dp(12),
            y + h - top_pad - icon_size,
        )
        self._icon_campana.pos = (
            x + w - pad - icon_size,
            y + h - top_pad - icon_size,
        )

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
