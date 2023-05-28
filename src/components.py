from kivymd.uix.tooltip import MDTooltip
from kivymd.uix.button.button import MDFloatingBottomButton
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.list import OneLineListItem
from kivy.uix.behaviors import ButtonBehavior

# Define custom components that we are going to use from kivy

class FloatingButton(MDFloatingBottomButton, MDTooltip):
    """
    A class to represent FloatingButton component. 
    This class is empty and will be used by Kivy framework
    """
    pass

class DialogContent(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        menu_items = [
            {
                "viewclass": "OneLineListItem",
                "text": "RSA",
                "data": 0,
                "on_release": lambda x="RSA", set_item=DialogContent.set_item, this=self: set_item(this, x),
            },
            {
                "viewclass": "OneLineListItem",
                "text": "DSA & ElGamal",
                "data": 1,
                "on_release": lambda x="DSA & ElGamal", set_item=DialogContent.set_item, this=self: set_item(this, x),
            }
        ]
        
        self.menu = MDDropdownMenu(
            caller=self.ids.drop_item,
            items=menu_items,
            position="auto",
            width_mult=3
        )

        self.menu.bind()

    
    def set_item(self, text_item):
        self.ids.drop_item.set_item(text_item)
        self.menu.dismiss()

    def open_item(self):
        if self.menu:
            self.menu.open()