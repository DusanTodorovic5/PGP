from kivy.lang import Builder
from kivymd.app import MDApp

class MainApp(MDApp):

    def build(self):
        return Builder.load_file("layouts/main_screen.kv")
    
    def on_start(self):
        self.title = "PGP"
        self.theme_cls.primary_palette = "DeepPurple"