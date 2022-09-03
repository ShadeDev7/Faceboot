from utils import read_file, get_input, create_json_file
from constants import CONFIG_OBJECT, VISUALS_OPTIONS


def get_config() -> dict | None:
    config = read_file("config.json")

    if config is None:
        return

    config_keys = config.keys()

    for key in CONFIG_OBJECT.keys():
        possible_values = CONFIG_OBJECT[key]
        has_infinite_values = len(possible_values) == 0

        if (
            key not in config_keys
            or (has_infinite_values and type(config[key]) != str)
            or (not has_infinite_values and config[key] not in possible_values)
        ):
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
