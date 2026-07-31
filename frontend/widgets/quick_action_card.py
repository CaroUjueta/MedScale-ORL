import os
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image as KivyImage
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.utils import get_color_from_hex
from kivy.metrics import dp, sp
from kivy.graphics import Color, RoundedRectangle, Line

_CWD = os.path.dirname(os.path.abspath(__file__))
_IMG = os.path.join(_CWD, "..", "assets")


class QuickActionCard(BoxLayout):
    def __init__(self, title, description, icon=None, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"
        self.size_hint_y = None
        self.padding = [dp(18), dp(20), dp(18), dp(18)]
        self.spacing = 0

        if icon:
            anchor = AnchorLayout(size_hint_y=None, height=dp(52))
            anchor.add_widget(
                KivyImage(
                    source=os.path.join(_IMG, icon),
                    size_hint=(None, None),
                    size=(dp(52), dp(52)),
                    allow_stretch=False,
                    keep_ratio=True,
                    fit_mode="contain",
                )
            )
            self.add_widget(anchor)
            self.add_widget(Widget(size_hint_y=None, height=dp(14)))
        else:
            self.add_widget(Widget(size_hint_y=None, height=dp(50)))

        self._title_lbl = Label(
            text=title,
            font_size=sp(18),
            bold=True,
            color=get_color_from_hex("#1F2937"),
            halign="center",
            valign="middle",
            size_hint_y=None,
            height=dp(24),
        )
        self.add_widget(self._title_lbl)

        self.add_widget(Widget(size_hint_y=None, height=dp(6)))

        self._desc_lbl = Label(
            text=description,
            font_size=sp(13),
            color=get_color_from_hex("#9CA3AF"),
            halign="center",
            valign="top",
            size_hint_y=None,
            height=dp(20),
        )
        self.add_widget(self._desc_lbl)

        self.bind(pos=self._draw, size=self._draw)

    def _draw(self, *a):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(0, 0, 0, 0.05)
            RoundedRectangle(pos=(self.x + dp(2), self.y - dp(2)), size=self.size, radius=[dp(18)])
            Color(1, 1, 1, 1)
            RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(18)])
            Color(*get_color_from_hex("#F0F1F3"))
            Line(rounded_rectangle=(self.x, self.y, self.width, self.height, dp(18)), width=dp(0.8))
