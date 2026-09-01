from frontend.screens.base import ScaleScreen

OPTS = ["No (0)", "A veces (2)", "Si (4)"]
VALS = [0, 2, 4]

def _interpretar_thi(puntaje):
    if puntaje <= 16:
        return "Sin discapacidad\n(acufeno leve)"
    elif puntaje <= 36:
        return "Discapacidad leve"
    elif puntaje <= 56:
        return "Discapacidad moderada"
    elif puntaje <= 76:
        return "Discapacidad severa"
    else:
        return "Discapacidad catastrofica"


QS = [
    "¿Le cuesta concentrarse por culpa del ruido o zumbido de oído?",
    "¿Le cuesta escuchar a los demás debido a que el zumbido es muy fuerte?",
    "¿Lo pone mal genio el zumbido del oído?",
    "¿Se siente confundido por culpa del zumbido del oído?",
    "¿Se desespera con el ruido o zumbido del oído?",
    "¿Se queja mucho por tener el zumbido en el oído?",
    "¿Le cuesta quedarse dormido en la noche por culpa del zumbido del oído?",
    "¿Cree que el problema de su zumbido es algo sin solución?",
    "¿El zumbido del oído es un problema que le impide disfrutar de la vida como por ejemplo salir a comer con amigos o ir al cine?",
    "¿Se siente desilusionado por culpa del zumbido del oído?",
    "¿Cree que tiene una enfermedad incurable?",
    "¿El zumbido de oído le impide pasarlo bien?",
    "¿Le estorba el zumbido de oído en su trabajo o en las labores de la casa?",
    "¿Se siente a menudo de mal genio por culpa del zumbido del oído?",
    "¿Le cuesta comprender lo que lee por culpa del zumbido del oído?",
    "¿Se siente alterado por el zumbido de oído?",
    "¿Siente que el zumbido de oído ha echado a perder las relaciones con sus familiares y amigos?",
    "¿Le cuesta sacarse de la cabeza el zumbido y concentrarse en otra cosa?",
    "¿Siente que no puede controlar el zumbido de oído?",
    "¿Se siente a menudo cansado por culpa del zumbido de oído?",
    "¿Se siente deprimido por causa del zumbido de oído?",
    "¿Lo pone nervioso el zumbido de oído?",
    "¿Siente que no puede ya hacerle frente al zumbido de oído?",
    "¿Empeora el zumbido de oído cuando está estresado?",
    "¿Se siente inseguro por culpa del zumbido de oído?",
]


class ThiScreen(ScaleScreen):
    title_text = "THI"
    result_prefix = "THI:"
    scale_name = "THI"
    _questions = QS

    def _build_form(self, layout):
        self._section(layout, "Responda No, A veces o Si:")
        self._cards = []
        for q in QS:
            self._cards.append(self._question(layout, q, OPTS, VALS))
        self._calc_btn(layout, self._calc)
        self._result_box(layout)

    def _calc(self, _):
        total = sum(c._option_state["score"] for c in self._cards)
        interp = _interpretar_thi(total)
        self._result_lbl.text = f"{self.result_prefix} {total}\n{interp}"
        self._last_puntaje = total
        self._save_btn_widget.opacity = 1
        self._save_btn_widget.disabled = False
