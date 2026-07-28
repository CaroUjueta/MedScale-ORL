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


class Etdq7Screen(ScaleScreen):
    title_text = "ETDQ-7"
    result_prefix = "Puntaje total:"

    def _build_form(self, layout):
        self._section(layout, "Durante el último mes, en qué grado le han afectado:")

        self._states_l = []
        self._states_r = []

        for q in QS:
            state_l, state_r = self._add_question(layout, q)
            self._states_l.append(state_l)
            self._states_r.append(state_r)

        self._calc_btn(layout, self._calc)

        self._sub_pair = BoxLayout(
            orientation="horizontal",
            size_hint_y=None,
            height=dp(28),
            spacing=dp(6),
        )
        self._sub_left = Label(
            text="Izquierdo: 0/7", font_size="12sp", bold=True, color=C_PRIMARY,
            halign="center", valign="middle", size_hint_x=0.5,
        )
        self._sub_pair.add_widget(self._sub_left)
        self._sub_right = Label(
            text="Derecho: 0/7", font_size="12sp", bold=True, color=C_PRIMARY,
            halign="center", valign="middle", size_hint_x=0.5,
        )
        self._sub_pair.add_widget(self._sub_right)
        layout.add_widget(self._sub_pair)

        self._result_box(layout)

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
        self._sub_left.text = f"Izquierdo: {left}/7"
        self._sub_right.text = f"Derecho: {right}/7"
        total = left + right
        self._result_lbl.text = f"{self.result_prefix} {total}"
