import os
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.image import Image as KivyImage
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.utils import get_color_from_hex
from kivy.metrics import dp, sp
from kivy.graphics import Color, RoundedRectangle, Line

_CWD = os.path.dirname(os.path.abspath(__file__))
_IMG = os.path.join(_CWD, "..", "assets")


class ChipBadge(Widget):
    def __init__(self, text, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (None, None)
        self.size = (dp(110), dp(30))
        self._lbl = Label(
            text=text,
            font_size=sp(13),
            color=get_color_from_hex("#2563EB"),
            halign="center",
            valign="middle",
            pos=self.pos,
            size=self.size,
        )
        self.add_widget(self._lbl)
        self.bind(pos=self._draw, size=self._draw)
        self.bind(pos=lambda s, p: setattr(s._lbl, 'pos', p))
        self.bind(size=lambda s, sz: setattr(s._lbl, 'size', sz))

    def _draw(self, *a):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(1, 1, 1, 0.85)
            RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(15)])
            Color(0.82, 0.87, 0.96, 1)
            Line(rounded_rectangle=(self.x, self.y, self.width, self.height, dp(15)), width=dp(0.8))


class AreaCard(BoxLayout):
    def __init__(self, title, subtitle, chips, bg_color, img_name, target=None, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "horizontal"
        self.size_hint_y = None
        self.height = dp(116)
        self.padding = [dp(14), dp(14), dp(14), dp(14)]
        self._bg_color = bg_color
        self._target = target

        self._img = KivyImage(
            source=os.path.join(_IMG, img_name),
            size_hint=(None, None),
            size=(dp(86), dp(86)),
            allow_stretch=False,
            keep_ratio=True,
            fit_mode="contain",
        )
        self.add_widget(self._img)

        self.add_widget(Widget(size_hint_x=None, width=dp(10)))

        col = BoxLayout(
            orientation="vertical",
            size_hint_x=1,
            spacing=dp(2),
        )

        self._title_lbl = Label(
            text=title.upper(),
            font_size=sp(18),
            bold=True,
            color=get_color_from_hex("#133E7C"),
            halign="left",
            valign="middle",
            size_hint_y=None,
            height=dp(24),
        )
        self._title_lbl.bind(size=self._set_text_size)
        col.add_widget(self._title_lbl)

        self._subtitle_lbl = Label(
            text=subtitle,
            font_size=sp(14),
            color=get_color_from_hex("#6B7280"),
            halign="left",
            valign="top",
            size_hint_y=None,
            height=dp(20),
        )
        self._subtitle_lbl.bind(size=self._set_text_size)
        col.add_widget(self._subtitle_lbl)

        chips_row = BoxLayout(
            orientation="horizontal",
            size_hint_y=None,
            height=dp(30),
            spacing=dp(6),
        )
        for c in chips:
            chips_row.add_widget(ChipBadge(text=c))
        col.add_widget(chips_row)

        self.add_widget(col)

        self.add_widget(Widget(size_hint_x=None, width=dp(8)))

        self._arrow = Button(
            text=">",
            size_hint=(None, None),
            size=(dp(38), dp(38)),
            background_normal="",
            background_color=get_color_from_hex("#FFFFFF"),
            color=get_color_from_hex("#6B7280"),
            font_size=sp(18),
            bold=True,
        )
        self.add_widget(self._arrow)
        if self._target:
            self._arrow.bind(on_press=lambda *a: self._go())

        self.bind(pos=self._draw, size=self._draw)

    def _go(self):
        from kivy.app import App
        App.get_running_app().root.current = self._target

    @staticmethod
    def _set_text_size(label, size):
        label.text_size = (size[0], None)

    def _draw(self, *a):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(0, 0, 0, 0.06)
            RoundedRectangle(pos=(self.x + dp(2), self.y - dp(3)), size=self.size, radius=[dp(22)])
            Color(0, 0, 0, 0.03)
            RoundedRectangle(pos=(self.x + dp(1), self.y - dp(1)), size=self.size, radius=[dp(22)])
            Color(*self._bg_color)
            RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(22)])


class ApneaCard(AreaCard):
    def __init__(self, **kwargs):
        super().__init__(
            title="Apnea Obstructiva del Sueño",
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
