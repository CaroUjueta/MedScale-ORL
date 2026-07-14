from frontend.screens.base import ScaleScreen

OPTS = ["0", "1", "2", "3", "4", "5"]
VALS = [0, 1, 2, 3, 4, 5]

QS = [
    "1. Necesidad de sonarse",
    "2. Secrecion nasal",
    "3. Goteo postnasal por la garganta",
    "4. Tos",
    "5. Sensacion de secrecion en la garganta",
    "6. Oidos tapados",
    "7. Mareo",
    "8. Dolor/presion en los oidos",
    "9. Dolor/presion facial",
    "10. Dificultad para dormir",
    "11. Despertar durante la noche",
    "12. Falta de sueno reparador",
    "13. Cansancio / falta de energia",
    "14. Disminucion de concentracion",
    "15. Disminucion de productividad",
    "16. Tristeza / irritabilidad",
    "17. Sensacion de verguenza",
    "18. Incapacidad de hacer lo que gusta",
    "19. Incapacidad de salir de casa",
    "20. Incapacidad de trabajar",
    "21. Enojo con otros por mi condicion",
    "22. Compras por mi condicion",
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
