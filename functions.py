from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import (
    TimeoutException,
    NoSuchElementException,
    ElementNotInteractableException,
)

from utils import read_file, get_input, create_json_file
from constants import CONFIG_OBJECT, VISUALS_OPTIONS, DRIVER_ARGUMENTS, BROWSER_URL


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


def initialize_driver(visuals: bool) -> Chrome:
    arguments = DRIVER_ARGUMENTS + ["--headless"] if not visuals else DRIVER_ARGUMENTS

    options = ChromeOptions()
    options.binary_location = BROWSER_URL

    for argument in arguments:
        options.add_argument(argument)

    return Chrome(
        service=Service(executable_path="./chromedriver.exe"), options=options
    )


def await_element_load(driver: Chrome, element: tuple) -> bool:
    try:
        WebDriverWait(driver, 5).until(EC.presence_of_element_located(element))

        return True
    except TimeoutException:
        return False


def login(driver: Chrome, username: str, password: str) -> bool:
    loaded = await_element_load(driver, (By.ID, "login_form"))

    if not loaded:
        return False

    try:
        username_input = driver.find_element(By.NAME, "email")
        username_input.click()
        username_input.send_keys(username)

        password_input = driver.find_element(By.NAME, "pass")
        password_input.click()
        password_input.send_keys(password)

        submit_button = driver.find_element(By.NAME, "login")
        submit_button.click()

        return True
    except (
        NoSuchElementException,
        ElementNotInteractableException,
    ) as e:
        print(e, e.__class__, "@login")  # Only for testing purposes.

        return False
