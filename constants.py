VERSION = "0.0.0"

CONFIG_OBJECT = {
    "username": [],
    "password": [],
    "visuals": [True, False],
}

VISUALS_OPTIONS = [
    {"display": "Yes", "value": True},
    {"display": "No", "value": False},
]

DRIVER_ARGUMENTS = [
    f"--user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36",
    "--mute-audio",
    "--disable-extensions",
    "--disable-dev-sh-usage",
    "--disable-gpu",
    "log-level=3",
]

BROWSER_URL = "C:\\Program Files\\BraveSoftware\\Brave-Browser\\Application\\brave.exe"

LOADING_TIMEOUT = 5
