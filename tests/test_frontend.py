import unittest


class TestFrontend(unittest.TestCase):
    def test_home_screen_exists(self):
        from frontend.screens.home import HomeScreen
        screen = HomeScreen()
        self.assertEqual(screen.name, "home")


if __name__ == "__main__":
    unittest.main()
