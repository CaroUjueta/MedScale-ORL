from frontend.screens.base import ScaleScreen

OPTS = ["Nunca (0)", "Leve (1)", "Moderado (2)", "Alto (3)"]
VALS = [0, 1, 2, 3]

QS = [
    "1. Sentado/a, leyendo",
    "2. Viendo television",
    "3. Sentado/a inactivo/a en un lugar publico",
    "4. De pasajero/a en coche, sin parar 1h",
    "5. Acostado/a a descansar por la tarde",
    "6. Sentado/a, hablando con alguien",
    "7. Sentado/a tranquilamente despues de comer",
    "8. En coche, parado/a en el trafico",
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
