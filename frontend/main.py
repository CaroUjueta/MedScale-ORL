from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, NoTransition
from kivy.utils import get_color_from_hex
from kivy.core.window import Window

from frontend.screens.home import HomeScreen
from frontend.screens.ess_screen import EssScreen
from frontend.screens.stop_bang_screen import StopBangScreen
from frontend.screens.imc_screen import ImcScreen
from frontend.screens.snot22_screen import Snot22Screen
from frontend.screens.lund_mackay_screen import LundMackayScreen
from frontend.screens.thi_screen import ThiScreen
from frontend.screens.etdq7_screen import Etdq7Screen

BG = get_color_from_hex("#F0F2F5")

Window.clearcolor = BG


class MedScaleORLApp(App):
    def build(self):
        sm = ScreenManager(transition=NoTransition())
        sm.add_widget(HomeScreen(name="home"))
        sm.add_widget(EssScreen(name="ess"))
        sm.add_widget(StopBangScreen(name="stop_bang"))
        sm.add_widget(ImcScreen(name="imc"))
        sm.add_widget(Snot22Screen(name="snot22"))
        sm.add_widget(LundMackayScreen(name="lund_mackay"))
        sm.add_widget(ThiScreen(name="thi"))
        sm.add_widget(Etdq7Screen(name="etdq7"))
        return sm


if __name__ == "__main__":
    MedScaleORLApp().run()
