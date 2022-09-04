from utils import get_input
from constants import (
    CALCULATED_TIME_OPTIONS,
    MODE_OPTIONS,
    STATIC_TIME_OPTIONS,
    VISUALS_OPTIONS,
)


def create_config() -> dict:
    username = get_input("Facebook Account Username/Email: ")
    password = get_input("Facebook Account Password: ")
    visuals = get_input("Do you want to activate bot visuals?", VISUALS_OPTIONS)
    mode = get_input("What mode do you want to use?", MODE_OPTIONS)
    st, ct = None, None

    if mode == "ST":
        st = get_input("Select the amount of static time:", STATIC_TIME_OPTIONS)
    else:
        ct = get_input("Select the amount of calculated time:", CALCULATED_TIME_OPTIONS)

    return {
        "username": username,
        "password": password,
        "visuals": visuals,
        "mode": mode,
        "ST" if st else "CT": st if st else ct,
    }
