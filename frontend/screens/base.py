from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.image import Image as KivyImage
from kivy.uix.popup import Popup
from kivy.uix.widget import Widget
from kivy.utils import get_color_from_hex
from kivy.app import App
from kivy.metrics import dp, sp
from kivy.core.window import Window
from kivy.clock import Clock

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

_chk_tex_on = None
_chk_tex_off = None


def _render_chk_textures():
    global _chk_tex_on, _chk_tex_off
    if _chk_tex_on is not None:
        return
    from kivy.graphics import Fbo, Color, ClearBuffers, ClearColor, RoundedRectangle, Line
    sz = 64
    pad = 8
    rad = 10
    for selected in (False, True):
        fbo = Fbo(size=(sz, sz))
        fbo.add(ClearColor(0, 0, 0, 0))
        fbo.add(ClearBuffers())
        with fbo:
            if selected:
                Color(*C_ACCENT)
                RoundedRectangle(pos=(pad, pad), size=(sz - pad*2, sz - pad*2), radius=[rad])
                Color(1, 1, 1, 1)
                Line(points=[
                    sz*0.27, sz*0.52,
                    sz*0.40, sz*0.38,
                    sz*0.72, sz*0.70,
                ], width=3, cap="round", joint="round")
            else:
                Color(*C_DIVIDER)
                Line(rounded_rectangle=(pad, pad, sz - pad*2, sz - pad*2, rad), width=2)
        fbo.draw()
        if selected:
            _chk_tex_on = fbo.texture
        else:
            _chk_tex_off = fbo.texture


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

    def on_enter(self):
        from frontend.database import registrar_uso_escala
        from frontend.scales import escala_id_por_nombre

        scale_name = getattr(self, "scale_name", self.__class__.__name__)
        registrar_uso_escala(escala_id_por_nombre(scale_name) or scale_name)

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
        card = self._question_card(text, options, values)
        layout.add_widget(card)
        return card

    def _question_card(self, text, options, values=None):
        if values is None:
            values = list(range(len(options)))

        _render_chk_textures()

        num_opts = len(options)
        card_h = dp(54) + dp(34) * num_opts

        card = BoxLayout(
            orientation="vertical",
            size_hint_y=None,
            height=card_h,
            padding=[dp(12), dp(8)],
            spacing=dp(2),
        )
        with card.canvas.before:
            from kivy.graphics import Color, RoundedRectangle
            Color(*C_CARD)
            card._bg = RoundedRectangle(
                pos=card.pos, size=card.size, radius=[dp(10)]
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
            size_hint_y=None,
            height=dp(38),
        )
        lbl.bind(width=lambda s, w: setattr(s, 'text_size', (w - dp(8), None)))
        card.add_widget(lbl)

        state = {"score": values[0], "selected": 0}
        card._option_state = state

        chk_widgets = []
        lbl_widgets = []

        def _draw_cb(img, is_selected):
            img.texture = _chk_tex_on if is_selected else _chk_tex_off

        def _select(idx):
            state["score"] = values[idx]
            state["selected"] = idx
            for j in range(len(chk_widgets)):
                is_sel = (j == idx)
                _draw_cb(chk_widgets[j], is_sel)
                lbl_widgets[j].color = C_ACCENT if is_sel else C_TEXT
                lbl_widgets[j].bold = is_sel

        row_widgets = []
        for i, (opt_text, val) in enumerate(zip(options, values)):
            row = BoxLayout(
                size_hint_y=None,
                height=dp(32),
                spacing=dp(8),
                padding=[dp(4), 0],
            )

            chk_img = KivyImage(
                size_hint_x=None,
                size=(dp(24), dp(24)),
                allow_stretch=True,
                texture=_chk_tex_off,
            )

            opt_lbl = Label(
                text=opt_text,
                font_size=sp(12),
                color=C_TEXT,
                halign="left",
                valign="middle",
                text_size=(None, None),
                bold=False,
                size_hint_x=1,
            )
            opt_lbl.bind(width=lambda s, w: setattr(s, 'text_size', (w - dp(8), None)))

            row.add_widget(chk_img)
            row.add_widget(opt_lbl)
            chk_widgets.append(chk_img)
            lbl_widgets.append(opt_lbl)
            row_widgets.append(row)
            card.add_widget(row)

        def _on_card_touch(card_widget, touch):
            if not card_widget.collide_point(*touch.pos):
                return False
            for idx, row in enumerate(row_widgets):
                if row.collide_point(*touch.pos):
                    _select(idx)
                    return True
            return False

        card.bind(on_touch_down=_on_card_touch)

        def _init_checkboxes(_dt):
            _select(0)

        from kivy.clock import Clock
        Clock.schedule_once(_init_checkboxes)

        return card

    def _numeric_input(self, layout, text, hint, card_height=None):
        card = BoxLayout(
            orientation="vertical",
            size_hint_y=None,
            height=card_height or dp(70),
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
        row = BoxLayout(
            size_hint_y=None,
            height=dp(28),
            spacing=dp(8),
            padding=[dp(4), 0],
        )
        lbl = Label(
            text=text,
            font_size=sp(11),
            bold=False,
            color=C_TEXT_SEC,
            size_hint_x=1,
            halign="left",
            valign="middle",
            text_size=(None, None),
        )
        lbl.bind(width=lambda s, w: setattr(s, 'text_size', (w - dp(8), None)))
        row.add_widget(lbl)
        layout.add_widget(row)

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

        self._last_puntaje = None
        self._save_btn_widget = Button(
            text="Guardar resultado",
            size_hint_y=None,
            height=dp(46),
            font_size=sp(14),
            bold=True,
            background_normal="",
            background_color=C_ACCENT,
            color=get_color_from_hex("#FFFFFF"),
        )
        self._save_btn_widget.bind(on_press=lambda _: self._show_save_popup())
        self._save_btn_widget.opacity = 0
        self._save_btn_widget.disabled = True
        layout.add_widget(self._save_btn_widget)

    def _show_result(self, value):
        self._result_lbl.text = f"{self.result_prefix} {value}"
        self._last_puntaje = value
        self._save_btn_widget.opacity = 1
        self._save_btn_widget.disabled = False

    def _get_responses(self):
        if not hasattr(self, "_cards"):
            return {}
        questions = getattr(self, "_questions", []) or []
        resp = {}
        for i, card in enumerate(self._cards):
            q = questions[i] if i < len(questions) else f"Pregunta {i+1}"
            resp[q] = card._option_state["selected"]
        return resp

    def _show_save_popup(self):
        from frontend.database import obtener_pacientes

        pacientes = obtener_pacientes()
        content = BoxLayout(orientation="vertical", padding=dp(12), spacing=dp(8))

        content.add_widget(Label(
            text="Seleccionar paciente:",
            font_size=sp(14),
            bold=True,
            color=C_TEXT,
            size_hint_y=None,
            height=dp(30),
        ))

        scroll = ScrollView(bar_width=dp(3))
        btn_list = BoxLayout(
            orientation="vertical",
            size_hint_y=None,
            spacing=dp(4),
        )

        if not pacientes:
            btn_list.add_widget(Label(
                text="No hay pacientes registrados.\nCrea uno primero desde 'Mis Pacientes'.",
                font_size=sp(12),
                color=C_TEXT_SEC,
                halign="center",
                size_hint_y=None,
                height=dp(50),
            ))
        else:
            for p in pacientes:
                sexo_txt = "M" if p["sexo"] == "M" else "F"
                btn = Button(
                    text=f"{p['expediente']}  |  {p['edad']} anios  |  {sexo_txt}",
                    size_hint_y=None,
                    height=dp(44),
                    font_size=sp(13),
                    background_normal="",
                    background_color=C_CARD,
                    color=C_TEXT,
                )
                btn.bind(
                    on_press=lambda _, pid=p["id"]: self._save_for_patient(pid)
                )
                btn_list.add_widget(btn)

        btn_list.bind(minimum_height=btn_list.setter("height"))
        scroll.add_widget(btn_list)
        content.add_widget(scroll)

        close_btn = Button(
            text="Cancelar",
            size_hint_y=None,
            height=dp(42),
            font_size=sp(13),
            background_normal="",
            background_color=C_DIVIDER,
            color=C_TEXT,
        )
        content.add_widget(close_btn)

        self._save_popup = Popup(
            title="Guardar evaluacion",
            content=content,
            size_hint=(0.85, 0.6),
            auto_dismiss=False,
        )
        close_btn.bind(on_press=self._save_popup.dismiss)
        self._save_popup.open()

    def _save_for_patient(self, paciente_id):
        from frontend.database import guardar_evaluacion

        if self._last_puntaje is None:
            return

        respuestas = self._get_responses()
        scale_name = getattr(self, "scale_name", self.__class__.__name__)
        guardar_evaluacion(paciente_id, scale_name, respuestas, self._last_puntaje)

        if hasattr(self, "_save_popup") and self._save_popup:
            self._save_popup.dismiss()

        self._show_save_toast()

    def _show_save_toast(self):
        toast_box = BoxLayout(
            size_hint=(None, None),
            size=(dp(260), dp(44)),
            pos_hint={"center_x": 0.5, "top": 0.95},
        )
        with toast_box.canvas.before:
            from kivy.graphics import Color, RoundedRectangle
            Color(0.05, 0.43, 0.43, 0.95)
            toast_box._bg = RoundedRectangle(
                pos=toast_box.pos, size=toast_box.size, radius=[dp(8)]
            )
        toast_box.bind(pos=lambda s, p: setattr(s._bg, 'pos', p))
        toast_box.bind(size=lambda s, sz: setattr(s._bg, 'size', sz))

        toast_box.add_widget(Label(
            text="Evaluacion guardada",
            font_size=sp(13),
            bold=True,
            color=get_color_from_hex("#FFFFFF"),
        ))

        self.add_widget(toast_box)

        def _remove(_dt):
            self.remove_widget(toast_box)

        Clock.schedule_once(_remove, 2.0)
