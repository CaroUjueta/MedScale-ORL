from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.utils import get_color_from_hex
from kivy.app import App
from kivy.clock import Clock
from kivy.metrics import dp, sp
from kivy.graphics import Color, Rectangle

from frontend.widgets.header import HomeHeader
from frontend.widgets.area_card import ViaAereaCard, RinosinusitisCard, OtologiaCard
from frontend.widgets.quick_action_card import QuickActionCard
from frontend.widgets.info_banner import EvidenceBanner
from frontend.widgets.bottom_nav import BottomNavigation

C_TEXT = get_color_from_hex("#1F2937")
C_ACCENT = get_color_from_hex("#14828A")


def navigate_to(name):
    App.get_running_app().root.current = name


class HomeScreen(Screen):
    instance = None

    def __init__(self, **kwargs):
        HomeScreen.instance = self
        super().__init__(**kwargs)

        root = BoxLayout(orientation="vertical")

        self._header = HomeHeader()
        root.add_widget(self._header)

        sv = ScrollView(
            bar_width=dp(3),
            bar_color=get_color_from_hex("#D0D0D0"),
            scroll_type=["content"],
        )
        content = BoxLayout(
            orientation="vertical",
            padding=[dp(20), 0],
            size_hint_y=None,
        )
        content.bind(minimum_height=content.setter("height"))

        content.add_widget(Widget(size_hint_y=None, height=dp(28)))

        content.add_widget(self._section_title("Explora por área"))
        content.add_widget(Widget(size_hint_y=None, height=dp(20)))

        content.add_widget(ViaAereaCard())
        content.add_widget(Widget(size_hint_y=None, height=dp(8)))
        content.add_widget(RinosinusitisCard())
        content.add_widget(Widget(size_hint_y=None, height=dp(8)))
        content.add_widget(OtologiaCard())

        content.add_widget(Widget(size_hint_y=None, height=dp(28)))

        content.add_widget(self._section_title("Acciones rapidas"))
        content.add_widget(Widget(size_hint_y=None, height=dp(20)))

        content.add_widget(self._build_quick_grid())

        content.add_widget(Widget(size_hint_y=None, height=dp(28)))

        content.add_widget(EvidenceBanner())

        content.add_widget(Widget(size_hint_y=None, height=dp(28)))

        sv.add_widget(content)
        root.add_widget(sv)

        self._bottom_nav = BottomNavigation()
        root.add_widget(self._bottom_nav)

        self.add_widget(root)

    def _section_title(self, text):
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
        row.bind(pos=lambda s, p: setattr(s._line, 'pos', (p[0], p[1] + dp(6))))

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
        lbl.bind(size=lambda s, sz: setattr(s, 'text_size', (sz[0], None)))
        row.add_widget(lbl)
        return row

    def _build_quick_grid(self):
        grid = GridLayout(
            cols=4,
            spacing=dp(12),
            size_hint_y=None,
        )
        grid.bind(minimum_height=grid.setter("height"))

        actions = [
            ("favoritos.png", "Favoritos", "Escalas guardadas", "favoritos"),
            ("recientes.png", "Recientes", "Últimas escalas utilizadas", "recientes"),
            ("pacientes.png", "Pacientes", "Registro y seguimiento", "patient_list"),
            ("guia.png", "Guías rápidas", "Algoritmos y recomendaciones", "guias"),
        ]

        cards = []
        for icon, title, subtitle, target in actions:
            card = QuickActionCard(
                source=icon,
                title=title,
                subtitle=subtitle,
                target=target,
            )
            cards.append(card)
            grid.add_widget(card)

        def _size_cards(dt):
            w = grid.width
            if w < 1:
                Clock.schedule_once(_size_cards, 0.05)
                return
            last = getattr(_size_cards, "last", 0.0)
            card_w = (w - dp(12) * 3) / 4.0
            for c in cards:
                c.size = (card_w, dp(140))
            if abs(w - last) > 1:
                _size_cards.last = w
                Clock.schedule_once(_size_cards, 0.05)

        Clock.schedule_once(_size_cards, 0.1)

        return grid
