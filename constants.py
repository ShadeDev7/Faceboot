VERSION = "0.0.0"

VISUALS_OPTIONS = [
    {"display": "Yes", "value": True},
    {"display": "No", "value": False},
]

MODE_OPTIONS = [
    {"display": "Static Time", "value": "ST"},
    {"display": "Calculated Time", "value": "CT"},
]

STATIC_TIME_OPTIONS = [
    {"display": "Every 60 Minutes [SAFEST]", "value": 60},
    {"display": "Every 30 Minutes [NORMAL]", "value": 30},
    {"display": "Every 15 Minutes [RISKY]", "value": 15},
]

CALCULATED_TIME_OPTIONS = [
    {"display": "Every 24 Hours [SAFEST]", "value": 1440},
    {"display": "Every 12 Hours [NORMAL]", "value": 720},
    {"display": "Every 6 Hours [RISKY]", "value": 360},
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
