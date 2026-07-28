from frontend.screens.base import ScaleScreen

OPTS = ["0", "1", "2", "3", "4", "5"]
VALS = [0, 1, 2, 3, 4, 5]

QS = [
    "1. Necesidad de sonarse la nariz",
    "2. Estornudos",
    "3. Mucosidad nasal continua",
    "4. Tos",
    "5. Cae secreción por atrás hacia la garganta",
    "6. Secreción nasal espesa",
    "7. Sensación de oído tapado",
    "8. Mareos",
    "9. Dolor de oídos",
    "10. Presión o dolor en la cara",
    "11. Dificultad para quedarse dormido(a)",
    "12. Se despierta durante la noche",
    "13. Sensación de que durmió mal",
    "14. Despertar cansado(a)",
    "15. Fatiga o cansancio",
    "16. Productividad o rendimiento reducida",
    "17. Menor o poca concentración",
    "18. Frustración / cansancio / irritabilidad",
    "19. Tristeza",
    "20. Sentirse avergonzado(a)",
    "21. Obstrucción nasal",
    "22. Pérdida del sentido del olfato y gusto",
]


class Snot22Screen(ScaleScreen):
    title_text = "SNOT-22"
    result_prefix = "SNOT-22:"

    def _build_form(self, layout):
        self._section(layout, "0 = nada, 5 = peor problema:")
        self._cards = []
        for q in QS:
            self._cards.append(self._question(layout, q, OPTS, VALS))
        self._calc_btn(layout, self._calc)
        self._result_box(layout)

    def _calc(self, _):
        self._show_result(sum(c._option_state["score"] for c in self._cards))
