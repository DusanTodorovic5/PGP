import configparser
import os

def init():
    """Initalizes config data from config.ini file"""
    global config
    config = configparser.ConfigParser()
    config.read("config.ini")

def get_all_components() -> list:
    """Returns the path of all components inside path given in config file

    Returns:
        list: List of paths of all components
    """
    return [
        os.path.join(config["PGP"]["components_path"], kv_file)
        for kv_file 
        in os.listdir(config["PGP"]["components_path"])
    ]

# Returns the path of a screen given
def get_screen(name) -> str:
    """Returns the path of a screen given its name. This function adds the necessary extension and path from config file

    Args:
        name (str): Name of a screen, without extensions

    Returns:
        str: Path of a given screen with proper extensions
    """
    return os.path.join(config["PGP"]["layouts_path"], name + ".kv")

def get_icon(name) -> str:
    """Return the path of icon specified. This function adds the necessary extension and path from config file

    Args:
        name (str): Name of icon(without extension)

    Returns:
        str: Returns the full path to icon with extension
    """
    return os.path.join(config["PGP"]["assets_path"], name + ".ico")

def get_png(name) -> str:
    """Return the path of png image specified. This function adds the necessary extension and path from config file

    Args:
        name (str): Name of png image(without extension)

    Returns:
        str: Returns the full path to image with extension
    """
    return os.path.join(config["PGP"]["assets_path"], name + ".png")