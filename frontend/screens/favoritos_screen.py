from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout

from frontend.scales import escala_por_id
from frontend.widgets.app_header import SimpleHeader
from frontend.widgets.scale_row import ScaleRow
from frontend.widgets.ui import content_column, scroll_with, section_title, empty_message


class FavoritosScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        root = BoxLayout(orientation="vertical")
        root.add_widget(SimpleHeader("Favoritos", back_target="home"))
        self._content = content_column()
        root.add_widget(scroll_with(self._content))
        self.add_widget(root)

    def on_enter(self):
        self._rebuild()

    def _rebuild(self):
        from frontend.database import obtener_favoritas

        self._content.clear_widgets()
        self._content.add_widget(section_title("Mis favoritos"))

        favoritas = [f for f in obtener_favoritas() if escala_por_id(f) is not None]
        if not favoritas:
            empty_message(
                self._content,
                "Aun no tienes favoritos.\nToca la estrella en 'Escalas' para guardarlos.",
            )
            return

        for f in favoritas:
            row = ScaleRow(
                escala_por_id(f),
                show_star=True,
                on_toggle=self._rebuild,
            )
            self._content.add_widget(row)