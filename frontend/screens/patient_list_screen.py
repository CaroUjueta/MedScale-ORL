from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
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


class PatientListScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        root = BoxLayout(orientation="vertical")
        root.add_widget(self._build_header())
        self._search = None
        self._list_container = BoxLayout(orientation="vertical")
        root.add_widget(self._list_container)
        self.add_widget(root)

    def on_enter(self):
        self._refresh_list()

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
            text="Mis Pacientes",
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

    def _refresh_list(self, busqueda=None):
        from frontend.database import obtener_pacientes

        self._list_container.clear_widgets()

        search_row = BoxLayout(
            orientation="horizontal",
            size_hint_y=None,
            height=dp(50),
            padding=[dp(16), dp(8)],
            spacing=dp(8),
        )
        self._search_input = TextInput(
            hint_text="Buscar por expediente...",
            multiline=False,
            size_hint_x=0.7,
            font_size=sp(13),
            padding=[dp(10), dp(8)],
            background_normal="",
            background_active="",
            background_color=C_BG,
            cursor_color=C_PRIMARY,
            foreground_color=C_TEXT,
            hint_text_color=C_TEXT_SEC,
        )
        self._search_input.bind(text=lambda s, t: self._do_search(t))
        search_row.add_widget(self._search_input)

        search_btn = Button(
            text="Buscar",
            size_hint_x=0.3,
            font_size=sp(13),
            background_normal="",
            background_color=C_PRIMARY,
            color=get_color_from_hex("#FFFFFF"),
        )
        search_btn.bind(on_press=lambda _: self._do_search(self._search_input.text))
        search_row.add_widget(search_btn)
        self._list_container.add_widget(search_row)

        pacientes = obtener_pacientes(busqueda)

        add_btn = Button(
            text="+ Nuevo Paciente",
            size_hint_y=None,
            height=dp(50),
            font_size=sp(15),
            bold=True,
            background_normal="",
            background_color=C_ACCENT,
            color=get_color_from_hex("#FFFFFF"),
        )
        add_btn.bind(on_press=lambda _: navigate_to("patient_form"))

        scroll = ScrollView(bar_width=dp(3), bar_color=C_DIVIDER)
        btn_list = BoxLayout(
            orientation="vertical",
            size_hint_y=None,
            spacing=dp(6),
            padding=[dp(16), dp(8)],
        )

        btn_list.add_widget(add_btn)

        if not pacientes:
            btn_list.add_widget(Label(
                text="No hay pacientes registrados",
                font_size=sp(13),
                color=C_TEXT_SEC,
                halign="center",
                size_hint_y=None,
                height=dp(50),
            ))
        else:
            for p in pacientes:
                card = Button(
                    size_hint_y=None,
                    height=dp(72),
                    font_size=sp(13),
                    background_normal="",
                    background_color=C_CARD,
                    color=C_TEXT,
                    halign="left",
                )
                sexo_txt = "Masculino" if p["sexo"] == "M" else "Femenino"
                card.text = f"  Exp: {p['expediente']}\n  {p['edad']} anios  |  {sexo_txt}"
                card.bind(
                    on_press=lambda _, pid=p["id"]: self._open_patient(pid)
                )
                btn_list.add_widget(card)

        btn_list.bind(minimum_height=btn_list.setter("height"))
        scroll.add_widget(btn_list)
        self._list_container.add_widget(scroll)

    def _do_search(self, text):
        self._refresh_list(busqueda=text.strip() if text.strip() else None)

    def _open_patient(self, paciente_id):
        app = App.get_running_app()
        detail = app.root.get_screen("patient_detail")
        detail.set_paciente_id(paciente_id)
        navigate_to("patient_detail")
