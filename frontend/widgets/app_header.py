from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.utils import get_color_from_hex
from kivy.metrics import dp, sp
from kivy.graphics import Color, Rectangle


C_PRIMARY_DARK = get_color_from_hex("#1565C0")
C_ACCENT = get_color_from_hex("#26A69A")
C_WHITE = get_color_from_hex("#FFFFFF")


def navigate_to(name):
    from kivy.app import App
    App.get_running_app().root.current = name


class SimpleHeader(BoxLayout):
    def __init__(self, title, back_target="home", extra=None, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "horizontal"
        self.size_hint_y = None
        self.height = dp(52)
        self.padding = [dp(8), 0]

        with self.canvas.before:
            Color(*C_PRIMARY_DARK)
            self._bg = Rectangle(pos=self.pos, size=self.size)
        self.bind(pos=lambda s, p: setattr(self._bg, "pos", p))
        self.bind(size=lambda s, sz: setattr(self._bg, "size", sz))

        if back_target:
            back = Button(
                text="<",
                size_hint=(None, None),
                size=(dp(44), dp(36)),
                pos_hint={"center_y": 0.5},
                background_normal="",
                background_color=C_ACCENT,
                color=C_WHITE,
                font_size=sp(18),
                bold=True,
            )
            back.bind(on_press=lambda _: navigate_to(back_target))
            self.add_widget(back)

        title_lbl = Label(
            text=title,
            font_size=sp(16),
            bold=True,
            color=C_WHITE,
            halign="left",
            valign="middle",
            size_hint_x=1,
        )
        self._title_lbl = title_lbl

        def _resize(w, value):
            w.text_size = (value - dp(12), None)

        title_lbl.bind(width=_resize)
        self.add_widget(title_lbl)

        if extra is not None:
            self.add_widget(extra)

    def set_title(self, text):
        self._title_lbl.text = text