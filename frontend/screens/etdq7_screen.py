from frontend.screens import base as _base
from frontend.screens.base import ScaleScreen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.image import Image as KivyImage
from kivy.utils import get_color_from_hex
from kivy.metrics import dp, sp
from kivy.clock import Clock

C_PRIMARY = get_color_from_hex("#1976D2")
C_RESULT = get_color_from_hex("#0D6E6E")
C_RESULT_BG = get_color_from_hex("#E0F2F1")
C_RED = get_color_from_hex("#C62828")
C_RED_BG = get_color_from_hex("#FFEBEE")

OPTS = ["1", "2", "3", "4", "5", "6", "7"]
VALS = [1, 2, 3, 4, 5, 6, 7]

QS = [
    "1. ¿Presión en los oídos?",
    "2. ¿Dolor de oídos?",
    "3. ¿Sensación de oído tapado o de escuchar \"bajo el agua\"?",
    "4. ¿Problemas de oído asociados a resfríos o sinusitis?",
    "5. ¿Ruidos como crujidos o chasquidos en los oídos?",
    "6. ¿Zumbido en los oídos?",
    "7. ¿Sensación de audición débil o \"apagada\"?",
]


def _interpretar(promedio):
    if promedio < 2.0:
        return "Función tubárica normal\n(sin evidencia de disfunción)"
    elif promedio < 3.0:
        return "Leve disfunción de la\ntrompa de Eustaquio"
    elif promedio < 6.0:
        return "Moderada disfunción de la\ntrompa de Eustaquio"
    else:
        return "Severa disfunción de la\ntrompa de Eustaquio"


class Etdq7Screen(ScaleScreen):
    title_text = "ETDQ-7"

    def _build_form(self, layout):
        self._section(layout, "Durante el último mes, en qué grado le han afectado:")

        self._states_l = []
        self._states_r = []

        for q in QS:
            state_l, state_r = self._add_question(layout, q)
            self._states_l.append(state_l)
            self._states_r.append(state_r)

        self._calc_btn(layout, self._calc)

        self._results_pair = BoxLayout(
            orientation="horizontal",
            size_hint_y=None,
            height=dp(200),
            spacing=dp(8),
        )

        self._col_left = self._build_result_column("Oído Izquierdo", C_PRIMARY, C_RESULT_BG)
        self._col_right = self._build_result_column("Oído Derecho", C_PRIMARY, C_RESULT_BG, title_color=C_RED)

        self._results_pair.add_widget(self._col_left["box"])
        self._results_pair.add_widget(self._col_right["box"])

        layout.add_widget(self._results_pair)

    def _build_result_column(self, title, accent_color=None, bg_color=None, title_color=None):
        if accent_color is None:
            accent_color = C_PRIMARY
        if bg_color is None:
            bg_color = C_RESULT_BG
        if title_color is None:
            title_color = accent_color

        box = BoxLayout(
            orientation="vertical",
            size_hint_x=0.5,
            size_hint_y=None,
            height=dp(200),
            padding=[dp(12), dp(8)],
            spacing=dp(4),
        )
        with box.canvas.before:
            from kivy.graphics import Color, RoundedRectangle
            Color(*bg_color)
            box._bg = RoundedRectangle(
                pos=box.pos, size=box.size, radius=[dp(12)]
            )
        box.bind(pos=lambda s, p: setattr(box._bg, 'pos', p))
        box.bind(size=lambda s, sz: setattr(box._bg, 'size', sz))

        title_lbl = Label(
            text=title,
            font_size=sp(13),
            bold=True,
            color=title_color,
            halign="center",
            valign="middle",
            size_hint_y=None,
            height=dp(28),
        )
        box.add_widget(title_lbl)

        total_lbl = Label(
            text="Puntaje total: 0/49",
            font_size=sp(14),
            bold=True,
            color=_base.C_RESULT,
            halign="center",
            valign="middle",
            size_hint_y=None,
            height=dp(28),
        )
        box.add_widget(total_lbl)

        avg_lbl = Label(
            text="Promedio: 0.0/7",
            font_size=sp(12),
            color=_base.C_RESULT,
            halign="center",
            valign="middle",
            size_hint_y=None,
            height=dp(24),
        )
        box.add_widget(avg_lbl)

        interp_hdr = Label(
            text="Interpretación:",
            font_size=sp(11),
            bold=True,
            color=_base.C_TEXT_SEC,
            halign="center",
            valign="middle",
            size_hint_y=None,
            height=dp(20),
        )
        box.add_widget(interp_hdr)

        interp_lbl = Label(
            text="",
            font_size=sp(11),
            color=_base.C_TEXT,
            halign="center",
            valign="middle",
            size_hint_y=None,
            height=dp(48),
        )
        box.add_widget(interp_lbl)

        return {
            "box": box,
            "total": total_lbl,
            "avg": avg_lbl,
            "interp": interp_lbl,
        }

    def _add_question(self, layout, question_text):
        _base._render_chk_textures()

        card = BoxLayout(
            orientation="vertical",
            size_hint_y=None,
            height=dp(154),
            padding=[dp(12), dp(8)],
            spacing=dp(2),
        )
        with card.canvas.before:
            from kivy.graphics import Color, RoundedRectangle
            Color(*_base.C_CARD)
            card._bg = RoundedRectangle(
                pos=card.pos, size=card.size, radius=[dp(10)]
            )
        card.bind(pos=lambda s, p: setattr(card._bg, 'pos', p))
        card.bind(size=lambda s, sz: setattr(card._bg, 'size', sz))

        q_lbl = Label(
            text=question_text,
            font_size=sp(13),
            color=_base.C_TEXT,
            halign="left",
            valign="middle",
            text_size=(None, None),
            size_hint_y=None,
            height=dp(32),
        )
        q_lbl.bind(width=lambda s, w: setattr(s, 'text_size', (w - dp(8), None)))
        card.add_widget(q_lbl)

        state_l, chks_l, grid_l = self._make_grid(card, "Oído izquierdo")
        state_r, chks_r, grid_r = self._make_grid(card, "Oído derecho")

        def _on_touch(instance, touch):
            if not instance.collide_point(*touch.pos):
                return False
            for state, chks, grid in [
                (state_l, chks_l, grid_l),
                (state_r, chks_r, grid_r),
            ]:
                if not grid.collide_point(*touch.pos):
                    continue
                for idx in range(len(chks)):
                    if chks[idx].collide_point(*touch.pos):
                        for j in range(len(chks)):
                            chks[j].texture = (
                                _base._chk_tex_on if j == idx else _base._chk_tex_off
                            )
                        state["score"] = VALS[idx]
                        state["selected"] = idx
                        return True
            return False

        card.bind(on_touch_down=_on_touch)
        layout.add_widget(card)

        return state_l, state_r

    def _make_grid(self, card, ear_label):
        state = {"score": VALS[0], "selected": 0}

        ear_hdr = Label(
            text=ear_label,
            font_size=sp(10),
            bold=True,
            color=C_PRIMARY,
            halign="left",
            valign="middle",
            text_size=(None, None),
            size_hint_y=None,
            size_hint_x=1,
            height=dp(20),
        )
        ear_hdr.bind(width=lambda s, w: setattr(s, 'text_size', (w, None)))
        card.add_widget(ear_hdr)

        grid = GridLayout(
            cols=len(OPTS),
            rows=1,
            size_hint_y=None,
            height=dp(34),
            spacing=dp(0),
            padding=[dp(0), dp(3)],
        )

        chks = []

        for i in range(len(OPTS)):
            cell = BoxLayout(
                orientation="horizontal",
                spacing=dp(0),
                size_hint_x=None,
                width=dp(42),
            )

            chk = KivyImage(
                size_hint=(None, None),
                size=(dp(24), dp(24)),
                allow_stretch=True,
                texture=_base._chk_tex_off,
            )

            num = Label(
                text=OPTS[i],
                font_size=sp(11),
                color=_base.C_TEXT,
                halign="left",
                valign="middle",
                size_hint=(None, None),
                size=(dp(10), dp(24)),
            )

            cell.add_widget(chk)
            cell.add_widget(num)
            grid.add_widget(cell)
            chks.append(chk)

        card.add_widget(grid)

        def _init(_dt, _ch=chks):
            for j in range(len(_ch)):
                _ch[j].texture = (
                    _base._chk_tex_on if j == 0 else _base._chk_tex_off
                )

        Clock.schedule_once(_init)

        return state, chks, grid

    def _calc(self, _):
        left = sum(s["score"] for s in self._states_l)
        right = sum(s["score"] for s in self._states_r)

        avg_l = left / 7.0
        avg_r = right / 7.0

        self._col_left["total"].text = f"Puntaje total: {left}/49"
        self._col_left["avg"].text = f"Promedio: {avg_l:.1f}/7"
        self._col_left["interp"].text = _interpretar(avg_l)

        self._col_right["total"].text = f"Puntaje total: {right}/49"
        self._col_right["avg"].text = f"Promedio: {avg_r:.1f}/7"
        self._col_right["interp"].text = _interpretar(avg_r)
