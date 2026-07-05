from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from screens.home import HomeScreen
from screens.escala_vhi import VhiScreen
from screens.escala_snot import SnotScreen


class MedScaleORLApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(HomeScreen(name="home"))
        sm.add_widget(VhiScreen(name="vhi"))
        sm.add_widget(SnotScreen(name="snot"))
        return sm


if __name__ == "__main__":
    MedScaleORLApp().run()
