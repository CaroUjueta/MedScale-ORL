from frontend.screens.base import ScaleScreen
from kivy.uix.label import Label
from kivy.utils import get_color_from_hex

C_PRIMARY = get_color_from_hex("#1976D2")

OPTS = ["Ninguna (0)", "Parcial (1)", "Total (2)"]
VALS = [0, 1, 2]

LEFT = [
    "Seno maxilar (izq)",
    "Etmoides anterior (izq)",
    "Etmoides posterior (izq)",
    "Seno esfenoidal (izq)",
    "Seno frontal (izq)",
    "Complejo ostiomeatal (izq)",
]

RIGHT = [
    "Seno maxilar (der)",
    "Etmoides anterior (der)",
    "Etmoides posterior (der)",
    "Seno esfenoidal (der)",
    "Seno frontal (der)",
    "Complejo ostiomeatal (der)",
]


class LundMackayScreen(ScaleScreen):
    title_text = "Lund Mackay"
    result_prefix = "Total:"

    def _build_form(self, layout):
        self._section(layout, "TAC: 0=ninguna, 1=parcial, 2=total")

        self._section(layout, "-- Lado izquierdo --")
        self._cards_l = []
        for q in LEFT:
            self._cards_l.append(self._question(layout, q, OPTS, VALS))

        self._section(layout, "-- Lado derecho --")
        self._cards_r = []
        for q in RIGHT:
            self._cards_r.append(self._question(layout, q, OPTS, VALS))

        self._calc_btn(layout, self._calc)

        self._sub_left = Label(
            text="", font_size="14sp", bold=True, color=C_PRIMARY,
            size_hint_y=None, height=28,
        )
        layout.add_widget(self._sub_left)
        self._sub_right = Label(
            text="", font_size="14sp", bold=True, color=C_PRIMARY,
            size_hint_y=None, height=28,
        )
        layout.add_widget(self._sub_right)
        self._result_box(layout)

    def _calc(self, _):
        left = sum(c._option_state["score"] for c in self._cards_l)
        right = sum(c._option_state["score"] for c in self._cards_r)
        self._sub_left.text = f"Izquierdo: {left}"
        self._sub_right.text = f"Derecho: {right}"
        self._show_result(left + right)
