from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.utils import get_color_from_hex
from kivy.metrics import dp, sp
from kivy.graphics import Color, Rectangle


C_TEXT = get_color_from_hex("#1F2937")
C_ACCENT = get_color_from_hex("#14828A")
C_DIVIDER = get_color_from_hex("#E5E7EB")


def content_column(vertical_padding=16):
    content = BoxLayout(
        orientation="vertical",
        padding=[dp(16), dp(vertical_padding)],
        spacing=dp(10),
        size_hint_y=None,
    )
    content.bind(minimum_height=content.setter("height"))
    return content


def scroll_with(content, bar_color=C_DIVIDER):
    sv = ScrollView(bar_width=dp(3), bar_color=bar_color)
    sv.add_widget(content)
    return sv


def section_title(text):
    row = BoxLayout(
        orientation="horizontal",
        size_hint_y=None,
        height=dp(32),
        spacing=dp(8),
    )
    with row.canvas.before:
        Color(*C_ACCENT)
        row._line = Rectangle(
            pos=(row.x, row.y + dp(6)),
            size=(dp(3), dp(20)),
        )
    row.bind(pos=lambda s, p: setattr(s._line, "pos", (p[0], p[1] + dp(6))))

    lbl = Label(
        text=text,
        font_size=sp(16),
        bold=True,
        color=C_TEXT,
        halign="left",
        valign="middle",
        size_hint_x=1,
        padding=[dp(8), 0],
    )
    lbl.bind(size=lambda s, sz: setattr(s, "text_size", (sz[0], None)))
    row.add_widget(lbl)
    return row


def empty_message(layout, text):
    layout.add_widget(Label(
        text=text,
        font_size=sp(13),
        color=C_TEXT,
        halign="center",
        valign="middle",
        size_hint_y=None,
        height=dp(80),
        text_size=(None, None),
    ))


def add_recent_usage(scale_id):
    from frontend.database import registrar_uso_escala
    registrar_uso_escala(scale_id)