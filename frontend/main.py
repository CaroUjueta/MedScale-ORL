import os
os.environ.setdefault("KIVY_NO_ARGS", "1")

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, SlideTransition
from kivy.utils import get_color_from_hex
from kivy.core.window import Window
from kivy.metrics import dp

Window.clearcolor = get_color_from_hex("#F0F2F5")
Window.softinput_mode = "resize"

from frontend.database import init_db

from frontend.screens.home import HomeScreen
from frontend.screens.ess_screen import EssScreen
from frontend.screens.stop_bang_screen import StopBangScreen
from frontend.screens.imc_screen import ImcScreen
from frontend.screens.snot22_screen import Snot22Screen
from frontend.screens.lund_mackay_screen import LundMackayScreen
from frontend.screens.thi_screen import ThiScreen
from frontend.screens.etdq7_screen import Etdq7Screen
from frontend.screens.vhi10_screen import Vhi10Screen
from frontend.screens.grbas_screen import GrbasScreen
from frontend.screens.patient_list_screen import PatientListScreen
from frontend.screens.patient_form_screen import PatientFormScreen
from frontend.screens.patient_detail_screen import PatientDetailScreen
from frontend.screens.settings_screen import SettingsScreen
from frontend.screens.escalas_screen import EscalasScreen
from frontend.screens.favoritos_screen import FavoritosScreen
from frontend.screens.recientes_screen import RecientesScreen
from frontend.screens.guias_screen import GuiasScreen
from frontend.screens.calculadoras_screen import CalculadorasScreen
from frontend.screens.perfil_screen import PerfilScreen


class MedScaleORLApp(App):
    title = "MedScale-ORL"

    def build(self):
        init_db()

        sm = ScreenManager(
            transition=SlideTransition(duration=0.15),
        )
        sm.add_widget(HomeScreen(name="home"))
        sm.add_widget(EssScreen(name="ess"))
        sm.add_widget(StopBangScreen(name="stop_bang"))
        sm.add_widget(ImcScreen(name="imc"))
        sm.add_widget(Snot22Screen(name="snot22"))
        sm.add_widget(LundMackayScreen(name="lund_mackay"))
        sm.add_widget(ThiScreen(name="thi"))
        sm.add_widget(Etdq7Screen(name="etdq7"))
        sm.add_widget(Vhi10Screen(name="vhi10"))
        sm.add_widget(GrbasScreen(name="grbas"))
        sm.add_widget(PatientListScreen(name="patient_list"))
        sm.add_widget(PatientFormScreen(name="patient_form"))
        sm.add_widget(PatientDetailScreen(name="patient_detail"))
        sm.add_widget(SettingsScreen(name="settings"))
        sm.add_widget(EscalasScreen(name="escalas"))
        sm.add_widget(FavoritosScreen(name="favoritos"))
        sm.add_widget(RecientesScreen(name="recientes"))
        sm.add_widget(GuiasScreen(name="guias"))
        sm.add_widget(CalculadorasScreen(name="calculadoras"))
        sm.add_widget(PerfilScreen(name="perfil"))
        return sm


if __name__ == "__main__":
    MedScaleORLApp().run()
