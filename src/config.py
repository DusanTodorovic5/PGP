import configparser
import os

def init():
    global config
    config = configparser.ConfigParser()
    config.read("config.ini")

def get_all_components() -> list:
    return [
        os.path.join(config["PGP"]["components_path"], kv_file)
        for kv_file 
        in os.listdir(config["PGP"]["components_path"])
    ]

def get_screen(name) -> str:
    return os.path.join(config["PGP"]["layouts_path"], name + ".kv")

def get_icon(name) -> str:
    return os.path.join(config["PGP"]["assets_path"], name + ".ico")

def get_png(name) -> str:
    return os.path.join(config["PGP"]["assets_path"], name + ".png")