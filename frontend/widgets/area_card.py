import os
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.image import Image as KivyImage
from kivy.uix.button import Button
from kivy.uix.behaviors.button import ButtonBehavior
from kivy.uix.widget import Widget
from kivy.utils import get_color_from_hex
from kivy.metrics import dp, sp
from kivy.graphics import Color, RoundedRectangle, Line, Ellipse

_CWD = os.path.dirname(os.path.abspath(__file__))
_IMG = os.path.join(_CWD, "..", "assets")


class ChipBadge(Widget):
    def __init__(self, text, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (None, None)
        self.size = (dp(110), dp(30))
        self._lbl = Label(
            text=text,
            font_size=sp(13),
            color=get_color_from_hex("#2563EB"),
            halign="center",
            valign="middle",
            pos=self.pos,
            size=self.size,
        )
        self.add_widget(self._lbl)
        self.bind(pos=self._draw, size=self._draw)
        self.bind(pos=lambda s, p: setattr(s._lbl, 'pos', p))
        self.bind(size=lambda s, sz: setattr(s._lbl, 'size', sz))

    def _draw(self, *a):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(1, 1, 1, 0.85)
            RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(15)])
            Color(0.82, 0.87, 0.96, 1)
            Line(rounded_rectangle=(self.x, self.y, self.width, self.height, dp(15)), width=dp(0.8))


class AreaCard(BoxLayout):
    def __init__(self, title, subtitle, chips, bg_color, img_name, area=None, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "horizontal"
        self.size_hint_y = None
        self.height = dp(140)
        self.padding = [dp(14), dp(14), dp(14), dp(14)]
        self._bg_color = bg_color
        self._area = area

        self._img = KivyImage(
            source=os.path.join(_IMG, img_name),
            size_hint=(None, None),
            size=(dp(110), dp(110)),
            allow_stretch=False,
            keep_ratio=True,
            fit_mode="contain",
        )
        self.add_widget(self._img)

        self.add_widget(Widget(size_hint_x=None, width=dp(10)))

        col = BoxLayout(
            orientation="vertical",
            size_hint_x=1,
            spacing=dp(2),
        )

        self._title_lbl = Label(
            text=title.upper(),
            font_size=sp(18),
            bold=True,
            color=get_color_from_hex("#133E7C"),
            halign="left",
            valign="middle",
            size_hint_y=None,
            height=dp(24),
        )
        self._title_lbl.bind(size=self._set_text_size)
        col.add_widget(self._title_lbl)

        self._subtitle_lbl = Label(
            text=subtitle,
            font_size=sp(14),
            color=get_color_from_hex("#6B7280"),
            halign="left",
            valign="top",
            size_hint_y=None,
            height=dp(20),
        )
        self._subtitle_lbl.bind(size=self._set_text_size)
        col.add_widget(self._subtitle_lbl)

        chips_row = BoxLayout(
            orientation="horizontal",
            size_hint_y=None,
            height=dp(30),
            spacing=dp(6),
        )
        for c in chips:
            chips_row.add_widget(ChipBadge(text=c))
        col.add_widget(chips_row)

        self.add_widget(col)

        self.add_widget(Widget(size_hint_x=None, width=dp(8)))

        self._arrow = Button(
            text=">",
            size_hint=(None, None),
            size=(dp(38), dp(38)),
            background_normal="",
            background_color=get_color_from_hex("#FFFFFF"),
            color=get_color_from_hex("#6B7280"),
            font_size=sp(18),
            bold=True,
        )
        self.add_widget(self._arrow)
        self._arrow.bind(on_press=lambda *a: self._go())

        self.bind(pos=self._draw, size=self._draw)

    def _go(self):
        if not self._area:
            return
        from kivy.app import App
        sm = App.get_running_app().root
        esc = sm.get_screen("escalas")
        esc.set_filtro(self._area)
        sm.current = "escalas"

    @staticmethod
    def _set_text_size(label, size):
        label.text_size = (size[0], None)

    def _draw(self, *a):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(0, 0, 0, 0.06)
            RoundedRectangle(pos=(self.x + dp(2), self.y - dp(3)), size=self.size, radius=[dp(22)])
            Color(0, 0, 0, 0.03)
            RoundedRectangle(pos=(self.x + dp(1), self.y - dp(1)), size=self.size, radius=[dp(22)])
            Color(*self._bg_color)
            RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(22)])


class ApneaCard(AreaCard):
    def __init__(self, **kwargs):
        super().__init__(
            title="Apnea Obstructiva del Sueño",
            subtitle="Evaluacion y tamizaje",
            chips=["ESS", "STOP-BANG", "IMC"],
            bg_color=get_color_from_hex("#EDF5FF"),
            img_name="Apnea.png",
            area="apnea",
            **kwargs,
        )


class RinosinusitisCard(AreaCard):
    def __init__(self, **kwargs):
        super().__init__(
            title="Rinosinusitis",
            subtitle="Sintomas y evaluacion",
            chips=["SNOT-22", "Lund Mackay"],
            bg_color=get_color_from_hex("#EEF9F1"),
            img_name="Rinosinusitis.png",
            area="rinosinusitis",
            **kwargs,
        )


class OtologiaCard(AreaCard):
    def __init__(self, **kwargs):
        super().__init__(
            title="Otologia",
            subtitle="Audicion y funcion del oido",
            chips=["THI", "ETDQ-7"],
            bg_color=get_color_from_hex("#F3ECFF"),
            img_name="Otología.png",
            area="otologia",
            **kwargs,
        )


def _navigate(screen_name):
    from kivy.app import App
    app = App.get_running_app()
    if app is not None and app.root is not None:
        app.root.current = screen_name


class PillBadge(ButtonBehavior, Widget):
    def __init__(self, text, target=None, disabled=False, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (None, None)
        self.size = (dp(96), dp(26))
        self.target = target
        self.disabled = disabled
        self._active_color = get_color_from_hex("#2563EB")
        self._lbl = Label(
            text=text,
            font_size=sp(12),
            color=get_color_from_hex("#9CA3AF") if disabled else get_color_from_hex("#1F2937"),
            halign="center",
            valign="middle",
            pos=self.pos,
            size=self.size,
        )
        self.add_widget(self._lbl)
        self.bind(pos=self._draw, size=self._draw)
        self.bind(pos=lambda s, p: setattr(s._lbl, 'pos', p))
        self.bind(size=lambda s, sz: setattr(s._lbl, 'size', sz))
        Clock.schedule_once(self._measure)

    def _measure(self, _dt):
        self._lbl.texture_update()
        tw = self._lbl.texture_size[0]
        if tw < 1:
            Clock.schedule_once(self._measure, 0.02)
            return
        self.width = tw + dp(18)

    def _draw(self, *a):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(0.94, 0.94, 0.96, 1)
            RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(13)])
            Color(0, 0, 0, 0.08)
            Line(
                rounded_rectangle=(self.x, self.y, self.width, self.height, dp(13)),
                width=dp(0.6),
            )

    def on_press(self):
        if self.disabled:
            return
        self._lbl.color = self._active_color

    def on_release(self):
        if self.disabled or not self.target:
            return
        self._lbl.color = get_color_from_hex("#1F2937")
        _navigate(self.target)

    def on_touch_down(self, touch):
        if not self.collide_point(*touch.pos):
            return False
        if not self.disabled:
            ButtonBehavior.on_touch_down(self, touch)
        return True

    def on_touch_up(self, touch):
        if not self.collide_point(*touch.pos):
            return False
        if not self.disabled:
            ButtonBehavior.on_touch_up(self, touch)
        return True


class AirwayIcon(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (None, None)
        self.size = (dp(56), dp(56))
        self.bind(pos=self._draw, size=self._draw)

    @staticmethod
    def _profile():
        return [
            (0.36, 0.84), (0.33, 0.70), (0.26, 0.62), (0.21, 0.56),
            (0.18, 0.52), (0.16, 0.47), (0.19, 0.45), (0.15, 0.41),
            (0.21, 0.37), (0.27, 0.28), (0.33, 0.17), (0.45, 0.14),
            (0.58, 0.16), (0.71, 0.31), (0.73, 0.50), (0.62, 0.74),
            (0.60, 0.84),
        ]

    def _draw(self, *a):
        x, y, s = self.x, self.y, self.width
        self.canvas.before.clear()
        with self.canvas.before:
            Color(0.91, 0.94, 0.996, 1)
            Ellipse(pos=(x, y), size=(s, s))

        self.canvas.clear()
        with self.canvas:
            pts = []
            for px, py in self._profile():
                pts.append(x + px * s)
                pts.append(y + py * s)

            for w in (dp(7), dp(5), dp(4), dp(3)):
                Color(0.075, 0.243, 0.486, 1)
                Line(points=pts, width=w, close=True, joint="round", cap="round")

            Color(0.16, 0.62, 0.56, 1)
            Line(
                points=[
                    x + 0.265 * s, y + 0.46 * s,
                    x + 0.275 * s, y + 0.60 * s,
                    x + 0.295 * s, y + 0.71 * s,
                    x + 0.325 * s, y + 0.82 * s,
                ],
                width=dp(3.4),
                cap="round",
            )
            rings = [
                ((0.255, 0.58), (0.305, 0.58)),
                ((0.275, 0.68), (0.318, 0.68)),
                ((0.295, 0.77), (0.335, 0.77)),
            ]
            for (ax, ay), (bx, by) in rings:
                Line(
                    points=[x + ax * s, y + ay * s, x + bx * s, y + by * s],
                    width=dp(0.8),
                )


_VIA_AEREA_COLUMNS = [
    {
        "titulo": "Disfonía",
        "desc": "Evaluación de la voz",
        "chips": [
            ("VHI-10", "vhi10"),
            ("GRBAS", "grbas"),
        ],
    },
    {
        "titulo": "Apnea",
        "desc": "Evaluación del sueño",
        "chips": [
            ("Epworth (ESS)", "ess"),
            ("STOP-BANG", "stop_bang"),
            ("IMC", "imc"),
        ],
    },
]

_C_TITLE = get_color_from_hex("#1F2937")
_C_DESC = get_color_from_hex("#6B7280")
_C_NAVY = get_color_from_hex("#133E7C")


class ChevronButton(ButtonBehavior, Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (None, None)
        self.size = (dp(38), dp(38))
        self.point_down = True
        self.bind(pos=self._draw, size=self._draw)

    def set_expanded(self, expanded):
        self.point_down = bool(expanded)
        self._draw()

    def _draw(self, *a):
        c = self.canvas.before
        c.clear()
        x, y, w, h = self.x, self.y, self.width, self.height
        cx, cy = x + w / 2, y + h / 2
        with c:
            Color(0.95, 0.96, 0.97, 1)
            Ellipse(pos=(x, y), size=(w, h))
            Color(0.33, 0.36, 0.39, 1)
            if self.point_down:
                Line(
                    points=[cx - dp(6), cy, cx, cy + dp(7), cx + dp(6), cy],
                    width=dp(2),
                    joint="round",
                    cap="round",
                )
            else:
                Line(
                    points=[cx, cy + dp(6), cx + dp(7), cy, cx, cy - dp(6)],
                    width=dp(2),
                    joint="round",
                    cap="round",
                )


class ViaAereaCard(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"
        self.size_hint_y = None
        self.padding = [dp(14), dp(12), dp(14), dp(12)]
        self.spacing = dp(8)
        self._expanded = True
        self._mode = "narrow"
        self._bg_color = get_color_from_hex("#FFFFFF")

        self.bind(minimum_height=self.setter("height"))
        self.bind(pos=self._draw, size=self._draw)

        header = BoxLayout(
            orientation="horizontal",
            size_hint_y=None,
            height=dp(56),
            spacing=dp(12),
        )
        header.add_widget(AirwayIcon())

        title = Label(
            text="VÍA AÉREA",
            font_size=sp(18),
            bold=True,
            color=_C_NAVY,
            halign="left",
            valign="middle",
            size_hint_x=1,
        )
        title.bind(size=lambda s, sz: setattr(s, "text_size", (sz[0], None)))
        header.add_widget(title)

        self._arrow = ChevronButton()
        self._arrow.bind(on_press=lambda *_: self._toggle())
        header.add_widget(self._arrow)
        self.add_widget(header)

        self._col_host = BoxLayout(
            orientation="vertical",
            size_hint_y=None,
        )
        self._col_host.bind(minimum_height=self._sync_col_host)
        self._col_host.height = 0
        self.add_widget(self._col_host)

        self._build_columns()
        self.bind(size=self._apply_responsive)

    def _sync_col_host(self, *a):
        if self._expanded:
            Clock.schedule_once(self._apply_col_height, -1)
        else:
            self._col_host.height = 0

    def _apply_col_height(self, *_a):
        self._col_host.height = 0 if not self._expanded else self._col_host.minimum_height

    def _build_columns(self):
        self._col_host.clear_widgets()
        inner = self.width - self.padding[0] - self.padding[2]
        self._mode = "wide" if inner >= dp(430) else "narrow"

        if self._mode == "wide":
            container = BoxLayout(
                orientation="horizontal",
                size_hint_y=None,
                spacing=dp(10),
            )
            columns = [self._build_column(col) for col in _VIA_AEREA_COLUMNS]
            max_h = max(c.height for c in columns)
            for c in columns:
                c.height = max_h
                container.add_widget(c)
        else:
            container = BoxLayout(
                orientation="vertical",
                size_hint_y=None,
                spacing=dp(8),
            )
            for col in _VIA_AEREA_COLUMNS:
                container.add_widget(self._build_column(col))

        container.bind(minimum_height=container.setter("height"))
        self._col_host.add_widget(container)
        if self._expanded:
            Clock.schedule_once(self._apply_col_height, -1)

    def _build_column(self, col):
        column = BoxLayout(
            orientation="vertical",
            size_hint_y=None,
            spacing=dp(6),
        )

        def _left(lbl):
            lbl.bind(size=lambda s, sz: setattr(s, "text_size", (sz[0], None)))
            return lbl

        col_title = _left(Label(
            text=col["titulo"],
            font_size=sp(15),
            bold=True,
            color=_C_TITLE,
            halign="left",
            valign="middle",
            size_hint_y=None,
            height=dp(22),
        ))
        column.add_widget(col_title)

        desc = _left(Label(
            text=col["desc"],
            font_size=sp(12),
            color=_C_DESC,
            halign="left",
            valign="middle",
            size_hint_y=None,
            height=dp(18),
        ))
        column.add_widget(desc)

        stack_h = dp(0)
        chips = BoxLayout(
            orientation="vertical",
            size_hint_y=None,
            spacing=dp(5),
        )
        for text, target in col["chips"]:
            chips.add_widget(PillBadge(text=text, target=target, disabled=target is None))
            stack_h += dp(26)
        if col["chips"]:
            stack_h += dp(5) * (len(col["chips"]) - 1)
        chips.height = stack_h
        column.add_widget(chips)

        column.height = dp(22) + dp(6) + dp(18) + dp(6) + stack_h
        return column

    def _toggle(self):
        self._expanded = not self._expanded
        self._arrow.set_expanded(self._expanded)
        self._apply_col_height()

    def _apply_responsive(self, *a):
        inner = self.width - self.padding[0] - self.padding[2]
        mode = "wide" if inner >= dp(430) else "narrow"
        if mode != self._mode:
            self._build_columns()

    def on_touch_down(self, touch):
        if not self.collide_point(*touch.pos):
            return False
        if super().on_touch_down(touch):
            return True
        self._toggle()
        return True

    def _draw(self, *a):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(0, 0, 0, 0.06)
            RoundedRectangle(pos=(self.x + dp(2), self.y - dp(3)), size=self.size, radius=[dp(22)])
            Color(0, 0, 0, 0.03)
            RoundedRectangle(pos=(self.x + dp(1), self.y - dp(1)), size=self.size, radius=[dp(22)])
            Color(*self._bg_color)
            RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(22)])
