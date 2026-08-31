from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.utils import get_color_from_hex
from kivy.metrics import dp, sp
from kivy.graphics import Color, RoundedRectangle

from frontend.widgets.app_header import SimpleHeader, navigate_to
from frontend.widgets.bottom_nav import BottomNavigation
from frontend.widgets.ui import content_column, scroll_with, section_title


C_TEXT = get_color_from_hex("#1F2937")
C_TEXT_SEC = get_color_from_hex("#6B7280")
C_ACCENT = get_color_from_hex("#14828A")
C_PRIMARY = get_color_from_hex("#1976D2")
C_DIVIDER = get_color_from_hex("#E5E7EB")


class PerfilScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        root = BoxLayout(orientation="vertical")

        root.add_widget(SimpleHeader("Perfil", back_target=None))

        self._content = content_column()
        root.add_widget(scroll_with(self._content))

        self._nav = BottomNavigation()
        root.add_widget(self._nav)

        self.add_widget(root)

    def on_enter(self):
        self._nav.set_active(4)
        self._rebuild()

    def _card(self, layout, title, text):
        card = BoxLayout(
            orientation="vertical",
            size_hint_y=None,
            height=dp(72),
            padding=[dp(16), dp(10)],
            spacing=dp(2),
        )
        with card.canvas.before:
            Color(0, 0, 0, 0.06)
            card._shadow = RoundedRectangle(
                pos=(card.x + dp(2), card.y - dp(3)), size=card.size, radius=[dp(16)]
            )
            Color(1, 1, 1, 1)
            card._bg = RoundedRectangle(pos=card.pos, size=card.size, radius=[dp(16)])
        card.bind(
            pos=lambda s, p: (
                setattr(s._shadow, "pos", (p[0] + dp(2), p[1] - dp(3))),
                setattr(s._bg, "pos", p),
            )
        )
        card.bind(
            size=lambda s, sz: (
                setattr(s._shadow, "size", sz),
                setattr(s._bg, "size", sz),
            )
        )

        t = Label(
            text=title,
            font_size=sp(14),
            bold=True,
            color=C_TEXT,
            halign="left",
            valign="middle",
            size_hint_y=None,
            height=dp(24),
        )
        t.bind(size=lambda s, sz: setattr(s, "text_size", (sz[0], None)))
        card.add_widget(t)

        d = Label(
            text=text,
            font_size=sp(13),
            color=C_TEXT_SEC,
            halign="left",
            valign="middle",
            size_hint_y=None,
            height=dp(22),
        )
        d.bind(size=lambda s, sz: setattr(s, "text_size", (sz[0], None)))
        card.add_widget(d)

        layout.add_widget(card)

    def _rebuild(self):
        from frontend.database import obtener_toda_config

        self._content.clear_widgets()
        self._content.add_widget(section_title("Cuenta"))

        self._card(
            self._content,
            "MedScale-ORL",
            "Herramientas clinicas basadas en evidencias.",
        )
        self._card(
            self._content,
            "Perfil",
            "¡Hola, Doctor(a)!",
        )

        self._content.add_widget(section_title("Notificaciones"))

        cfg = obtener_toda_config()
        self._card(self._content, "Correo fijo", cfg.get("correo_fijo") or "-")
        self._card(
            self._content,
            "Correo configurable",
            cfg.get("correo_configurable") or "-",
        )

        btn = Button(
            text="Abrir configuracion",
            size_hint_y=None,
            height=dp(50),
            font_size=sp(15),
            bold=True,
            background_normal="",
            background_color=C_PRIMARY,
            color=get_color_from_hex("#FFFFFF"),
        )
        btn.bind(on_press=lambda _: navigate_to("settings"))
        self._content.add_widget(btn)