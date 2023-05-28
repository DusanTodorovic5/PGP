from kivy.lang import Builder
from kivymd.app import MDApp
from components import FloatingButton, DialogContent
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button.button import MDFlatButton
from kivy.config import Config


import config

class MainApp(MDApp):
    """
    MainApp screen class 
    """
    def __init__(self, **kwargs):
        """Constructor of MainApp. 
        Loads the icon, flotaing button data and all of the components avaliable
        """
        super().__init__(**kwargs)
        self.dialog = None
        Config.set('kivy','window_icon',config.get_icon("icon"))


        # Load all components in builder
        for kv_component in config.get_all_components():
            self.icon = config.get_icon("icon")
            Builder.load_file(kv_component)

    def build(self):
        """Build method inherited from Kivy's MDApp"""
        return Builder.load_file(config.get_screen("main_screen"))
    
    def on_start(self):
        """Start method inherited from Kivy's MDApp"""
        self.title = "PGP"
        self.icon = 'security'
        self.theme_cls.primary_palette = "DeepPurple"

    def new_key_pair_click(self):
        """Callback for creating new pair of keys"""
        if not self.dialog:
            tmp = MDDialog(
                title = "Generate new pair of keys",
                type="custom",
                content_cls = DialogContent(),
                buttons=[
                    MDFlatButton(
                        text="CANCEL",
                        theme_text_color="Custom",
                        text_color=self.theme_cls.primary_color,
                        on_release=lambda x, close_dialog=MainApp.close_dialog, this=self: close_dialog(this)
                    ),
                    MDFlatButton(
                        text="GENERATE",
                        theme_text_color="Custom",
                        text_color=self.theme_cls.primary_color,
                        on_press=lambda x, generate_keys=MainApp.generate_keys, this=self: generate_keys(this)
                    ),
                ],
                on_dismiss=lambda x, close_dialog=MainApp.release_dialog, this=self: close_dialog(this)
            )
            self.dialog = tmp
            self.dialog.open()

    def close_dialog(self):
        if self.dialog:
            self.dialog.dismiss(force=True)

    def release_dialog(self):
        self.dialog = None

    def generate_keys(self):
        pass
            