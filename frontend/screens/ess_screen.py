from frontend.screens.base import ScaleScreen

OPTS = [
    "Sin posibilidad de adormecerse (0)",
    "Ligera posibilidad de adormecerse (1)",
    "Posibilidad moderada de adormecerse (2)",
    "Posibilidad alta de adormecerse (3)",
]
VALS = [0, 1, 2, 3]

QS = [
    "1. Sentado/a y leyendo",
    "2. Viendo la television",
    "3. Sentado/a inactivo/a en un lugar publico",
    "4. Sentado/a 1h como pasajero/a en un coche",
    "5. Tumbado/a por la tarde para descansar",
    "6. Sentado/a y hablando con otra persona",
    "7. Sentado/a tranquilamente despues de comer",
    "8. Sentado/a en un coche, parado/a en un atasco",
]


class EssScreen(ScaleScreen):
    title_text = "Epworth (ESS)"
    result_prefix = "ESS:"

    def _build_form(self, layout):
        self._section(layout, "Probabilidad de quedarse dormido/a:")
        self._cards = []
        for q in QS:
            self._cards.append(self._question(layout, q, OPTS, VALS))
        self._calc_btn(layout, self._calc)
        self._result_box(layout)

    def _calc(self, _):
        self._show_result(sum(c._option_state["score"] for c in self._cards))
