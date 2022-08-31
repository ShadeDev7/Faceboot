from utils import read_file, get_input, create_json_file
from constants import CONFIG_OBJECT, LANG_OPTIONS, VISUALS_OPTIONS


def get_config() -> dict | None:
    config = read_file("config.json")

    if config is None:
        return

    config_keys = config.keys()

    """
    Casos en los que está mal la config:
        if 


        key not in config_keys
        config[key] not in CONFIG_OBJECT[key]
    """

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
    lang = get_input("Please select your language", LANG_OPTIONS)
    visuals = get_input("Do you want to activate bot visuals?", VISUALS_OPTIONS)

    config = {
        "username": username,
        "password": password,
        "lang": lang,
        "visuals": visuals,
    }

    create_json_file("config", config)

    return config
