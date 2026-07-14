from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.utils import get_color_from_hex
from kivy.app import App

C_PRIMARY = get_color_from_hex("#1976D2")
C_PRIMARY_DARK = get_color_from_hex("#1565C0")
C_ACCENT = get_color_from_hex("#26A69A")
C_BG = get_color_from_hex("#F0F2F5")
C_CARD = get_color_from_hex("#FFFFFF")
C_TEXT = get_color_from_hex("#1A1A2E")
C_TEXT_SEC = get_color_from_hex("#6B7280")
C_TAB_SEL = get_color_from_hex("#E3F2FD")


def navigate_to(name):
    App.get_running_app().root.current = name


class ScaleCard(Button):
    def __init__(self, label, target, **kwargs):
        super().__init__(**kwargs)
        self.text = label
        self._target = target
        self.size_hint_y = None
        self.height = 56
        self.background_normal = ""
        self.background_color = C_PRIMARY
        self.color = get_color_from_hex("#FFFFFF")
        self.font_size = "15sp"
        self.bold = True
        self.bind(on_press=self._go)

    def _go(self, _):
        navigate_to(self._target)


class HomeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        root = BoxLayout(orientation="vertical")

        header = BoxLayout(size_hint_y=None, height=56)
        with header.canvas.before:
            from kivy.graphics import Color, Rectangle
            Color(*C_PRIMARY_DARK)
            header._bg = Rectangle(pos=header.pos, size=header.size)
        header.bind(pos=lambda s, p: setattr(header._bg, 'pos', p))
        header.bind(size=lambda s, sz: setattr(header._bg, 'size', sz))
        header.add_widget(Label(
            text="  MedScale-ORL",
            font_size="20sp",
            bold=True,
            color=get_color_from_hex("#FFFFFF"),
            halign="left",
            valign="middle",
        ))
        root.add_widget(header)

        tp = TabbedPanel(
            tab_height=46,
            do_default_tab=False,
            background_color=C_BG,
        )

        categories = [
            ("Apnea", [
                ("Epworth (ESS)", "ess"),
                ("STOP-BANG", "stop_bang"),
                ("IMC", "imc"),
            ]),
            ("Rinosinusitis", [
                ("SNOT-22", "snot22"),
                ("Lund Mackay", "lund_mackay"),
            ]),
            ("Otologia", [
                ("THI", "thi"),
                ("ETDQ-7", "etdq7"),
            ]),
        ]

        for tab_name, scales in categories:
            tab = TabbedPanelItem(text=tab_name)
            tab.background_normal = ""
            tab.background_disabled_normal = ""
            tab.background_color = C_BG
            tab.color = C_TEXT_SEC
            tab.bold = True
            tab.bind(state=self._on_tab_state)

            inner = BoxLayout(
                orientation="vertical",
                padding=[20, 12],
                spacing=8,
            )

            inner.add_widget(Label(
                text=tab_name,
                font_size="18sp",
                bold=True,
                color=C_PRIMARY,
                size_hint_y=None,
                height=40,
                halign="left",
                valign="middle",
            ))
            inner.children[-1].bind(
                width=lambda s, w: setattr(s, 'text_size', (w - 8, None))
            )

            for label, target in scales:
                inner.add_widget(ScaleCard(label=label, target=target))

            inner.add_widget(Label(size_hint_y=1))

            sv = ScrollView(bar_width=0)
            sv.add_widget(inner)
            tab.content = sv
            tp.add_widget(tab)

        tp.default_tab_text = "Apnea"
        root.add_widget(tp)
        self.add_widget(root)

    def _on_tab_state(self, instance, value):
        if value == "down":
            instance.color = C_PRIMARY
        else:
            instance.color = C_TEXT_SEC
