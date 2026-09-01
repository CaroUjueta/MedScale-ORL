from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.utils import get_color_from_hex
from kivy.metrics import dp, sp
from kivy.graphics import Color, RoundedRectangle


C_TEXT = get_color_from_hex("#1F2937")
C_TEXT_SEC = get_color_from_hex("#6B7280")
C_ACCENT = get_color_from_hex("#14828A")
C_STAR = get_color_from_hex("#F5A623")


def navigate_to(name):
    from kivy.app import App
    App.get_running_app().root.current = name


class ScaleRow(BoxLayout):
    def __init__(self, scale, show_star=False, date=None, on_open=None, on_toggle=None, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "horizontal"
        self.size_hint_y = None
        self.height = dp(92)
        self.padding = [dp(14), dp(10), dp(10), dp(10)]
        self._scale = scale
        self._on_open = on_open
        self._on_toggle = on_toggle

        with self.canvas.before:
            Color(0, 0, 0, 0.06)
            self._shadow = RoundedRectangle(
                pos=(self.x + dp(2), self.y - dp(3)), size=self.size, radius=[dp(16)]
            )
            Color(1, 1, 1, 1)
            self._bg = RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(16)])
            Color(*C_ACCENT)
            self._bar = RoundedRectangle(
                pos=(self.x + dp(6), self.y + dp(14)),
                size=(dp(4), self.height - dp(28)),
                radius=[dp(2)],
            )
        self.bind(pos=self._draw, size=self._draw)

        col = BoxLayout(orientation="vertical", size_hint_x=1, spacing=dp(2))
        title = Label(
            text=scale["nombre"],
            font_size=sp(16),
            bold=True,
            color=C_TEXT,
            halign="left",
            valign="middle",
            size_hint_y=None,
            height=dp(26),
        )
        title.bind(size=self._set_text_size)
        col.add_widget(title)

        if date:
            desc = Label(
                text=f'{scale["desc"]}  |  {date}',
                font_size=sp(12),
                color=C_TEXT_SEC,
                halign="left",
                valign="middle",
                size_hint_y=None,
                height=dp(20),
            )
            desc.bind(size=self._set_text_size)
            col.add_widget(desc)
        else:
            desc = Label(
                text=scale["desc"],
                font_size=sp(12),
                color=C_TEXT_SEC,
                halign="left",
                valign="middle",
                size_hint_y=None,
                height=dp(20),
            )
            desc.bind(size=self._set_text_size)
            col.add_widget(desc)

        chips = "  ".join(f"#{c}" for c in scale["chips"])
        chips_lbl = Label(
            text=chips,
            font_size=sp(11),
            color=C_ACCENT,
            halign="left",
            valign="middle",
            size_hint_y=None,
            height=dp(18),
        )
        chips_lbl.bind(size=self._set_text_size)
        col.add_widget(chips_lbl)

        self.add_widget(col)

        self.add_widget(Widget(size_hint_x=None, width=dp(4)))

        self._star_lbl = None
        if show_star:
            self._star_lbl = Label(
                text="★" if self._is_fav() else "☆",
                font_size=sp(24),
                color=C_STAR,
                halign="center",
                valign="middle",
                size_hint=(None, None),
                size=(dp(40), dp(40)),
                pos_hint={"center_y": 0.5},
            )
            self.add_widget(self._star_lbl)
            self.add_widget(Widget(size_hint_x=None, width=dp(2)))

        arrow = Button(
            text=">",
            size_hint=(None, None),
            size=(dp(34), dp(34)),
            pos_hint={"center_y": 0.5},
            background_normal="",
            background_color=get_color_from_hex("#F3F4F6"),
            color=C_TEXT_SEC,
            font_size=sp(16),
            bold=True,
        )
        self.add_widget(arrow)

    def _is_fav(self):
        from frontend.database import es_favorita
        return es_favorita(self._scale["id"])

    @staticmethod
    def _set_text_size(label, size):
        label.text_size = (size[0], None)

    def _draw(self, *a):
        if not hasattr(self, "_shadow"):
            return
        self._shadow.pos = (self.x + dp(2), self.y - dp(3))
        self._shadow.size = self.size
        self._bg.pos = self.pos
        self._bg.size = self.size
        self._bar.pos = (self.x + dp(6), self.y + dp(14))
        self._bar.size = (dp(4), self.height - dp(28))

    def on_touch_down(self, touch):
        if not self.collide_point(*touch.pos):
            return False
        local = self.to_widget(*touch.pos, relative=True)
        if self._star_lbl is not None and self._star_lbl.collide_point(*local):
            self._toggle_star()
            return True
        if self._on_open is not None:
            self._on_open(self._scale)
        else:
            navigate_to(self._scale["id"])
        return True

    def _toggle_star(self):
        from frontend.database import quitar_favorita, agregar_favorita

        if self._is_fav():
            quitar_favorita(self._scale["id"])
            self._star_lbl.text = "☆"
        else:
            agregar_favorita(self._scale["id"])
            self._star_lbl.text = "★"
        if self._on_toggle is not None:
            self._on_toggle()