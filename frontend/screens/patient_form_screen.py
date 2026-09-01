from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
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


class PatientFormScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._editing_id = None
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
            text="Expediente:",
            font_size=sp(13),
            color=C_TEXT,
            halign="left",
            valign="middle",
            text_size=(None, None),
            size_hint_y=None,
            height=dp(24),
        ))
        content.children[-1].bind(
            width=lambda s, w: setattr(s, 'text_size', (w - dp(8), None))
        )

        self._exp_input = TextInput(
            hint_text="Numero de expediente",
            multiline=False,
            font_size=sp(14),
            size_hint_y=None,
            height=dp(44),
            padding=[dp(10), dp(8)],
            background_normal="",
            background_active="",
            background_color=C_BG,
            cursor_color=C_PRIMARY,
            foreground_color=C_TEXT,
            hint_text_color=C_TEXT_SEC,
        )
        content.add_widget(self._exp_input)

        content.add_widget(Label(
            text="Edad:",
            font_size=sp(13),
            color=C_TEXT,
            halign="left",
            valign="middle",
            text_size=(None, None),
            size_hint_y=None,
            height=dp(24),
        ))
        content.children[-1].bind(
            width=lambda s, w: setattr(s, 'text_size', (w - dp(8), None))
        )

        self._edad_input = TextInput(
            hint_text="Edad en anios",
            multiline=False,
            input_filter="int",
            font_size=sp(14),
            size_hint_y=None,
            height=dp(44),
            padding=[dp(10), dp(8)],
            background_normal="",
            background_active="",
            background_color=C_BG,
            cursor_color=C_PRIMARY,
            foreground_color=C_TEXT,
            hint_text_color=C_TEXT_SEC,
        )
        content.add_widget(self._edad_input)

        content.add_widget(Label(
            text="Sexo:",
            font_size=sp(13),
            color=C_TEXT,
            halign="left",
            valign="middle",
            text_size=(None, None),
            size_hint_y=None,
            height=dp(24),
        ))
        content.children[-1].bind(
            width=lambda s, w: setattr(s, 'text_size', (w - dp(8), None))
        )

        self._sexo_spinner = Spinner(
            text="Masculino",
            values=["Masculino", "Femenino"],
            font_size=sp(14),
            size_hint_y=None,
            height=dp(44),
            background_normal="",
            background_color=C_BG,
            color=C_TEXT,
        )
        content.add_widget(self._sexo_spinner)

        content.add_widget(BoxLayout(size_hint_y=None, height=dp(10)))

        save_btn = Button(
            text="Guardar paciente",
            size_hint_y=None,
            height=dp(50),
            font_size=sp(16),
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
            color=get_color_from_hex("#F44336"),
            halign="center",
            size_hint_y=None,
            height=dp(30),
        )
        content.add_widget(self._msg_label)

        sv.add_widget(content)
        root.add_widget(sv)
        self.add_widget(root)

    def on_enter(self):
        if self._editing_id is None:
            self._exp_input.text = ""
            self._edad_input.text = ""
            self._sexo_spinner.text = "Masculino"
            self._msg_label.text = ""

    def set_editing(self, paciente_id):
        from frontend.database import obtener_paciente
        p = obtener_paciente(paciente_id)
        if p:
            self._editing_id = p["id"]
            self._exp_input.text = p["expediente"]
            self._edad_input.text = str(p["edad"])
            self._sexo_spinner.text = "Masculino" if p["sexo"] == "M" else "Femenino"

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
        back.bind(on_press=lambda _: navigate_to("patient_list"))
        header.add_widget(back)

        header.add_widget(Label(
            text="Paciente",
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
        expediente = self._exp_input.text.strip()
        edad = self._edad_input.text.strip()
        sexo = "M" if self._sexo_spinner.text == "Masculino" else "F"

        if not expediente:
            self._msg_label.text = "Ingresa el numero de expediente"
            return
        if not edad:
            self._msg_label.text = "Ingresa la edad"
            return

        from frontend.database import crear_paciente, editar_paciente

        try:
            if self._editing_id:
                editar_paciente(self._editing_id, expediente, int(edad), sexo)
            else:
                crear_paciente(expediente, int(edad), sexo)
        except Exception as e:
            self._msg_label.text = f"Error: {str(e)}"
            return

        navigate_to("patient_list")
