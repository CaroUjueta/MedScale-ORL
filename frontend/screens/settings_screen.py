from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.utils import get_color_from_hex
from kivy.app import App
from kivy.metrics import dp, sp

C_PRIMARY = get_color_from_hex("#1976D2")
C_PRIMARY_DARK = get_color_from_hex("#1565C0")
C_ACCENT = get_color_from_hex("#26A69A")
C_BG = get_color_from_hex("#F0F2F5")
C_CARD = get_color_from_hex("#FFFFFF")
C_TEXT = get_color_from_hex("#1A1A2E")
C_TEXT_SEC = get_color_from_hex("#6B7280")
C_DIVIDER = get_color_from_hex("#E5E7EB")


def navigate_to(name):
    App.get_running_app().root.current = name


class SettingsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        root = BoxLayout(orientation="vertical")
        root.add_widget(self._build_header())

        sv = ScrollView(bar_width=dp(3), bar_color=C_DIVIDER)
        content = BoxLayout(
            orientation="vertical",
            padding=[dp(16), dp(12)],
            spacing=dp(10),
            size_hint_y=None,
        )
        content.bind(minimum_height=content.setter("height"))

        content.add_widget(Label(
            text="CORREO DESTINO",
            font_size=sp(11),
            bold=True,
            color=C_TEXT_SEC,
            halign="left",
            text_size=(None, None),
            size_hint_y=None,
            height=dp(24),
        ))
        content.children[-1].bind(
            width=lambda s, w: setattr(s, 'text_size', (w - dp(8), None))
        )

        content.add_widget(Label(
            text="Correo fijo (siempre recibe):",
            font_size=sp(12),
            color=C_TEXT,
            halign="left",
            text_size=(None, None),
            size_hint_y=None,
            height=dp(20),
        ))
        content.children[-1].bind(
            width=lambda s, w: setattr(s, 'text_size', (w - dp(8), None))
        )

        self._fijo_input = TextInput(
            hint_text="correo@ejemplo.com",
            multiline=False,
            font_size=sp(13),
            size_hint_y=None,
            height=dp(42),
            padding=[dp(10), dp(8)],
            background_normal="",
            background_active="",
            background_color=C_BG,
            cursor_color=C_PRIMARY,
            foreground_color=C_TEXT,
            hint_text_color=C_TEXT_SEC,
        )
        content.add_widget(self._fijo_input)

        content.add_widget(Label(
            text="Correo configurable (quien usa la app puede cambiarlo):",
            font_size=sp(12),
            color=C_TEXT,
            halign="left",
            text_size=(None, None),
            size_hint_y=None,
            height=dp(20),
        ))
        content.children[-1].bind(
            width=lambda s, w: setattr(s, 'text_size', (w - dp(8), None))
        )

        self._config_input = TextInput(
            hint_text="correo@ejemplo.com",
            multiline=False,
            font_size=sp(13),
            size_hint_y=None,
            height=dp(42),
            padding=[dp(10), dp(8)],
            background_normal="",
            background_active="",
            background_color=C_BG,
            cursor_color=C_PRIMARY,
            foreground_color=C_TEXT,
            hint_text_color=C_TEXT_SEC,
        )
        content.add_widget(self._config_input)

        content.add_widget(BoxLayout(size_hint_y=None, height=dp(10)))

        content.add_widget(Label(
            text="CREDENCIALES SMTP (Gmail)",
            font_size=sp(11),
            bold=True,
            color=C_TEXT_SEC,
            halign="left",
            text_size=(None, None),
            size_hint_y=None,
            height=dp(24),
        ))
        content.children[-1].bind(
            width=lambda s, w: setattr(s, 'text_size', (w - dp(8), None))
        )

        content.add_widget(Label(
            text="Usuario Gmail:",
            font_size=sp(12),
            color=C_TEXT,
            halign="left",
            text_size=(None, None),
            size_hint_y=None,
            height=dp(20),
        ))
        content.children[-1].bind(
            width=lambda s, w: setattr(s, 'text_size', (w - dp(8), None))
        )

        self._usuario_input = TextInput(
            hint_text="tu_usuario@gmail.com",
            multiline=False,
            font_size=sp(13),
            size_hint_y=None,
            height=dp(42),
            padding=[dp(10), dp(8)],
            background_normal="",
            background_active="",
            background_color=C_BG,
            cursor_color=C_PRIMARY,
            foreground_color=C_TEXT,
            hint_text_color=C_TEXT_SEC,
        )
        content.add_widget(self._usuario_input)

        content.add_widget(Label(
            text="Clave de aplicacion (App Password):",
            font_size=sp(12),
            color=C_TEXT,
            halign="left",
            text_size=(None, None),
            size_hint_y=None,
            height=dp(20),
        ))
        content.children[-1].bind(
            width=lambda s, w: setattr(s, 'text_size', (w - dp(8), None))
        )

        self._clave_input = TextInput(
            hint_text="App Password de 16 caracteres",
            multiline=False,
            font_size=sp(13),
            size_hint_y=None,
            height=dp(42),
            password=True,
            padding=[dp(10), dp(8)],
            background_normal="",
            background_active="",
            background_color=C_BG,
            cursor_color=C_PRIMARY,
            foreground_color=C_TEXT,
            hint_text_color=C_TEXT_SEC,
        )
        content.add_widget(self._clave_input)

        content.add_widget(BoxLayout(size_hint_y=None, height=dp(10)))

        save_btn = Button(
            text="Guardar configuracion",
            size_hint_y=None,
            height=dp(50),
            font_size=sp(15),
            bold=True,
            background_normal="",
            background_color=C_PRIMARY,
            color=get_color_from_hex("#FFFFFF"),
        )
        save_btn.bind(on_press=self._save)
        content.add_widget(save_btn)

        self._msg_label = Label(
            text="",
            font_size=sp(12),
            color=C_ACCENT,
            halign="center",
            size_hint_y=None,
            height=dp(26),
        )
        content.add_widget(self._msg_label)

        sv.add_widget(content)
        root.add_widget(sv)
        self.add_widget(root)

    def on_enter(self):
        from frontend.database import obtener_config
        self._fijo_input.text = obtener_config("correo_fijo") or ""
        self._config_input.text = obtener_config("correo_configurable") or ""
        self._usuario_input.text = obtener_config("smtp_usuario") or ""
        self._clave_input.text = obtener_config("smtp_clave") or ""

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
            text="Configuracion",
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

    def _save(self, _):
        from frontend.database import actualizar_config

        actualizar_config("correo_fijo", self._fijo_input.text.strip())
        actualizar_config("correo_configurable", self._config_input.text.strip())
        actualizar_config("smtp_usuario", self._usuario_input.text.strip())
        actualizar_config("smtp_clave", self._clave_input.text.strip())

        self._msg_label.text = "Configuracion guardada"
