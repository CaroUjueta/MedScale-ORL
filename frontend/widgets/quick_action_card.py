import os
from kivy.uix.behaviors.button import ButtonBehavior
from kivy.uix.image import Image as KivyImage

_CWD = os.path.dirname(os.path.abspath(__file__))
_IMG = os.path.join(_CWD, "..", "assets")


class QuickActionCard(ButtonBehavior, KivyImage):
    def __init__(self, source, target=None, **kwargs):
        super().__init__(**kwargs)
        self.source = os.path.join(_IMG, source)
        self.target = target
        self.size_hint = (None, None)
        self.allow_stretch = False
        self.keep_ratio = True
        self.pos_hint = {"center_x": 0.5, "center_y": 0.5}

    def on_release(self):
        if not self.target:
            return
        from kivy.app import App
        app = App.get_running_app()
        if app is not None and app.root is not None:
            app.root.current = self.target

    @property
    def aspect(self):
        w, h = self.texture_size
        if h <= 0:
            return 0.0
        return float(w) / float(h)