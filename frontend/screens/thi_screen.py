from frontend.screens.base import ScaleScreen

OPTS = ["No (0)", "A veces (2)", "Si (4)"]
VALS = [0, 2, 4]

QS = [
    "1. Le impiden los zumbidos conciliar el sueño",
    "2. Le impiden los zumbidos concentrate",
    "3. Le impiden los zumbidos escuchar con claridad",
    "4. Le causan los zumbidos enfado",
    "5. Le causan los zumbidos confusion",
    "6. Le causan los zumbidos depresion",
    "7. Le impiden los zumbidos relajarse",
    "8. Le causan los zumbidos ansiedad",
    "9. Le impiden los zumbidos disfrutar de la vida social",
    "10. Le impiden los zumbidos trabajar",
    "11. Le impiden los zumbidos leer",
    "12. Le impiden los zumbidos disfrutar de la musica",
    "13. Le causan los zumbidos irritabilidad",
    "14. Le causan los zumbidos problemas de equilibrio",
    "15. Le impiden los zumbidos ir al cine",
    "16. Le causan los zumbidos perder el control",
    "17. Le impiden los zumbidos disfrutar del silencio",
    "18. Le causan los zumbidos desesperanza",
    "19. Le impiden los zumbidos socializar",
    "20. Le causan los zumbidos cansancio",
    "21. Le causan los zumbidos sentirse enfermo/a",
    "22. Le impiden los zumbidos viajar en avion",
    "23. Le impiden los zumbidos subir escaleras",
    "24. Le impiden los zumbidos disfrutar aficiones",
    "25. Le impiden los zumbidos vivir normalmente",
]


class ThiScreen(ScaleScreen):
    title_text = "THI"
    result_prefix = "THI:"

    def _build_form(self, layout):
        self._section(layout, "Responda No, A veces o Si:")
        self._cards = []
        for q in QS:
            self._cards.append(self._question(layout, q, OPTS, VALS))
        self._calc_btn(layout, self._calc)
        self._result_box(layout)

    def _calc(self, _):
        self._show_result(sum(c._option_state["score"] for c in self._cards))
