from frontend.screens.base import ScaleScreen

OPTS = [
    "Normal (0)",
    "Leve (1)",
    "Moderado (2)",
    "Severo/Extremo (3)",
]
VALS = [0, 1, 2, 3]

QS = [
    "G - Grado: grado global de la alteracion vocal o disfonia",
    "R - Ronquera: importancia de la ronquera y aspereza",
    "A - Astenia: grado de astenia o fatiga vocal",
    "B - Soplosidad: voz aerea, caracter soplado o velado",
    "S - Tension: grado de tension, constrenimiento o dureza",
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
        self._result_lbl.text = f"{self.result_prefix} {total}\nG-R-A-B-S: {per}\n{interp}"