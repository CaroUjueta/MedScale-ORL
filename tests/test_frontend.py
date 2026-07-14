import unittest


class TestFrontend(unittest.TestCase):
    def test_home_screen_importable(self):
        try:
            from frontend.screens.home import HomeScreen
            screen = HomeScreen()
            self.assertEqual(screen.name, "home")
        except ImportError:
            self.skipTest("Kivy no instalado en este entorno")


if __name__ == "__main__":
    unittest.main()
