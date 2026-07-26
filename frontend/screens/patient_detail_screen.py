import json
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.button import Button
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
C_RESULT_BG = get_color_from_hex("#E0F2F1")
C_RESULT = get_color_from_hex("#0D6E6E")


def navigate_to(name):
    App.get_running_app().root.current = name


class PatientDetailScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._paciente_id = None
        root = BoxLayout(orientation="vertical")
        root.add_widget(self._build_header())
        self._content = BoxLayout(orientation="vertical")
        root.add_widget(self._content)
        self.add_widget(root)

    def set_paciente_id(self, pid):
        self._paciente_id = pid

    def on_enter(self):
        if self._paciente_id:
            self._refresh()

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

        self._header_title = Label(
            text="Paciente",
            font_size=sp(16),
            bold=True,
            color=get_color_from_hex("#FFFFFF"),
            halign="left",
            valign="middle",
            text_size=(None, None),
            size_hint_x=1,
        )
        self._header_title.bind(
            width=lambda s, w: setattr(s, 'text_size', (w - dp(12), None))
        )
        header.add_widget(self._header_title)
        return header

    def _refresh(self):
        from frontend.database import obtener_paciente, obtener_evaluaciones, eliminar_paciente, eliminar_evaluacion

        self._content.clear_widgets()
        paciente = obtener_paciente(self._paciente_id)
        if not paciente:
            self._content.add_widget(Label(
                text="Paciente no encontrado",
                font_size=sp(14),
                color=C_TEXT_SEC,
            ))
            return

        self._header_title.text = f"Exp: {paciente['expediente']}"

        info_box = BoxLayout(
            orientation="vertical",
            size_hint_y=None,
            height=dp(100),
            padding=[dp(16), dp(10)],
            spacing=dp(2),
        )
        with info_box.canvas.before:
            from kivy.graphics import Color, RoundedRectangle
            Color(*C_CARD)
            info_box._bg = RoundedRectangle(
                pos=info_box.pos, size=info_box.size, radius=[dp(10)]
            )
        info_box.bind(pos=lambda s, p: setattr(info_box._bg, 'pos', p))
        info_box.bind(size=lambda s, sz: setattr(info_box._bg, 'size', sz))

        sexo_txt = "Masculino" if paciente["sexo"] == "M" else "Femenino"
        info_box.add_widget(Label(
            text=f"Expediente: {paciente['expediente']}",
            font_size=sp(14),
            bold=True,
            color=C_TEXT,
            halign="left",
            text_size=(None, None),
            size_hint_y=0.33,
        ))
        info_box.children[-1].bind(
            width=lambda s, w: setattr(s, 'text_size', (w - dp(8), None))
        )
        info_box.add_widget(Label(
            text=f"Edad: {paciente['edad']} anios  |  Sexo: {sexo_txt}",
            font_size=sp(12),
            color=C_TEXT_SEC,
            halign="left",
            text_size=(None, None),
            size_hint_y=0.33,
        ))
        info_box.children[-1].bind(
            width=lambda s, w: setattr(s, 'text_size', (w - dp(8), None))
        )

        btn_row = BoxLayout(
            size_hint_y=0.33,
            spacing=dp(8),
        )
        edit_btn = Button(
            text="Editar",
            font_size=sp(12),
            background_normal="",
            background_color=C_PRIMARY,
            color=get_color_from_hex("#FFFFFF"),
        )
        edit_btn.bind(on_press=lambda _: self._edit_patient())
        btn_row.add_widget(edit_btn)

        delete_btn = Button(
            text="Eliminar",
            font_size=sp(12),
            background_normal="",
            background_color=get_color_from_hex("#F44336"),
            color=get_color_from_hex("#FFFFFF"),
        )
        delete_btn.bind(on_press=lambda _: self._confirm_delete_patient())
        btn_row.add_widget(delete_btn)

        send_btn = Button(
            text="Enviar por correo",
            font_size=sp(12),
            background_normal="",
            background_color=C_ACCENT,
            color=get_color_from_hex("#FFFFFF"),
        )
        send_btn.bind(on_press=lambda _: self._send_email())
        btn_row.add_widget(send_btn)

        info_box.add_widget(btn_row)
        self._content.add_widget(info_box)

        evaluaciones = obtener_evaluaciones(self._paciente_id)

        hdr = BoxLayout(
            size_hint_y=None,
            height=dp(36),
            padding=[dp(16), 0],
        )
        with hdr.canvas.before:
            from kivy.graphics import Color, Rectangle
            Color(*C_BG)
            hdr._bg = Rectangle(pos=hdr.pos, size=hdr.size)
        hdr.bind(pos=lambda s, p: setattr(hdr._bg, 'pos', p))
        hdr.bind(size=lambda s, sz: setattr(hdr._bg, 'size', sz))
        hdr.add_widget(Label(
            text=f"EVALUACIONES ({len(evaluaciones)})",
            font_size=sp(11),
            bold=True,
            color=C_TEXT_SEC,
            halign="left",
            text_size=(None, None),
        ))
        hdr.children[-1].bind(
            width=lambda s, w: setattr(s, 'text_size', (w - dp(16), None))
        )
        self._content.add_widget(hdr)

        scroll = ScrollView(bar_width=dp(3), bar_color=C_DIVIDER)
        ev_list = BoxLayout(
            orientation="vertical",
            size_hint_y=None,
            spacing=dp(6),
            padding=[dp(16), dp(8)],
        )

        if not evaluaciones:
            ev_list.add_widget(Label(
                text="No hay evaluaciones registradas",
                font_size=sp(13),
                color=C_TEXT_SEC,
                halign="center",
                size_hint_y=None,
                height=dp(50),
            ))
        else:
            for ev in evaluaciones:
                card = BoxLayout(
                    orientation="vertical",
                    size_hint_y=None,
                    height=dp(90),
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

                fecha_corta = ev["fecha"][:16].replace("T", " ")
                card.add_widget(Label(
                    text=f"{ev['tipo_escala']}  -  {ev['puntaje']}",
                    font_size=sp(14),
                    bold=True,
                    color=C_RESULT,
                    halign="left",
                    text_size=(None, None),
                    size_hint_y=0.4,
                ))
                card.children[-1].bind(
                    width=lambda s, w: setattr(s, 'text_size', (w - dp(8), None))
                )
                card.add_widget(Label(
                    text=fecha_corta,
                    font_size=sp(11),
                    color=C_TEXT_SEC,
                    halign="left",
                    text_size=(None, None),
                    size_hint_y=0.3,
                ))
                card.children[-1].bind(
                    width=lambda s, w: setattr(s, 'text_size', (w - dp(8), None))
                )

                del_btn = Button(
                    text="Eliminar",
                    size_hint=(None, None),
                    size=(dp(70), dp(24)),
                    font_size=sp(10),
                    background_normal="",
                    background_color=get_color_from_hex("#FFCDD2"),
                    color=get_color_from_hex("#C62828"),
                )
                del_btn.bind(
                    on_press=lambda _, eid=ev["id"]: self._delete_eval(eid)
                )
                card.add_widget(del_btn)

                ev_list.add_widget(card)

        ev_list.bind(minimum_height=ev_list.setter("height"))
        scroll.add_widget(ev_list)
        self._content.add_widget(scroll)

    def _edit_patient(self):
        form = self.manager.get_screen("patient_form")
        form.set_editing(self._paciente_id)
        navigate_to("patient_form")

    def _confirm_delete_patient(self):
        content = BoxLayout(
            orientation="vertical",
            padding=dp(16),
            spacing=dp(12),
        )
        content.add_widget(Label(
            text="Eliminar paciente y todas sus evaluaciones?",
            font_size=sp(14),
            color=C_TEXT,
            halign="center",
        ))
        btn_row = BoxLayout(spacing=dp(8), size_hint_y=None, height=dp(44))
        cancel = Button(
            text="Cancelar",
            font_size=sp(13),
            background_normal="",
            background_color=C_DIVIDER,
            color=C_TEXT,
        )
        confirm = Button(
            text="Eliminar",
            font_size=sp(13),
            background_normal="",
            background_color=get_color_from_hex("#F44336"),
            color=get_color_from_hex("#FFFFFF"),
        )
        btn_row.add_widget(cancel)
        btn_row.add_widget(confirm)
        content.add_widget(btn_row)

        popup = Popup(
            title="Confirmar",
            content=content,
            size_hint=(0.8, 0.3),
            auto_dismiss=False,
        )
        cancel.bind(on_press=popup.dismiss)
        confirm.bind(
            on_press=lambda _: (
                __import__("frontend.database", fromlist=["eliminar_paciente"]).eliminar_paciente(self._paciente_id),
                popup.dismiss(),
                navigate_to("patient_list"),
            )
        )
        popup.open()

    def _delete_eval(self, eval_id):
        from frontend.database import eliminar_evaluacion
        eliminar_evaluacion(eval_id)
        self._refresh()

    def _send_email(self):
        from frontend.email_sender import enviar_correo, hay_internet

        if not hay_internet():
            self._show_popup_msg("Sin conexion a internet. Intenta mas tarde.")
            return

        self._show_popup_msg("Enviando correo...")

        def on_result(ok, msg):
            from kivy.clock import Clock
            Clock.schedule_once(lambda dt: self._show_popup_msg(msg), 0)

        enviar_correo(self._paciente_id, callback=on_result)

    def _show_popup_msg(self, msg):
        content = BoxLayout(padding=dp(16))
        content.add_widget(Label(
            text=msg,
            font_size=sp(13),
            color=C_TEXT,
            halign="center",
        ))
        popup = Popup(
            title="Correo",
            content=content,
            size_hint=(0.8, 0.3),
            auto_dismiss=True,
        )
        popup.open()
