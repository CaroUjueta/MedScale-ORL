from datetime import datetime

from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout

from frontend.scales import escala_por_id
from frontend.widgets.app_header import SimpleHeader
from frontend.widgets.scale_row import ScaleRow
from frontend.widgets.ui import content_column, scroll_with, section_title, empty_message


def _formato_fecha(iso):
    try:
        dt = datetime.fromisoformat(iso)
        return dt.strftime("%d-%m-%Y")
    except Exception:
        return iso[:10]


class RecientesScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        root = BoxLayout(orientation="vertical")
        root.add_widget(SimpleHeader("Recientes", back_target="home"))
        self._content = content_column()
        root.add_widget(scroll_with(self._content))
        self.add_widget(root)

    def on_enter(self):
        self._rebuild()

    def _rebuild(self):
        from frontend.database import obtener_recientes

        self._content.clear_widgets()
        self._content.add_widget(section_title("Escalas recientes"))

        recientes = obtener_recientes()
        items = [(r["escala"], _formato_fecha(r["fecha"])) for r in recientes]
        items = [(e, f) for (e, f) in items if escala_por_id(e) is not None]

        if not items:
            empty_message(
                self._content,
                "Aun no hay escalas recien usadas.\nAbre una escala y aparecera aqui.",
            )
            return

        for escala_id, fecha in items:
            row = ScaleRow(escala_por_id(escala_id), show_star=False, date=fecha)
            self._content.add_widget(row)