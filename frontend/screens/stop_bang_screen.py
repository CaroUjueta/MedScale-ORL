from frontend.screens.base import ScaleScreen

OPTS = ["No (0)", "Si (1)"]
VALS = [0, 1]

QS = [
    "S - Ronca fuerte y frecuentemente",
    "T - Se siente cansado/a de dia",
    "O - Alguien observa que deja de respirar",
    "P - Diagnostico de presion arterial alta",
    "B - IMC mayor a 35 kg/m2",
    "A - Edad mayor a 50 anios",
    "N - Cuello mayor a 40 cm",
    "G - Genero masculino",
]


class StopBangScreen(ScaleScreen):
    title_text = "STOP-BANG"
    result_prefix = "STOP-BANG:"

    def _build_form(self, layout):
        self._section(layout, "Responda Si o No:")
        self._cards = []
        for q in QS:
            self._cards.append(self._question(layout, q, OPTS, VALS))
        self._calc_btn(layout, self._calc)
        self._result_box(layout)

    def _calc(self, _):
        self._show_result(sum(c._option_state["score"] for c in self._cards))
