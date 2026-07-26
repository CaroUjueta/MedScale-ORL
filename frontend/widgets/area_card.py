import os
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.image import Image as KivyImage
from kivy.uix.button import Button
from kivy.utils import get_color_from_hex
from kivy.metrics import dp, sp
from kivy.graphics import Color, RoundedRectangle, Line

_CWD = os.path.dirname(os.path.abspath(__file__))
_IMG = os.path.join(_CWD, "..", "assets")


class ChipBadge(Widget):
    def __init__(self, text, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (None, None)
        self.size = (dp(70), dp(28))
        self._lbl = Label(
            text=text,
            font_size=sp(9),
            color=get_color_from_hex("#2563EB"),
            halign="center",
            valign="middle",
            text_size=(None, None),
            pos=self.pos,
            size=self.size,
        )
        self.add_widget(self._lbl)
        self.bind(pos=self._draw, size=self._draw)
        self.bind(pos=lambda s, p: setattr(s._lbl, 'pos', p))

    def _draw(self, *a):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(1, 1, 1, 0.8)
            RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(14)])
            Color(0.85, 0.88, 0.95, 1)
            Line(rounded_rectangle=(self.x, self.y, self.width, self.height, dp(14)), width=dp(0.7))


class AreaCard(Widget):
    def __init__(self, title, subtitle, chips, bg_color, img_name, target=None, **kwargs):
        super().__init__(**kwargs)
        self.size_hint_y = None
        self.height = dp(140)
        self._bg = bg_color
        self._target = target

        self._img = KivyImage(
            source=os.path.join(_IMG, img_name),
            size_hint=(None, None),
            size=(dp(72), dp(72)),
            allow_stretch=True,
            keep_ratio=True,
            fit_mode="contain",
        )
        self.add_widget(self._img)

        self._title_lbl = Label(
            text=title.upper(),
            font_size=sp(13),
            bold=True,
            color=get_color_from_hex("#133E7C"),
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

        self._chips = []
        for c in chips:
            chip = ChipBadge(text=c)
            self._chips.append(chip)
            self.add_widget(chip)

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
            RoundedRectangle(pos=(self.x + dp(1), self.y - dp(2)), size=self.size, radius=[dp(22)])
            Color(0, 0, 0, 0.03)
            RoundedRectangle(pos=(self.x + dp(2), self.y - dp(1)), size=self.size, radius=[dp(22)])
            Color(*self._bg)
            RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(22)])

    def _layout(self, *a):
        x, y, w, h = self.x, self.y, self.width, self.height
        pad = dp(20)

        self._img.pos = (x + pad, y + h / 2 - dp(36))

        tx = x + dp(100)
        tw = w - dp(156)

        self._title_lbl.pos = (tx, y + h - dp(58))
        self._title_lbl.text_size = (tw, None)
        self._title_lbl.halign = "left"

        self._subtitle_lbl.pos = (tx, y + h - dp(76))
        self._subtitle_lbl.text_size = (tw, None)
        self._subtitle_lbl.halign = "left"

        chip_x = tx
        chip_y = y + dp(14)
        for i, chip in enumerate(self._chips):
            chip.pos = (chip_x + i * dp(74), chip_y)

        self._arrow.pos = (x + w - dp(52), y + h / 2 - dp(18))


class ApneaCard(AreaCard):
    def __init__(self, **kwargs):
        super().__init__(
            title="Apnea Obstructiva del Sueno",
            subtitle="Evaluacion y tamizaje",
            chips=["ESS", "STOP-BANG", "IMC"],
            bg_color=get_color_from_hex("#EDF5FF"),
            img_name="Apnea.png",
            **kwargs,
        )


class RinosinusitisCard(AreaCard):
    def __init__(self, **kwargs):
        super().__init__(
            title="Rinosinusitis",
            subtitle="Sintomas y evaluacion",
            chips=["SNOT-22", "Lund Mackay"],
            bg_color=get_color_from_hex("#EEF9F1"),
            img_name="Rinosinusitis.png",
            **kwargs,
        )


class OtologiaCard(AreaCard):
    def __init__(self, **kwargs):
        super().__init__(
            title="Otologia",
            subtitle="Audicion y funcion del oido",
            chips=["THI", "ETDQ-7"],
            bg_color=get_color_from_hex("#F3ECFF"),
            img_name="Otología.png",
            **kwargs,
        )
