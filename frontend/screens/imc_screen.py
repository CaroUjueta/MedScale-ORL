from frontend.screens.base import ScaleScreen


class ImcScreen(ScaleScreen):
    title_text = "IMC"
    result_prefix = "IMC:"

    def _build_form(self, layout):
        self._section(layout, "Indice de Masa Corporal")
        self._peso = self._numeric_input(layout, "Peso (kg):", "Ej: 70")
        self._talla = self._numeric_input(layout, "Estatura (cm):", "Ej: 170")
        self._calc_btn(layout, self._calc)
        self._result_box(layout)

    def _calc(self, _):
        try:
            peso = float(self._peso.text)
            talla_m = float(self._talla.text) / 100.0
            if talla_m <= 0:
                self._show_result("Error")
                return
            self._show_result(f"{peso / (talla_m ** 2):.1f} kg/m2")
        except (ValueError, ZeroDivisionError):
            self._show_result("Ingrese valores")
