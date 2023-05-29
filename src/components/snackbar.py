from kivy.properties import StringProperty
from kivymd.uix.snackbar import BaseSnackbar

class CustomBaseSnackbar(BaseSnackbar):
    text = StringProperty("")

class MissingFieldSnackbar(CustomBaseSnackbar):
    pass

class NonMatchingPasswordsSnackbar(CustomBaseSnackbar):
    pass