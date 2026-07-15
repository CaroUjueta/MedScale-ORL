from frontend.screens.base import ScaleScreen

OPTS = ["1", "2", "3", "4", "5", "6", "7"]
VALS = [1, 2, 3, 4, 5, 6, 7]

QS = [
    "1. Dificultad para igualar presion (montana/avion)",
    "2. Oidos tapados con frecuencia",
    "3. Sensacion de presion en los oidos",
    "4. Dificultad para oir en lugares ruidosos",
    "5. Dolor de oido",
    "6. Sensacion de liquido en los oidos",
    "7. Zumbidos en los oidos",
]


class Etdq7Screen(ScaleScreen):
    title_text = "ETDQ-7"
    result_prefix = "ETDQ-7:"

    def _build_form(self, layout):
        self._section(layout, "1 = nunca, 7 = siempre:")
        self._cards = []
        for q in QS:
            self._cards.append(self._question(layout, q, OPTS, VALS))
        self._calc_btn(layout, self._calc)
        self._result_box(layout)

    def _calc(self, _):
        self._show_result(sum(c._option_state["score"] for c in self._cards))
