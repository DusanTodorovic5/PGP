from kivymd.uix.tooltip import MDTooltip
from kivymd.uix.button.button import MDFloatingBottomButton
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.label import MDLabel
from kivy.properties import StringProperty
from kivymd.uix.snackbar import BaseSnackbar

# Define custom components that we are going to use from kivy

class FloatingButton(MDFloatingBottomButton, MDTooltip):
    """
    A class to represent FloatingButton component. 
    This class is empty and will be used by Kivy framework
    """
    pass

class CustomBaseSnackbar(BaseSnackbar):
    text = StringProperty("")

class MissingFieldSnackbar(CustomBaseSnackbar):
    pass

class NonMatchingPasswordsSnackbar(CustomBaseSnackbar):
    pass

class DialogContent(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.current_item = "RSA"
        self.current_size = 1024

        algorithms_menu_items = [
            {
                "viewclass": "OneLineListItem",
                "text": "RSA",
                "data": 0,
                "on_release": lambda x="RSA", set_item=DialogContent.algorithm_set_item, this=self: set_item(this, x),
            },
            {
                "viewclass": "OneLineListItem",
                "text": "DSA & ElGamal",
                "data": 1,
                "on_release": lambda x="DSA & ElGamal", set_item=DialogContent.algorithm_set_item, this=self: set_item(this, x),
            }
        ]

        key_size_items = [
            {
                "viewclass": "OneLineListItem",
                "text": "1024",
                "data": 0,
                "on_release": lambda x="1024", set_item=DialogContent.key_size_set_item, this=self: set_item(this, x),
            },
            {
                "viewclass": "OneLineListItem",
                "text": "2048",
                "data": 1,
                "on_release": lambda x="2048", set_item=DialogContent.key_size_set_item, this=self: set_item(this, x),
            }
        ]

        
        
        self.algorithm_menu = MDDropdownMenu(
            caller=self.ids.algorithm_drop_item,
            items=algorithms_menu_items,
            position="auto",
            width_mult=3
        )
        self.algorithm_menu.bind()

        self.key_size_menu = MDDropdownMenu(
            caller=self.ids.key_size_drop_item,
            items=key_size_items,
            position="auto",
            width_mult=3
        )
        self.key_size_menu.bind()

    
    def algorithm_set_item(self, text_item):
        self.ids.algorithm_drop_item.set_item(text_item)
        self.current_item = text_item
        self.algorithm_menu.dismiss()

    def algorithm_open_item(self):
        if self.algorithm_menu:
            self.algorithm_menu.open()

    def key_size_set_item(self, text_item):
        self.ids.key_size_drop_item.set_item(text_item)
        self.current_size = int(text_item)
        self.key_size_menu.dismiss()

    def key_size_open_item(self):
        if self.key_size_menu:
            self.key_size_menu.open()

    def get_data(self):
        return {
            "name": self.ids.name_field.text,
            "email": self.ids.email_field.text,
            "algorithm": self.current_item,
            "size": self.current_size
        }
    
class PasswordDialog(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def get_data(self):
        return {
            "password": self.ids.password_field.text,
            "confirm_password": self.ids.confirm_field.text
        }