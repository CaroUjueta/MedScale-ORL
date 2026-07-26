from frontend.screens.base import ScaleScreen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.utils import get_color_from_hex
from kivy.metrics import dp, sp

C_PRIMARY = get_color_from_hex("#1976D2")
C_TEXT_SEC = get_color_from_hex("#6B7280")

OPTS = ["Ninguna (0)", "Parcial (1)", "Total (2)"]
VALS = [0, 1, 2]

STRUCTURES = [
    "Seno maxilar",
    "Etmoides anterior",
    "Etmoides posterior",
    "Seno esfenoidal",
    "Seno frontal",
    "Complejo ostiomeatal",
]


class LundMackayScreen(ScaleScreen):
    title_text = "Lund Mackay"
    result_prefix = "Total:"
    scale_name = "Lund Mackay"

    def _build_form(self, layout):
        self._section(layout, "TAC: 0=ninguna, 1=parcial, 2=total")

        pair = BoxLayout(
            orientation="horizontal",
            size_hint_y=None,
            spacing=dp(6),
        )

        left_col = BoxLayout(
            orientation="vertical",
            size_hint_x=0.5,
            size_hint_y=None,
            spacing=dp(4),
        )
        left_col.bind(minimum_height=left_col.setter("height"))

        right_col = BoxLayout(
            orientation="vertical",
            size_hint_x=0.5,
            size_hint_y=None,
            spacing=dp(4),
        )
        right_col.bind(minimum_height=right_col.setter("height"))

        hdr_left = Label(
            text="-- Izquierdo --",
            font_size=sp(12),
            bold=True,
            color=C_PRIMARY,
            halign="center",
            valign="middle",
            size_hint_y=None,
            height=dp(28),
        )
        left_col.add_widget(hdr_left)

        hdr_right = Label(
            text="-- Derecho --",
            font_size=sp(12),
            bold=True,
            color=C_PRIMARY,
            halign="center",
            valign="middle",
            size_hint_y=None,
            height=dp(28),
        )
        right_col.add_widget(hdr_right)

        self._cards_l = []
        for q in STRUCTURES:
            self._cards_l.append(self._question_card(q, OPTS, VALS))
            left_col.add_widget(self._cards_l[-1])

        self._cards_r = []
        for q in STRUCTURES:
            self._cards_r.append(self._question_card(q, OPTS, VALS))
            right_col.add_widget(self._cards_r[-1])

        self._sub_left = Label(
            text="Subtotal: 0", font_size="13sp", bold=True, color=C_PRIMARY,
            halign="center", valign="middle", size_hint_y=None, height=dp(28),
        )
        left_col.add_widget(self._sub_left)

        self._sub_right = Label(
            text="Subtotal: 0", font_size="13sp", bold=True, color=C_PRIMARY,
            halign="center", valign="middle", size_hint_y=None, height=dp(28),
        )
        right_col.add_widget(self._sub_right)

        pair.add_widget(left_col)
        pair.add_widget(right_col)

        def _sync_height(*_):
            pair.height = max(left_col.minimum_height, right_col.minimum_height)
        left_col.bind(minimum_height=_sync_height)
        right_col.bind(minimum_height=_sync_height)

        layout.add_widget(pair)

        self._calc_btn(layout, self._calc)
        self._result_box(layout)

    def _calc(self, _):
        left = sum(c._option_state["score"] for c in self._cards_l)
        right = sum(c._option_state["score"] for c in self._cards_r)
        self._sub_left.text = f"Subtotal: {left}"
        self._sub_right.text = f"Subtotal: {right}"
        self._show_result(left + right)

    def _get_responses(self):
        resp = {}
        for i,结构 in enumerate(STRUCTURES):
            resp[f"Izq - {结构}"] = self._cards_l[i]._option_state["selected"]
            resp[f"Der - {结构}"] = self._cards_r[i]._option_state["selected"]
        return resp
