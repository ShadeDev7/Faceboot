from utils import read_file, get_input, create_json_file
from constants import CONFIG_OBJECT, LANG_OPTIONS, VISUALS_OPTIONS


def get_config() -> dict | None:
    config = read_file("config.json")

    if config is None:
        return

    config_keys = config.keys()

    for key in CONFIG_OBJECT.keys():
        if (key not in config_keys) or (config[key] not in CONFIG_OBJECT[key]):
            return

    return config


def create_config() -> dict:
    lang = get_input("Please select your language", LANG_OPTIONS)
    visuals = get_input("Do you want to activate bot visuals?", VISUALS_OPTIONS)

    config = {"lang": lang, "visuals": visuals}

    create_json_file("config", config)

    return config
