from frontend.screens.base import ScaleScreen

OPTS = [
    "Nunca (0)",
    "Casi nunca (1)",
    "A veces (2)",
    "Casi siempre (3)",
    "Siempre (4)",
]
VALS = [0, 1, 2, 3, 4]

QS = [
    "1. La gente tiene dificultad para oirme por mi voz",
    "2. Siento que tengo que esforzarme para producir la voz",
    "3. Mi voz dificulta mi vida personal y social",
    "4. Me siento excluido/a de las conversaciones",
    "5. Me quedo sin aire cuando hablo",
    "6. Mi voz suena poco confiable",
    "7. La gente pregunta que tiene mi voz",
    "8. Me pongo tenso/a al hablar con otros por mi voz",
    "9. El sonido de mi voz varia durante el dia",
    "10. Mi problema de voz afecta mi trabajo o actividades",
]


def _interpretar_vhi10(puntaje):
    if puntaje <= 11:
        return "Discapacidad vocal minima\n(voz dentro de lo normal)"
    elif puntaje <= 21:
        return "Discapacidad vocal leve"
    elif puntaje <= 31:
        return "Discapacidad vocal moderada"
    else:
        return "Discapacidad vocal severa"


class Vhi10Screen(ScaleScreen):
    title_text = "VHI-10"
    result_prefix = "VHI-10:"
    scale_name = "VHI-10"
    _questions = QS

    def _build_form(self, layout):
        self._section(layout, "Indice de discapacidad vocal:")
        self._cards = []
        for q in QS:
            self._cards.append(self._question(layout, q, OPTS, VALS))
        self._calc_btn(layout, self._calc)
        self._result_box(layout)

    def _calc(self, _):
        total = sum(c._option_state["score"] for c in self._cards)
        interp = _interpretar_vhi10(total)
        self._result_lbl.text = f"{self.result_prefix} {total}\n{interp}"