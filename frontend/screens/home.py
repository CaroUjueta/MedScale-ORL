from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.utils import get_color_from_hex
from kivy.app import App
from kivy.metrics import dp, sp

from frontend.widgets.header import HomeHeader
from frontend.widgets.area_card import ApneaCard, RinosinusitisCard, OtologiaCard
from frontend.widgets.quick_action_card import QuickActionCard
from frontend.widgets.info_banner import EvidenceBanner
from frontend.widgets.bottom_nav import BottomNavigation

C_TEXT = get_color_from_hex("#1F2937")


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
            padding=[dp(20), dp(16)],
            spacing=dp(24),
            size_hint_y=None,
        )
        content.bind(minimum_height=content.setter("height"))

        content.add_widget(self._build_explore_section())
        content.add_widget(self._build_quick_actions())
        content.add_widget(self._build_banner())
        content.add_widget(Widget(size_hint_y=None, height=dp(8)))

        sv.add_widget(content)
        root.add_widget(sv)

        self._bottom_nav = BottomNavigation()
        root.add_widget(self._bottom_nav)

        self.add_widget(root)

    def _build_explore_section(self):
        section = BoxLayout(
            orientation="vertical",
            size_hint_y=None,
            height=dp(380),
            spacing=dp(16),
        )

        header_row = BoxLayout(
            size_hint_y=None,
            height=dp(28),
            spacing=dp(8),
        )
        header_row.add_widget(Widget(
            size_hint_x=None,
            width=dp(4),
        ))
        with header_row.canvas.before:
            from kivy.graphics import Color, Rectangle
            Color(*get_color_from_hex("#14828A"))
            header_row._line = Rectangle(
                pos=(header_row.x + dp(20), header_row.y + dp(4)),
                size=(dp(3), dp(20)),
            )
        header_row.bind(pos=lambda s, p: setattr(s._line, 'pos', (p[0] + dp(20), p[1] + dp(4))))

        lbl = Label(
            text="Explora por area",
            font_size=sp(14),
            bold=True,
            color=C_TEXT,
            halign="left",
            valign="middle",
            text_size=(None, None),
            size_hint_x=1,
        )
        lbl.bind(width=lambda s, w: setattr(s, 'text_size', (w, None)))
        header_row.add_widget(lbl)
        section.add_widget(header_row)

        section.add_widget(ApneaCard())
        section.add_widget(RinosinusitisCard())
        section.add_widget(OtologiaCard())

        return section

    def _build_quick_actions(self):
        section = BoxLayout(
            orientation="vertical",
            size_hint_y=None,
            height=dp(240),
            spacing=dp(16),
        )

        header_row = BoxLayout(
            size_hint_y=None,
            height=dp(28),
            spacing=dp(8),
        )
        header_row.add_widget(Widget(
            size_hint_x=None,
            width=dp(4),
        ))
        with header_row.canvas.before:
            from kivy.graphics import Color, Rectangle
            Color(*get_color_from_hex("#14828A"))
            header_row._line = Rectangle(
                pos=(header_row.x + dp(20), header_row.y + dp(4)),
                size=(dp(3), dp(20)),
            )
        header_row.bind(pos=lambda s, p: setattr(s._line, 'pos', (p[0] + dp(20), p[1] + dp(4))))

        lbl = Label(
            text="Acciones rapidas",
            font_size=sp(14),
            bold=True,
            color=C_TEXT,
            halign="left",
            valign="middle",
            text_size=(None, None),
            size_hint_x=1,
        )
        lbl.bind(width=lambda s, w: setattr(s, 'text_size', (w, None)))
        header_row.add_widget(lbl)
        section.add_widget(header_row)

        actions = [
            ("Favoritos", "Escalas guardadas", "bookmark"),
            ("Recientes", "Ultimas escalas", "history"),
            ("Pacientes", "Registro y seguimiento", "groups"),
            ("Guias rapidas", "Algoritmos y recom.", "book"),
        ]

        row1 = BoxLayout(spacing=dp(12), size_hint_y=None, height=dp(100))
        row2 = BoxLayout(spacing=dp(12), size_hint_y=None, height=dp(100))
        for i, (title, desc, icon) in enumerate(actions):
            card = QuickActionCard(title=title, description=desc, icon_type=icon)
            if i < 2:
                row1.add_widget(card)
            else:
                row2.add_widget(card)

        section.add_widget(row1)
        section.add_widget(row2)
        return section

    def _build_banner(self):
        container = BoxLayout(
            size_hint_y=None,
            height=dp(80),
        )
        container.add_widget(EvidenceBanner())
        return container
