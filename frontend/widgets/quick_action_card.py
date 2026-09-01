import os
from kivy.uix.behaviors.button import ButtonBehavior
from kivy.uix.label import Label
from kivy.uix.image import Image as KivyImage
from kivy.uix.widget import Widget
from kivy.utils import get_color_from_hex
from kivy.metrics import dp, sp
from kivy.graphics import Color, RoundedRectangle, Line, Ellipse

_CWD = os.path.dirname(os.path.abspath(__file__))
_IMG = os.path.join(_CWD, "..", "assets")


class QuickActionCard(ButtonBehavior, Widget):
    """Tarjeta de accion rapida: icono teal sobresaliendo por arriba, titulo y subtitulo debajo."""

    def __init__(self, source, title="", subtitle="", target=None, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (None, None)
        self.target = target

        self.icon_tint = get_color_from_hex("#14828A")
        self._radius = dp(18)
        self._disk_d = dp(58)
        self._disk_fill = get_color_from_hex("#E6F4F5")

        self._img = KivyImage(
            source=os.path.join(_IMG, source),
            size_hint=(None, None),
            size=(dp(42), dp(42)),
            allow_stretch=False,
            keep_ratio=True,
            fit_mode="contain",
            color=self.icon_tint,
        )

        self._title_lbl = Label(
            text=title,
            font_size=sp(16),
            bold=True,
            color=get_color_from_hex("#1F2937"),
            halign="center",
            valign="middle",
            size_hint=(None, None),
        )
        self._subtitle_lbl = Label(
            text=subtitle,
            font_size=sp(12),
            color=get_color_from_hex("#6B7280"),
            halign="center",
            valign="top",
            size_hint=(None, None),
        )

        self.add_widget(self._img)
        self.add_widget(self._title_lbl)
        self.add_widget(self._subtitle_lbl)

        self.bind(pos=self._layout, size=self._layout)

    def _layout(self, *a):
        if self.width < 1:
            return
        cx = self.center_x
        y = self.y
        h = self.height
        d = self._disk_d

        # Circulo con el icono: centrados horizontalmente y dentro de la tarjeta,
        # con un pequeno margen interno respecto al borde superior.
        top_margin = dp(16)
        disk_cy = y + h - top_margin - d / 2
        self._img.center = (cx, disk_cy)

        text_top = disk_cy - d / 2 - dp(8)
        self._title_lbl.size = (self.width, dp(24))
        self._title_lbl.text_size = (self.width, None)
        self._title_lbl.pos = (self.x, text_top - dp(24))

        self._subtitle_lbl.size = (self.width, dp(34))
        self._subtitle_lbl.text_size = (self.width, None)
        self._subtitle_lbl.pos = (self.x, text_top - dp(24) - dp(34))

        self._draw()

    def _draw(self, *a):
        self.canvas.before.clear()
        if self.width < 1 or self.height < 1:
            return
        cx = self.center_x
        y = self.y
        h = self.height
        d = self._disk_d
        top_margin = dp(16)
        disk_cy = y + h - top_margin - d / 2
        pressed = self.state == "down"
        with self.canvas.before:
            Color(0, 0, 0, 0.06)
            RoundedRectangle(
                pos=(self.x, self.y - dp(2)),
                size=self.size,
                radius=[self._radius],
            )
            if pressed:
                Color(0.95, 0.96, 0.97, 1)
            else:
                Color(1, 1, 1, 1)
            RoundedRectangle(pos=self.pos, size=self.size, radius=[self._radius])
            Color(0.85, 0.87, 0.90, 1)
            Line(
                rounded_rectangle=(self.x, self.y, self.width, self.height, self._radius),
                width=dp(1),
            )
            # Circulo con el icono, contenido dentro de la tarjeta.
            Color(*self._disk_fill)
            Ellipse(pos=(cx - d / 2, disk_cy - d / 2), size=(d, d))

    def on_state(self, *a):
        self._draw()

    def on_release(self):
        if not self.target:
            return
        from kivy.app import App
        app = App.get_running_app()
        if app is not None and app.root is not None:
            app.root.current = self.target
