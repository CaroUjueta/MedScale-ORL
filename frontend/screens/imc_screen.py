import os
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.widget import Widget
from kivy.uix.textinput import TextInput
from kivy.utils import get_color_from_hex
from kivy.metrics import dp, sp
from kivy.graphics import Color, RoundedRectangle

from frontend.screens.base import ScaleScreen, C_BG, C_TEXT, C_TEXT_SEC, C_PRIMARY, C_CARD

_ASSETS = os.path.join(os.path.dirname(__file__), "..", "assets")

_CATS = [
    (18.5, "Bajo peso",        get_color_from_hex("#FF9800"), os.path.join(_ASSETS, "silueta_bajo_peso.png")),
    (25.0, "Peso normal",      get_color_from_hex("#4CAF50"), os.path.join(_ASSETS, "silueta_peso_normal.png")),
    (30.0, "Sobrepeso",        get_color_from_hex("#FF5722"), os.path.join(_ASSETS, "silueta_sobrepeso.png")),
    (35.0, "Obesidad grado I", get_color_from_hex("#F44336"), os.path.join(_ASSETS, "silueta_obesidad_1.png")),
    (40.0, "Obesidad grado II",get_color_from_hex("#C62828"), os.path.join(_ASSETS, "silueta_obesidad_2.png")),
    (999,  "Obesidad grado III",get_color_from_hex("#B71C1C"), os.path.join(_ASSETS, "silueta_obesidad_3.png")),
]


def _classify(bmi):
    for max_val, label, color, img in _CATS:
        if bmi < max_val:
            return label, color, img
    return _CATS[-1][1], _CATS[-1][2], _CATS[-1][3]


class ImcScreen(ScaleScreen):
    title_text = "IMC"
    result_prefix = "IMC:"

    def _build_body(self):
        root = BoxLayout(
            orientation="horizontal",
            padding=[dp(12), dp(8)],
            spacing=dp(10),
        )

        left = BoxLayout(
            orientation="vertical",
            size_hint_x=0.45,
            spacing=dp(8),
        )
        self._section(left, "Indice de Masa Corporal")
        self._peso = self._numeric_input(left, "Peso (kg):", "Ej: 70")
        self._talla = self._numeric_input(left, "Estatura (cm):", "Ej: 170")
        self._calc_btn(left, self._calc)
        left.add_widget(Widget())

        right = BoxLayout(
            orientation="vertical",
            size_hint_x=0.55,
            spacing=dp(6),
        )
        self._build_result_area(right)

        root.add_widget(left)
        root.add_widget(right)
        return root

    def _build_form(self, layout):
        pass

    def _numeric_input(self, layout, text, hint, card_height=None):
        card = BoxLayout(
            orientation="vertical",
            size_hint_y=None,
            height=card_height or dp(90),
            padding=[dp(12), dp(6)],
            spacing=dp(2),
        )
        with card.canvas.before:
            Color(*C_CARD)
            card._bg = RoundedRectangle(
                pos=card.pos, size=card.size, radius=[dp(8)]
            )
        card.bind(pos=lambda s, p: setattr(card._bg, 'pos', p))
        card.bind(size=lambda s, sz: setattr(card._bg, 'size', sz))

        lbl = Label(
            text=text,
            font_size=sp(15),
            color=C_TEXT,
            halign="left",
            valign="middle",
            text_size=(None, None),
            size_hint_y=0.45,
        )
        lbl.bind(width=lambda s, w: setattr(s, 'text_size', (w - dp(8), None)))
        card.add_widget(lbl)

        ti = TextInput(
            hint_text=hint,
            multiline=False,
            input_filter="float",
            size_hint_y=0.55,
            font_size=sp(18),
            padding=[dp(12), dp(8)],
            background_normal="",
            background_active="",
            background_color=C_BG,
            cursor_color=C_PRIMARY,
            foreground_color=C_TEXT,
            hint_text_color=C_TEXT_SEC,
            cursor_width=dp(2),
        )
        card.add_widget(ti)
        layout.add_widget(card)
        return ti

    def _build_result_area(self, layout):
        card = BoxLayout(
            orientation="vertical",
            padding=[dp(10), dp(8)],
            spacing=dp(4),
        )
        with card.canvas.before:
            Color(0.88, 0.95, 0.95, 1)
            card._bg = RoundedRectangle(
                pos=card.pos, size=card.size, radius=[dp(12)],
            )
        card.bind(pos=lambda s, p: setattr(card._bg, 'pos', p))
        card.bind(size=lambda s, sz: setattr(card._bg, 'size', sz))

        self._result_lbl = Label(
            text="",
            font_size=sp(20),
            bold=True,
            color=get_color_from_hex("#0D6E6E"),
            halign="center",
            valign="middle",
            size_hint_y=None,
            height=dp(32),
        )
        card.add_widget(self._result_lbl)

        self._cat_lbl = Label(
            text="",
            font_size=sp(14),
            bold=True,
            halign="center",
            valign="middle",
            size_hint_y=None,
            height=dp(24),
        )
        card.add_widget(self._cat_lbl)

        self._silueta = Image(
            source=os.path.join(_ASSETS, "silueta_peso_normal.png"),
            size_hint_y=1,
            fit_mode="contain",
        )
        card.add_widget(self._silueta)

        layout.add_widget(card)

    def _calc(self, _):
        try:
            peso = float(self._peso.text)
            talla_m = float(self._talla.text) / 100.0
            if talla_m <= 0:
                self._show_result("Error")
                return
            bmi = peso / (talla_m ** 2)
            label, color, img = _classify(bmi)

            self._result_lbl.text = f"IMC: {bmi:.1f} kg/m\u00b2"
            self._cat_lbl.text = label
            self._cat_lbl.color = color
            self._silueta.source = img
            self._silueta.reload()
        except (ValueError, ZeroDivisionError):
            self._show_result("Ingrese valores")
            self._cat_lbl.text = ""
