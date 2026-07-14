from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.spinner import Spinner
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.utils import get_color_from_hex
from kivy.app import App

C_PRIMARY = get_color_from_hex("#1976D2")
C_PRIMARY_DARK = get_color_from_hex("#1565C0")
C_ACCENT = get_color_from_hex("#26A69A")
C_BG = get_color_from_hex("#F0F2F5")
C_CARD = get_color_from_hex("#FFFFFF")
C_TEXT = get_color_from_hex("#1A1A2E")
C_TEXT_SEC = get_color_from_hex("#6B7280")
C_RESULT = get_color_from_hex("#0D6E6E")
C_RESULT_BG = get_color_from_hex("#E0F2F1")
C_DIVIDER = get_color_from_hex("#E5E7EB")


def navigate_to(screen_name):
    App.get_running_app().root.current = screen_name


class ScaleScreen(Screen):
    title_text = ""
    result_prefix = "Puntaje total:"
    icon_text = ""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        root = BoxLayout(orientation="vertical")
        root.add_widget(self._build_header())
        root.add_widget(self._build_body())
        self.add_widget(root)

    def _build_header(self):
        header = BoxLayout(
            orientation="horizontal",
            size_hint_y=None,
            height=56,
            padding=[8, 0],
        )
        with header.canvas.before:
            from kivy.graphics import Color, Rectangle
            Color(*C_PRIMARY_DARK)
            header._bg = Rectangle(pos=header.pos, size=header.size)
        header.bind(pos=lambda s, p: setattr(header._bg, 'pos', p))
        header.bind(size=lambda s, sz: setattr(header._bg, 'size', sz))

        back = Button(
            text="<",
            size_hint=(None, None),
            size=(48, 40),
            pos_hint={"center_y": 0.5},
            background_normal="",
            background_color=C_ACCENT,
            color=get_color_from_hex("#FFFFFF"),
            font_size="18sp",
            bold=True,
        )
        back.bind(on_press=lambda _: navigate_to("home"))
        header.add_widget(back)

        header.add_widget(Label(
            text=self.title_text,
            font_size="17sp",
            bold=True,
            color=get_color_from_hex("#FFFFFF"),
            halign="left",
            valign="middle",
            text_size=(None, None),
            size_hint_x=1,
        ))
        header.children[-1].bind(
            width=lambda s, w: setattr(s, 'text_size', (w - 16, None))
        )
        return header

    def _build_body(self):
        sv = ScrollView(bar_width=4, bar_color=C_DIVIDER)
        content = BoxLayout(
            orientation="vertical",
            padding=[20, 16],
            spacing=12,
            size_hint_y=None,
        )
        content.bind(minimum_height=content.setter("height"))
        self._build_form(content)
        sv.add_widget(content)
        return sv

    def _build_form(self, layout):
        raise NotImplementedError

    def _question(self, layout, text, options, values=None):
        if values is None:
            values = list(range(len(options)))

        card = BoxLayout(
            orientation="vertical",
            size_hint_y=None,
            height=72,
            padding=[12, 6],
            spacing=2,
        )
        with card.canvas.before:
            from kivy.graphics import Color, Rectangle, RoundedRectangle
            Color(*C_CARD)
            card._bg = RoundedRectangle(
                pos=card.pos, size=card.size, radius=[8]
            )
        card.bind(pos=lambda s, p: setattr(card._bg, 'pos', p))
        card.bind(size=lambda s, sz: setattr(card._bg, 'size', sz))

        lbl = Label(
            text=text,
            font_size="13sp",
            color=C_TEXT,
            halign="left",
            valign="middle",
            text_size=(None, None),
            size_hint_y=0.55,
        )
        lbl.bind(width=lambda s, w: setattr(s, 'text_size', (w - 8, None)))
        card.add_widget(lbl)

        spinner = Spinner(
            text=options[0],
            values=options,
            size_hint=(None, None),
            size=(140, 34),
            font_size="13sp",
            background_normal="",
            background_color=C_BG,
            color=C_TEXT,
            option_cls=self._spinner_option,
        )
        spinner._score_map = dict(zip(options, values))
        spinner_row = BoxLayout(size_hint_y=0.45)
        spinner_row.add_widget(spinner)
        spinner_row.add_widget(Label(size_hint_x=1))
        card.add_widget(spinner_row)

        layout.add_widget(card)
        return spinner

    def _spinner_option(self, *args, **kwargs):
        from kivy.uix.spinner import SpinnerOption
        opt = SpinnerOption(**kwargs)
        opt.background_normal = ""
        opt.background_color = C_CARD
        opt.color = C_TEXT
        opt.font_size = "13sp"
        return opt

    def _numeric_input(self, layout, text, hint):
        card = BoxLayout(
            orientation="vertical",
            size_hint_y=None,
            height=72,
            padding=[12, 6],
            spacing=2,
        )
        with card.canvas.before:
            from kivy.graphics import Color, RoundedRectangle
            Color(*C_CARD)
            card._bg = RoundedRectangle(
                pos=card.pos, size=card.size, radius=[8]
            )
        card.bind(pos=lambda s, p: setattr(card._bg, 'pos', p))
        card.bind(size=lambda s, sz: setattr(card._bg, 'size', sz))

        lbl = Label(
            text=text,
            font_size="13sp",
            color=C_TEXT,
            halign="left",
            valign="middle",
            text_size=(None, None),
            size_hint_y=0.55,
        )
        lbl.bind(width=lambda s, w: setattr(s, 'text_size', (w - 8, None)))
        card.add_widget(lbl)

        ti = TextInput(
            hint_text=hint,
            multiline=False,
            input_filter="float",
            size_hint_y=0.45,
            font_size="14sp",
            padding=[10, 8],
            background_normal="",
            background_active="",
            background_color=C_BG,
            cursor_color=C_PRIMARY,
            foreground_color=C_TEXT,
            hint_text_color=C_TEXT_SEC,
            cursor_width=2,
        )
        card.add_widget(ti)
        layout.add_widget(card)
        return ti

    def _section(self, layout, text):
        layout.add_widget(Label(
            text=text,
            font_size="14sp",
            bold=True,
            color=C_PRIMARY,
            size_hint_y=None,
            height=32,
            halign="left",
            valign="middle",
            text_size=(None, None),
        ))
        layout.children[-1].bind(
            width=lambda s, w: setattr(s, 'text_size', (w - 8, None))
        )

    def _calc_btn(self, layout, callback):
        btn = Button(
            text="Calcular",
            size_hint_y=None,
            height=52,
            font_size="16sp",
            bold=True,
            background_normal="",
            background_color=C_PRIMARY,
            color=get_color_from_hex("#FFFFFF"),
        )
        btn.bind(on_press=callback)
        layout.add_widget(btn)

    def _result_box(self, layout):
        box = BoxLayout(
            orientation="vertical",
            size_hint_y=None,
            height=72,
            padding=[16, 8],
        )
        with box.canvas.before:
            from kivy.graphics import Color, RoundedRectangle
            Color(*C_RESULT_BG)
            box._bg = RoundedRectangle(
                pos=box.pos, size=box.size, radius=[12]
            )
        box.bind(pos=lambda s, p: setattr(box._bg, 'pos', p))
        box.bind(size=lambda s, sz: setattr(box._bg, 'size', sz))

        self._result_lbl = Label(
            text="",
            font_size="24sp",
            bold=True,
            color=C_RESULT,
            halign="center",
            valign="middle",
        )
        box.add_widget(self._result_lbl)
        layout.add_widget(box)

    def _show_result(self, value):
        self._result_lbl.text = f"{self.result_prefix} {value}"
