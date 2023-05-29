from kivy.lang import Builder
from kivymd.app import MDApp
from components import FloatingButton, DialogContent, MissingFieldSnackbar, PasswordDialog, NonMatchingPasswordsSnackbar
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button.button import MDFlatButton
from kivy.config import Config
from rsa_algorithm import RSAPGP
from dsa_el_gamal_algorithm import DSAElGamalPGP
from cryptography.hazmat.primitives import serialization

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

       
        encryption_algorithm = DSAElGamalPGP()
          
        # encryption_algorithm = DSAElGamalPGP()

        keys = encryption_algorithm.generate_keys(2048)

        decoded_keys = encryption_algorithm.decode_keys(keys["sign"])
        print(decoded_keys)

        

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
                        on_release=lambda x, this=self: MainApp.close_dialog(this)
                    ),
                    MDFlatButton(
                        text="GENERATE",
                        theme_text_color="Custom",
                        text_color=self.theme_cls.primary_color,
                        on_release=lambda x, this=self: MainApp.enter_password(this)
                    ),
                ],
                on_dismiss=lambda x, this=self: MainApp.release_dialog(this)
            )
            self.dialog = tmp
            self.dialog.open()

    def open_password_dialog(self, data):
        tmp = MDDialog(
            title = "Enter keys password",
            type="custom",
            content_cls = PasswordDialog(),
            buttons=[
                MDFlatButton(
                    text="CANCEL",
                    theme_text_color="Custom",
                    text_color=self.theme_cls.primary_color,
                    on_release=lambda x, this=self: MainApp.close_dialog(this)
                ),
                MDFlatButton(
                    text="OK",
                    theme_text_color="Custom",
                    text_color=self.theme_cls.primary_color,
                    on_release=lambda x, this=self: MainApp.generate_keys(this, data)
                ),
            ],
            on_dismiss=lambda x, this=self: MainApp.release_dialog(this)
        )
        self.dialog = tmp
        self.dialog.open()

    def close_dialog(self):
        if self.dialog:
            self.dialog.dismiss(force=True)

    def release_dialog(self):
        self.dialog = None

    def enter_password(self):
        if self.dialog:
            data = self.dialog.content_cls.get_data()
            print(data)

            if data["name"] == "" or data["email"] == "":
                MissingFieldSnackbar().open()
                return

            self.dialog.dismiss(force=True)
            self.open_password_dialog(data)

    def generate_keys(self, data):
        if self.dialog:
            passwords = self.dialog.content_cls.get_data()
            print(passwords)
            print(data)

            if passwords["password"] != passwords["confirm_password"] or passwords["password"] == "":
                NonMatchingPasswordsSnackbar().open()
                return
            
            encryption_algorithm = None

            if data["algorithm"] == "RSA":
                encryption_algorithm = RSAPGP()
            else:
                encryption_algorithm = DSAElGamalPGP()

            keys = encryption_algorithm.generate_keys(data["size"])

            print(keys)
            
            self.dialog.dismiss(force=True)






