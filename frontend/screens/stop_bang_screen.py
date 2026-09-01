from frontend.screens.base import ScaleScreen

QS = [
    {
        "text": "S - Ronca fuerte y frecuentemente (Snoring)",
        "opts": ["Si (1)", "No (0)"],
        "vals": [1, 0],
    },
    {
        "text": "T - Se siente cansado/a de día (Tired)",
        "opts": ["Si (1)", "No (0)"],
        "vals": [1, 0],
    },
    {
        "text": "O - Alguien observa que deja de respirar (Observed)",
        "opts": ["Si (1)", "No (0)"],
        "vals": [1, 0],
    },
    {
        "text": "P - Diagnóstico de presión arterial alta (Pressure)",
        "opts": ["Si (1)", "No (0)"],
        "vals": [1, 0],
    },
    {
        "text": "B - Índice de masa corporal (BMI)",
        "opts": [">35 kg/m² (1)", "≤35 kg/m² (0)"],
        "vals": [1, 0],
    },
    {
        "text": "A - Edad (Age)",
        "opts": [">50 años (1)", "≤50 años (0)"],
        "vals": [1, 0],
    },
    {
        "text": "N - Circunferencia del cuello (Neck circumference)",
        "opts": [">40 cm (1)", "≤40 cm (0)"],
        "vals": [1, 0],
    },
    {
        "text": "G - Género (Gender)",
        "opts": ["Masculino (1)", "Femenino (0)"],
        "vals": [1, 0],
    },
]


def _interpretar_stop_bang(puntaje):
    if puntaje <= 2:
        return "Bajo riesgo de apnea\nobstructiva del sueno"
    elif puntaje <= 4:
        return "Riesgo intermedio de apnea\nobstructiva del sueno"
    else:
        return "Alto riesgo de apnea\nobstructiva del sueno"


class StopBangScreen(ScaleScreen):
    title_text = "STOP-BANG"
    result_prefix = "STOP-BANG:"
    scale_name = "STOP-BANG"
    _questions = QS

    def _build_form(self, layout):
        self._section(layout, "Responda según cada criterio:")
        self._cards = []
        for q in QS:
            self._cards.append(
                self._question(layout, q["text"], q["opts"], q["vals"])
            )
        self._calc_btn(layout, self._calc)
        self._result_box(layout)

    def _calc(self, _):
        total = sum(c._option_state["score"] for c in self._cards)
        interp = _interpretar_stop_bang(total)
        self._result_lbl.text = f"{self.result_prefix} {total}\n{interp}"
        self._last_puntaje = total
        self._save_btn_widget.opacity = 1
        self._save_btn_widget.disabled = False
