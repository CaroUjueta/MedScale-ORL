import math
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.utils import get_color_from_hex
from kivy.metrics import dp, sp
from kivy.graphics import Color, RoundedRectangle, Ellipse, Line


class AreaCard(Widget):
    def __init__(self, title, subtitle, chips, bg_color, icon_color, target=None, **kwargs):
        super().__init__(**kwargs)
        self.size_hint_y = None
        self.height = dp(140)
        self._bg = bg_color
        self._ic = icon_color
        self._target = target

        self._title_lbl = Label(
            text=title.upper(),
            font_size=sp(13),
            bold=True,
            color=get_color_from_hex("#1F2937"),
            halign="left",
            valign="middle",
            text_size=(None, None),
        )
        self.add_widget(self._title_lbl)

        self._subtitle_lbl = Label(
            text=subtitle,
            font_size=sp(11),
            color=get_color_from_hex("#6B7280"),
            halign="left",
            valign="top",
            text_size=(None, None),
        )
        self.add_widget(self._subtitle_lbl)

        self._chip_lbls = []
        for c in chips:
            lbl = Label(
                text=f"  {c}  ",
                font_size=sp(9),
                color=get_color_from_hex("#4B5563"),
                halign="center",
                valign="middle",
                size_hint=(None, None),
                size=(dp(62), dp(22)),
            )
            self._chip_lbls.append(lbl)
            self.add_widget(lbl)

        self._arrow = Button(
            text=">",
            size_hint=(None, None),
            size=(dp(36), dp(36)),
            background_normal="",
            background_color=get_color_from_hex("#FFFFFF"),
            color=get_color_from_hex("#6B7280"),
            font_size=sp(16),
            bold=True,
        )
        self.add_widget(self._arrow)
        if self._target:
            self._arrow.bind(on_press=lambda *a: self._go())

        self.bind(pos=self._draw, size=self._draw)
        self.bind(pos=self._layout, size=self._layout)

    def _go(self):
        from kivy.app import App
        App.get_running_app().root.current = self._target

    def _draw(self, *a):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(0, 0, 0, 0.05)
            RoundedRectangle(pos=(self.x + dp(1), self.y - dp(2)), size=self.size, radius=[dp(20)])
            Color(0, 0, 0, 0.03)
            RoundedRectangle(pos=(self.x + dp(2), self.y - dp(1)), size=self.size, radius=[dp(20)])
            Color(*self._bg)
            RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(20)])

            Color(*self._ic)
            cx = self.x + dp(56)
            cy = self.y + self.height / 2
            Ellipse(pos=(cx - dp(36), cy - dp(36)), size=(dp(72), dp(72)))

        self._draw_icon()

    def _draw_icon(self):
        pass

    def _layout(self, *a):
        x, y, w, h = self.x, self.y, self.width, self.height
        cx = x + dp(56)
        cy = y + h / 2

        tx = x + dp(100)
        tw = w - dp(156)

        self._title_lbl.pos = (tx, y + h - dp(58))
        self._title_lbl.text_size = (tw, None)
        self._title_lbl.halign = "left"

        self._subtitle_lbl.pos = (tx, y + h - dp(78))
        self._subtitle_lbl.text_size = (tw, None)
        self._subtitle_lbl.halign = "left"

        chip_x = tx
        chip_y = y + dp(14)
        for i, lbl in enumerate(self._chip_lbls):
            lbl.pos = (chip_x + i * dp(66), chip_y)

        self._arrow.pos = (x + w - dp(52), y + h / 2 - dp(18))


class ApneaCard(AreaCard):
    def __init__(self, **kwargs):
        super().__init__(
            title="Apnea Obstructiva del Sueno",
            subtitle="Evaluacion y tamizaje",
            chips=["ESS", "STOP-BANG", "IMC"],
            bg_color=get_color_from_hex("#EDF5FF"),
            icon_color=get_color_from_hex("#B3D9F7"),
            **kwargs,
        )

    def _draw_icon(self):
        cx = self.x + dp(56)
        cy = self.y + self.height / 2
        with self.canvas:
            Color(*get_color_from_hex("#4A90D9"))
            hy = cy + dp(6)
            Line(circle=(cx - dp(2), hy, dp(8)), width=dp(1.2))
            for s in [-1, 1]:
                Line(points=[cx - dp(2) + s * dp(4), hy - dp(8), cx - dp(2) + s * dp(5), hy - dp(16)], width=dp(1.2))

            Color(*get_color_from_hex("#4A90D9"))
            Line(
                points=[cx - dp(10), hy - dp(2), cx - dp(14), hy - dp(4), cx - dp(10), hy - dp(6)],
                width=dp(1),
            )

            for i, (zx, zy, zs) in enumerate([
                (cx + dp(12), cy + dp(10), dp(5)),
                (cx + dp(18), cy + dp(4), dp(4)),
                (cx + dp(22), cy - dp(2), dp(3)),
            ]):
                Line(points=[zx, zy + zs, zx + zs, zy + zs, zx + zs, zy, zx, zy], width=dp(1.1))


class RinosinusitisCard(AreaCard):
    def __init__(self, **kwargs):
        super().__init__(
            title="Rinosinusitis",
            subtitle="Sintomas y evaluacion",
            chips=["SNOT-22", "Lund Mackay"],
            bg_color=get_color_from_hex("#EEF9F1"),
            icon_color=get_color_from_hex("#A8E6CF"),
            **kwargs,
        )

    def _draw_icon(self):
        cx = self.x + dp(56)
        cy = self.y + self.height / 2
        with self.canvas:
            Color(*get_color_from_hex("#2ECC71"))
            ny = cy + dp(8)
            Line(
                points=[
                    cx - dp(6), ny, cx - dp(8), ny - dp(5),
                    cx - dp(4), ny - dp(12), cx, ny - dp(14),
                    cx + dp(4), ny - dp(12), cx + dp(8), ny - dp(5),
                    cx + dp(6), ny,
                ],
                width=dp(1.4),
            )
            for s in [-1, 1]:
                Line(points=[cx + s * dp(4), ny - dp(14), cx + s * dp(2), ny - dp(16)], width=dp(1))
            Color(*get_color_from_hex("#2ECC71"))
            Line(
                points=[cx - dp(10), ny - dp(1), cx - dp(12), ny + dp(2)],
                width=dp(0.8),
            )
            Line(
                points=[cx + dp(10), ny - dp(1), cx + dp(12), ny + dp(2)],
                width=dp(0.8),
            )


class OtologiaCard(AreaCard):
    def __init__(self, **kwargs):
        super().__init__(
            title="Otologia",
            subtitle="Audicion y funcion del oido",
            chips=["THI", "ETDQ-7"],
            bg_color=get_color_from_hex("#F3ECFF"),
            icon_color=get_color_from_hex("#D4B8F0"),
            **kwargs,
        )

    def _draw_icon(self):
        cx = self.x + dp(56)
        cy = self.y + self.height / 2
        with self.canvas:
            Color(*get_color_from_hex("#9B59B6"))
            Line(ellipse=(cx - dp(8), cy - dp(14), dp(16), dp(28)), width=dp(1.4))
            Color(*get_color_from_hex("#D4B8F0"))
            Line(ellipse=(cx - dp(4), cy - dp(8), dp(8), dp(16)), width=dp(1.1))
            Color(*get_color_from_hex("#9B59B6"))
            Line(points=[cx, cy - dp(4), cx - dp(2), cy - dp(10)], width=dp(1.1))
            Line(
                points=[cx - dp(8), cy - dp(4), cx - dp(12), cy - dp(2)],
                width=dp(0.9),
            )
            Line(
                points=[cx + dp(8), cy - dp(4), cx + dp(12), cy - dp(2)],
                width=dp(0.9),
            )
