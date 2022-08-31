VERSION = "0.0.0"

MESSAGES = {
    "welcome": {
        "messageType": "DEBUG",
        "variants": {
            "EN": "Hello and welcome to Facebook Bot.",
            "ES": "Hola y bienvenido al Bot de Facebook.",
        },
    }
}


CONFIG_OBJECT = {
    "username": [],
    "password": [],
    "lang": ["EN", "ES"],
    "visuals": [True, False],
}

LANG_OPTIONS = [
    {"display": "English", "value": "EN"},
    {"display": "Spanish", "value": "ES"},
]

VISUALS_OPTIONS = [
    {"display": "Yes", "value": True},
    {"display": "No", "value": False},
]
