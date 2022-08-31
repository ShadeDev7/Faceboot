from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.chrome.service import Service

from utils import read_file, get_input, create_json_file
from constants import CONFIG_OBJECT, VISUALS_OPTIONS, DRIVER_ARGUMENTS, BROWSER_URL


def get_config() -> dict | None:
    config = read_file("config.json")

    if config is None:
        return

    config_keys = config.keys()

    for key in CONFIG_OBJECT.keys():
        keyExists = key in config_keys
        keyValues = CONFIG_OBJECT[key]

        if keyExists and (not keyValues or config[key] in keyValues):
            continue

        return

    return config


def create_config() -> dict:
    username = get_input("Facebook Account Username: ")
    password = get_input("Facebook Account Password: ")
    visuals = get_input("Do you want to activate bot visuals?", VISUALS_OPTIONS)

    config = {
        "username": username,
        "password": password,
        "visuals": visuals,
    }

    create_json_file("config", config)

    return config


def initialize_driver(visuals: bool) -> Chrome:
    arguments = DRIVER_ARGUMENTS + ["--headless"] if not visuals else DRIVER_ARGUMENTS

    options = ChromeOptions()
    options.binary_location = BROWSER_URL

    for argument in arguments:
        options.add_argument(argument)

    return Chrome(
        service=Service(executable_path="./chromedriver.exe"), options=options
    )
