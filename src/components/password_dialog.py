from kivy.uix.boxlayout import BoxLayout

class PasswordDialog(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def get_data(self):
        return {
            "password": self.ids.password_field.text,
            "confirm_password": self.ids.confirm_field.text
        }