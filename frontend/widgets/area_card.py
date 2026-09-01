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


def _shade(color, factor):
    """Return `color` with its RGB channels scaled by `factor` (kept opaque)."""
    return (color[0] * factor, color[1] * factor, color[2] * factor, 1)


def _mix(a, b, t):
    """Blend color `a` toward color `b` by `t` (0..1), kept opaque."""
    return (
        a[0] + (b[0] - a[0]) * t,
        a[1] + (b[1] - a[1]) * t,
        a[2] + (b[2] - a[2]) * t,
        1,
    )


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


class PillBadge(ButtonBehavior, Widget):
    """Auto-width chip (white pill, blue border). Opens a scale screen when it has a target."""

    def __init__(self, text, target=None, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (None, None)
        self.size = (dp(72), dp(26))
        self.target = target
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
        self.bind(pos=self._sync, size=self._sync)
        Clock.schedule_once(self._measure)

    def _sync(self, *a):
        self._lbl.pos = self.pos
        self._lbl.size = self.size
        self._draw()

    def _measure(self, _dt):
        self._lbl.texture_update()
        tw = self._lbl.texture_size[0]
        if tw < 1:
            Clock.schedule_once(self._measure, 0.02)
            return
        self.width = tw + dp(18)
        self._sync()

    def _draw(self, *a):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(1, 1, 1, 0.85)
            RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(13)])
            Color(0.82, 0.87, 0.96, 1)
            Line(
                rounded_rectangle=(self.x, self.y, self.width, self.height, dp(13)),
                width=dp(0.8),
            )

    def on_release(self):
        if not self.target:
            return
        from kivy.app import App
        app = App.get_running_app()
        if app is not None and app.root is not None:
            app.root.current = self.target


class AreaCard(BoxLayout):
    def __init__(self, title, subtitle, chips, bg_color, img_name, area=None,
                 img_tint=None, icon_disk=False, disk_tint=None,
                 icon_size=110, disk_size=None, pad_left=14, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "horizontal"
        self.size_hint_y = None
        self.height = dp(140)
        self.padding = [dp(pad_left), dp(14), dp(14), dp(14)]
        self._bg_color = bg_color
        self._area = area
        self._icon_disk = bool(icon_disk)
        self._disk_size = dp(disk_size if disk_size is not None else icon_size)
        # Disk behind the icon: same hue as the card, just a little deeper. When
        # `disk_tint` is given the base is nudged toward it so it stays coordinated.
        base = bg_color if disk_tint is None else _mix(bg_color, disk_tint, 0.18)
        self._disk_fill = _shade(base, 0.98 if disk_tint is not None else 0.93)
        self._disk_ring = _shade(base, 0.84)

        self._img = KivyImage(
            source=os.path.join(_IMG, img_name),
            size_hint=(None, None),
            size=(dp(icon_size), dp(icon_size)),
            allow_stretch=False,
            keep_ratio=True,
            fit_mode="contain",
            pos_hint={"center_y": 0.5},
        )
        if img_tint is not None:
            self._img.color = img_tint
        self.add_widget(self._img)
        if icon_disk:
            self._img.bind(pos=self._draw, size=self._draw)

        self.add_widget(Widget(size_hint_x=None, width=dp(pad_left)))

        col = BoxLayout(
            orientation="vertical",
            size_hint_x=1,
            spacing=dp(2),
        )

        col.add_widget(Widget())

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

        col.add_widget(Widget())

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

            if self._icon_disk:
                d = self._disk_size
                cx, cy = self._img.center
                Color(*self._disk_fill)
                Ellipse(pos=(cx - d / 2, cy - d / 2), size=(d, d))
                Color(*self._disk_ring)
                Line(circle=(cx, cy, d / 2), width=dp(1))


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
            title="Rinología",
            subtitle="Rinosinusitis",
            chips=["SNOT-22", "Lund Mackay"],
            bg_color=get_color_from_hex("#EEF9F1"),
            img_name="Rinosinusitis.png",
            area="rinosinusitis",
            icon_size=96,
            disk_size=96,
            icon_disk=True,
            disk_tint=get_color_from_hex("#10B981"),
            pad_left=12,
            **kwargs,
        )


_OTOLOGIA_COLUMNS = [
    {
        "titulo": "Tinnitus",
        "desc": "gravedad del acúfeno",
        "tests": [("THI", "thi")],
        "width": 160,
    },
    {
        "titulo": "Disfunción tubárica",
        "desc": "Función tubárica",
        "tests": [("ETDQ-7", "etdq7")],
        "width": 230,
    },
]


_VIA_AEREA_COLUMNS = [
    {
        "titulo": "Disfonía",
        "desc": "Evaluación de la voz",
        "tests": [("VHI-10", "vhi10"), ("GRBAS", "grbas")],
        "width": 150,
    },
    {
        "titulo": "Apnea",
        "desc": "Evaluación del sueño",
        "tests": [("ESS", "ess"), ("STOP-BANG", "stop_bang"), ("IMC", "imc")],
        "width": 220,
    },
]


class ViaAereaCard(BoxLayout):
    def __init__(self, title="VÍA AÉREA", bg="#EDF5FF", disk_tint="#2563EB",
                 img_name="Inicio.png", columns=None, area=None,
                 icon_tint="#2563EB", **kwargs):
        super().__init__(**kwargs)
        self.orientation = "horizontal"
        self.size_hint_y = None
        self.height = dp(140)
        self.padding = [dp(12), dp(12), dp(12), dp(12)]
        self.spacing = dp(12)
        self._area = area

        bg = get_color_from_hex(bg)
        self._bg_color = bg
        base = _mix(bg, get_color_from_hex(disk_tint), 0.10)
        self._disk_fill = _shade(base, 0.99)
        self._disk_ring = _shade(base, 0.70)

        self._img = KivyImage(
            source=os.path.join(_IMG, img_name),
            size_hint=(None, None),
            size=(dp(96), dp(96)),
            allow_stretch=False,
            keep_ratio=True,
            fit_mode="contain",
            color=get_color_from_hex(icon_tint),
            pos_hint={"center_y": 0.5},
        )
        self.add_widget(self._img)
        self._img.bind(pos=self._draw, size=self._draw)

        content = BoxLayout(
            orientation="vertical",
            size_hint_x=1,
            spacing=dp(4),
        )

        self._title_lbl = Label(
            text=title,
            font_size=sp(18),
            bold=True,
            color=get_color_from_hex("#133E7C"),
            halign="left",
            valign="middle",
            size_hint_y=None,
            height=dp(24),
        )
        self._title_lbl.bind(size=lambda s, sz: setattr(s, "text_size", (sz[0], None)))
        content.add_widget(self._title_lbl)

        cols_row = BoxLayout(orientation="horizontal", size_hint_y=1, spacing=dp(24))
        for col in (columns or _VIA_AEREA_COLUMNS):
            cols_row.add_widget(self._build_column(col))
        content.add_widget(cols_row)

        self.add_widget(content)

        self._arrow = Button(
            text=">",
            size_hint=(None, None),
            size=(dp(34), dp(34)),
            background_normal="",
            background_color=get_color_from_hex("#FFFFFF"),
            color=get_color_from_hex("#6B7280"),
            font_size=sp(18),
            bold=True,
            pos_hint={"center_y": 0.5},
        )
        self._arrow.bind(on_press=lambda *a: self._go())
        self.add_widget(self._arrow)

        self.bind(pos=self._draw, size=self._draw)

    def _build_column(self, data):
        # Fixed width per column so each one fits its title and chips while the
        # cards keep an even look and a moderate gap between the two columns.
        column = BoxLayout(
            orientation="vertical",
            size_hint_x=None,
            width=dp(data.get("width", 160)),
            spacing=dp(1),
        )

        column.add_widget(Widget(size_hint_y=None, height=dp(0)))

        title = Label(
            text=data["titulo"],
            font_size=sp(14),
            bold=True,
            color=get_color_from_hex("#1F2937"),
            halign="left",
            valign="middle",
            size_hint_y=None,
            height=dp(19),
        )
        title.bind(size=lambda s, sz: setattr(s, "text_size", (sz[0], None)))
        column.add_widget(title)

        desc = Label(
            text=data["desc"],
            font_size=sp(11),
            color=get_color_from_hex("#6B7280"),
            halign="left",
            valign="middle",
            shorten=True,
            shorten_from="right",
            size_hint_y=None,
            height=dp(15),
        )
        desc.bind(width=lambda s, w: setattr(s, "text_size", (w, s.height)))
        column.add_widget(desc)

        column.add_widget(Widget(size_hint_y=None, height=dp(2)))

        chips = BoxLayout(
            orientation="horizontal",
            size_hint=(None, None),
            height=dp(26),
            spacing=dp(2),
        )
        chips.bind(minimum_width=chips.setter("width"))
        for text, target in data["tests"]:
            chips.add_widget(PillBadge(text=text, target=target))
        column.add_widget(chips)

        column.add_widget(Widget())

        return column

    def _go(self):
        from kivy.app import App
        sm = App.get_running_app().root
        if sm is None:
            return
        try:
            sm.get_screen("escalas").set_filtro(self._area)
        except Exception:
            pass
        sm.current = "escalas"

    def _draw(self, *a):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(0, 0, 0, 0.06)
            RoundedRectangle(pos=(self.x + dp(2), self.y - dp(3)), size=self.size, radius=[dp(22)])
            Color(0, 0, 0, 0.03)
            RoundedRectangle(pos=(self.x + dp(1), self.y - dp(1)), size=self.size, radius=[dp(22)])
            Color(*self._bg_color)
            RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(22)])

            d = dp(96)
            cx, cy = self._img.center
            Color(*self._disk_fill)
            Ellipse(pos=(cx - d / 2, cy - d / 2), size=(d, d))
            Color(*self._disk_ring)
            Line(circle=(cx, cy, d / 2), width=dp(1))


class OtologiaCard(ViaAereaCard):
    def __init__(self, **kwargs):
        super().__init__(
            title="OTOLOGÍA",
            bg="#F3ECFF",
            disk_tint="#7C3AED",
            icon_tint="#FFFFFF",
            img_name="Otología.png",
            columns=_OTOLOGIA_COLUMNS,
            area="otologia",
            **kwargs,
        )

