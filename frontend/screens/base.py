from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.utils import get_color_from_hex
from kivy.app import App
from kivy.metrics import dp, sp
from kivy.core.window import Window

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
            height=dp(52),
            padding=[dp(8), 0],
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
            size=(dp(44), dp(36)),
            pos_hint={"center_y": 0.5},
            background_normal="",
            background_color=C_ACCENT,
            color=get_color_from_hex("#FFFFFF"),
            font_size=sp(18),
            bold=True,
        )
        back.bind(on_press=lambda _: navigate_to("home"))
        header.add_widget(back)

        header.add_widget(Label(
            text=self.title_text,
            font_size=sp(16),
            bold=True,
            color=get_color_from_hex("#FFFFFF"),
            halign="left",
            valign="middle",
            text_size=(None, None),
            size_hint_x=1,
        ))
        header.children[-1].bind(
            width=lambda s, w: setattr(s, 'text_size', (w - dp(12), None))
        )
        return header

    def _build_body(self):
        sv = ScrollView(bar_width=dp(3), bar_color=C_DIVIDER)
        content = BoxLayout(
            orientation="vertical",
            padding=[dp(16), dp(12)],
            spacing=dp(10),
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
            height=dp(80),
            padding=[dp(12), dp(6)],
            spacing=dp(4),
        )
        with card.canvas.before:
            from kivy.graphics import Color, RoundedRectangle
            Color(*C_CARD)
            card._bg = RoundedRectangle(
                pos=card.pos, size=card.size, radius=[dp(8)]
            )
        card.bind(pos=lambda s, p: setattr(card._bg, 'pos', p))
        card.bind(size=lambda s, sz: setattr(card._bg, 'size', sz))

        lbl = Label(
            text=text,
            font_size=sp(13),
            color=C_TEXT,
            halign="left",
            valign="middle",
            text_size=(None, None),
            size_hint_y=0.45,
        )
        lbl.bind(width=lambda s, w: setattr(s, 'text_size', (w - dp(8), None)))
        card.add_widget(lbl)

        btn_row = BoxLayout(
            size_hint_y=0.55,
            spacing=dp(4),
        )

        state = {"score": values[0], "selected": 0}
        card._option_state = state

        btn_refs = []
        for i, (opt_text, val) in enumerate(zip(options, values)):
            btn = Button(
                text=opt_text,
                font_size=sp(11),
                bold=(i == 0),
                background_normal="",
                background_color=C_PRIMARY if i == 0 else C_BG,
                color=get_color_from_hex("#FFFFFF") if i == 0 else C_TEXT,
            )
            btn_refs.append(btn)

            def _on_press(_btn, _idx=i, _refs=btn_refs, _st=state, _vals=values, _opts=options):
                _st["score"] = _vals[_idx]
                _st["selected"] = _idx
                for j, b in enumerate(_refs):
                    b.background_color = C_PRIMARY if j == _idx else C_BG
                    b.color = get_color_from_hex("#FFFFFF") if j == _idx else C_TEXT
                    b.bold = (j == _idx)

            btn.bind(on_press=_on_press)
            btn_row.add_widget(btn)

        card.add_widget(btn_row)
        layout.add_widget(card)
        return card

    def _numeric_input(self, layout, text, hint):
        card = BoxLayout(
            orientation="vertical",
            size_hint_y=None,
            height=dp(70),
            padding=[dp(12), dp(6)],
            spacing=dp(2),
        )
        with card.canvas.before:
            from kivy.graphics import Color, RoundedRectangle
            Color(*C_CARD)
            card._bg = RoundedRectangle(
                pos=card.pos, size=card.size, radius=[dp(8)]
            )
        card.bind(pos=lambda s, p: setattr(card._bg, 'pos', p))
        card.bind(size=lambda s, sz: setattr(card._bg, 'size', sz))

        lbl = Label(
            text=text,
            font_size=sp(13),
            color=C_TEXT,
            halign="left",
            valign="middle",
            text_size=(None, None),
            size_hint_y=0.55,
        )
        lbl.bind(width=lambda s, w: setattr(s, 'text_size', (w - dp(8), None)))
        card.add_widget(lbl)

        ti = TextInput(
            hint_text=hint,
            multiline=False,
            input_filter="float",
            size_hint_y=0.45,
            font_size=sp(14),
            padding=[dp(10), dp(8)],
            background_normal="",
            background_active="",
            background_color=C_BG,
            cursor_color=C_PRIMARY,
            foreground_color=C_TEXT,
            hint_text_color=C_TEXT_SEC,
            cursor_width=dp(2),
        )
        card.add_widget(ti)
        layout.add_widget(card)
        return ti

    def _section(self, layout, text):
        lbl = Label(
            text=text,
            font_size=sp(13),
            bold=True,
            color=C_PRIMARY,
            size_hint_y=None,
            height=dp(30),
            halign="left",
            valign="middle",
            text_size=(None, None),
        )
        lbl.bind(width=lambda s, w: setattr(s, 'text_size', (w - dp(8), None)))
        layout.add_widget(lbl)

    def _calc_btn(self, layout, callback):
        btn = Button(
            text="Calcular",
            size_hint_y=None,
            height=dp(50),
            font_size=sp(16),
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
            height=dp(68),
            padding=[dp(16), dp(8)],
        )
        with box.canvas.before:
            from kivy.graphics import Color, RoundedRectangle
            Color(*C_RESULT_BG)
            box._bg = RoundedRectangle(
                pos=box.pos, size=box.size, radius=[dp(12)]
            )
        box.bind(pos=lambda s, p: setattr(box._bg, 'pos', p))
        box.bind(size=lambda s, sz: setattr(box._bg, 'size', sz))

        self._result_lbl = Label(
            text="",
            font_size=sp(22),
            bold=True,
            color=C_RESULT,
            halign="center",
            valign="middle",
        )
        box.add_widget(self._result_lbl)
        layout.add_widget(box)

    def _show_result(self, value):
        self._result_lbl.text = f"{self.result_prefix} {value}"
