from frontend.screens.base import ScaleScreen

OPTS = [
    "Ausente (0)",
    "Leve (1)",
    "Moderado (2)",
    "Severo (3)",
]
VALS = [0, 1, 2, 3]

QS = [
    "G - Grado de disfonia",
    "R - Aspereza",
    "B - Soplosidad",
    "A - Astenia (voz debil)",
    "S - Tension (voz forzada)",
]


def _interpretar_grbas(puntaje):
    if puntaje == 0:
        return "Voz normal"
    elif puntaje <= 6:
        return "Alteracion leve"
    elif puntaje <= 11:
        return "Alteracion moderada"
    else:
        return "Alteracion severa"


class GrbasScreen(ScaleScreen):
    title_text = "GRBAS"
    result_prefix = "GRBAS:"
    scale_name = "GRBAS"
    _questions = QS

    def _build_form(self, layout):
        self._section(layout, "Evaluacion perceptiva de la voz:")
        self._cards = []
        for q in QS:
            self._cards.append(self._question(layout, q, OPTS, VALS))
        self._calc_btn(layout, self._calc)
        self._result_box(layout)

    def _calc(self, _):
        total = sum(c._option_state["score"] for c in self._cards)
        interp = _interpretar_grbas(total)
        per = "  ".join(str(c._option_state["score"]) for c in self._cards)
        self._result_lbl.text = f"{self.result_prefix} {total}\nG-R-B-A-S: {per}\n{interp}"