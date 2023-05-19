from kivy.lang import Builder
from kivymd.app import MDApp
from components import FloatingButton
from kivy.config import Config

import config

class MainApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Config.set('kivy','window_icon',config.get_icon("icon"))
        self.floating_button_data = {
            "RSA" : [
                "lock-check",
                'allow_stretch', False,
                'keep_ratio', True,
                'on_press', lambda this: self.rsa_click()
            ],
            "DSA + ElGamal" : [
                "lock-check",
                'allow_stretch', False,
                'keep_ratio', True,
                'on_press', lambda this: self.dsa_clicked()
            ]
        }
        # Load all components in builder
        for kv_component in config.get_all_components():
            self.icon = config.get_icon("icon")
            Builder.load_file(kv_component)

    def build(self):
        return Builder.load_file(config.get_screen("main_screen"))
    
    def on_start(self):
        self.title = "PGP"
        self.icon = 'security'
        self.theme_cls.primary_palette = "DeepPurple"

    def rsa_click(self):
        print("RSA CLICKED")

    def dsa_clicked(self):
        print("DSA CLICKED")

