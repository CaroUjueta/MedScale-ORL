from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.utils import get_color_from_hex
from kivy.app import App
from kivy.metrics import dp, sp

C_PRIMARY = get_color_from_hex("#1976D2")
C_PRIMARY_DARK = get_color_from_hex("#1565C0")
C_ACCENT = get_color_from_hex("#26A69A")
C_BG = get_color_from_hex("#F0F2F5")
C_CARD = get_color_from_hex("#FFFFFF")
C_TEXT = get_color_from_hex("#1A1A2E")
C_TEXT_SEC = get_color_from_hex("#9CA3AF")
C_BOTTOM = get_color_from_hex("#FFFFFF")


def navigate_to(name):
    App.get_running_app().root.current = name


class ScaleCard(Button):
    def __init__(self, label, target, **kwargs):
        super().__init__(**kwargs)
        self.text = label
        self._target = target
        self.size_hint_y = None
        self.height = dp(54)
        self.background_normal = ""
        self.background_color = C_PRIMARY
        self.color = get_color_from_hex("#FFFFFF")
        self.font_size = sp(15)
        self.bold = True
        self.bind(on_press=self._go)

    def _go(self, _):
        navigate_to(self._target)


class NavButton(Button):
    def __init__(self, label, **kwargs):
        super().__init__(**kwargs)
        self.text = label
        self.size_hint_x = 1
        self.background_normal = ""
        self.background_color = C_BOTTOM
        self.color = C_TEXT_SEC
        self.font_size = sp(11)
        self.bold = True
        self.bind(on_press=self._on_press)

    def _on_press(self, _):
        tab_idx = int(self._tab_name == "Rinosinusitis") + int(self._tab_name == "Otologia")
        HomeScreen.instance.set_tab(tab_idx)


class HomeScreen(Screen):
    instance = None

    def __init__(self, **kwargs):
        HomeScreen.instance = self
        super().__init__(**kwargs)
        self._current_tab = 0

        root = BoxLayout(orientation="vertical")

        self._content_area = BoxLayout(orientation="vertical", size_hint_y=1)
        root.add_widget(self._content_area)

        self._build_bottom_nav(root)
        self._build_tabs_content()
        self.set_tab(0)

        self.add_widget(root)

    def _build_bottom_nav(self, root):
        self._nav_buttons = []
        nav_labels = ["Apnea", "Rinosinusitis", "Otologia"]

        nav = BoxLayout(
            orientation="horizontal",
            size_hint_y=None,
            height=dp(60),
            padding=[0, dp(4), 0, dp(4)],
        )
        with nav.canvas.before:
            from kivy.graphics import Color, Rectangle
            Color(*C_BOTTOM)
            nav._bg = Rectangle(pos=nav.pos, size=nav.size)
            Color(0, 0, 0, 0.08)
            nav._shadow = Rectangle(pos=(nav.x, nav.top), size=(nav.width, dp(1)))
        nav.bind(pos=lambda s, p: (setattr(nav._bg, 'pos', p), setattr(nav._shadow, 'pos', (p[0], p[1] + s.height))))
        nav.bind(size=lambda s, sz: (setattr(nav._bg, 'size', sz), setattr(nav._shadow, 'size', (sz[0], dp(1)))))

        for label in nav_labels:
            btn = Button(
                text=label,
                size_hint_x=1,
                background_normal="",
                background_color=C_BOTTOM,
                color=C_TEXT_SEC,
                font_size=sp(11),
                bold=True,
            )
            self._nav_buttons.append(btn)
            nav.add_widget(btn)

        self._nav_buttons[0].bind(on_press=lambda _: self.set_tab(0))
        self._nav_buttons[1].bind(on_press=lambda _: self.set_tab(1))
        self._nav_buttons[2].bind(on_press=lambda _: self.set_tab(2))

        root.add_widget(nav)

        credits = Label(
            text="Carolina Ujueta & Francys Ujueta",
            font_size=sp(9),
            color=get_color_from_hex("#B0B0B0"),
            size_hint_y=None,
            height=dp(20),
            halign="center",
            valign="middle",
        )
        root.add_widget(credits)

    def _build_tabs_content(self):
        self._tabs = []

        categories = [
            ("Apnea Obstructiva del Sueño", [
                ("Epworth Sleepiness Scale (ESS)", "ess"),
                ("STOP-BANG", "stop_bang"),
                ("IMC (Indice de Masa Corporal)", "imc"),
            ]),
            ("Rinosinusitis", [
                ("SNOT-22", "snot22"),
                ("Lund Mackay", "lund_mackay"),
            ]),
            ("Otologia", [
                ("THI (Tinnitus Handicap Inventory)", "thi"),
                ("ETDQ-7", "etdq7"),
            ]),
        ]

        for cat_name, scales in categories:
            container = BoxLayout(orientation="vertical")

            header = BoxLayout(
                orientation="horizontal",
                size_hint_y=None,
                height=dp(44),
                padding=[dp(16), 0],
            )
            with header.canvas.before:
                from kivy.graphics import Color, Rectangle
                Color(*C_BG)
                header._bg = Rectangle(pos=header.pos, size=header.size)
            header.bind(pos=lambda s, p: setattr(s._bg, 'pos', p))
            header.bind(size=lambda s, sz: setattr(s._bg, 'size', sz))
            header.add_widget(Label(
                text=cat_name.upper(),
                font_size=sp(11),
                bold=True,
                color=C_TEXT_SEC,
                halign="left",
                valign="middle",
            ))
            header.children[-1].bind(
                width=lambda s, w: setattr(s, 'text_size', (w - dp(16), None))
            )
            container.add_widget(header)

            inner = BoxLayout(
                orientation="vertical",
                padding=[dp(16), dp(12)],
                spacing=dp(8),
                size_hint_y=None,
            )
            inner.bind(minimum_height=inner.setter("height"))

            for label, target in scales:
                inner.add_widget(ScaleCard(label=label, target=target))

            inner.add_widget(Widget(size_hint_y=1))

            sv = ScrollView(bar_width=0)
            sv.add_widget(inner)
            container.add_widget(sv)
            self._tabs.append(container)

    def set_tab(self, idx):
        self._current_tab = idx
        self._content_area.clear_widgets()
        self._content_area.add_widget(self._tabs[idx])
        for i, btn in enumerate(self._nav_buttons):
            if i == idx:
                btn.color = C_PRIMARY
                btn.bold = True
            else:
                btn.color = C_TEXT_SEC
                btn.bold = False
