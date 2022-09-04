import time

from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.common.exceptions import (
    TimeoutException,
    NoSuchElementException,
    ElementNotInteractableException,
)

from .Logger import Logger
from locators import Locators
from cooldowns import Cooldowns
from constants import DRIVER_ARGUMENTS, BROWSER_URL, LOADING_TIMEOUT


class Bot:
    def __init__(self, config: dict) -> None:
        self.__username = config["username"]
        self.__password = config["password"]
        self.__headless = not config["visuals"]
        self.__logger = Logger()
        self.__driver = self.__initialize_driver()

        self.invalid_credentials = None
        self.error = False

        self.__logger.log(f"Welcome to Faceboot!", "DEBUG")
        self.__driver.get("https://mbasic.facebook.com")

    def __initialize_driver(self) -> Chrome:
        arguments = (
            DRIVER_ARGUMENTS + ["--headless"] if self.__headless else DRIVER_ARGUMENTS
        )

        options = ChromeOptions()
        options.binary_location = BROWSER_URL
        options.add_experimental_option("excludeSwitches", ["enable-logging"])

        for argument in arguments:
            options.add_argument(argument)

        return Chrome(
            service=Service(executable_path="./chromedriver.exe"), options=options
        )

    def __await_element_load(self, locator: tuple) -> bool:
        try:
            WebDriverWait(self.__driver, LOADING_TIMEOUT).until(
                expected_conditions.presence_of_element_located(locator)
            )

            return True
        except TimeoutException:
            return False

    def login(self) -> bool:
        if not self.__await_element_load(Locators.LOGIN_FORM):
            self.__logger.log(
                f"Couldn't load the login page... Trying again in {Cooldowns.LOGIN} seconds!",
                "ERROR",
            )

            time.sleep(Cooldowns.LOGIN)

            return False

        try:
            username_input = self.__driver.find_element(*Locators.USERNAME_INPUT)
            username_input.click()
            username_input.send_keys(self.__username)

            password_input = self.__driver.find_element(*Locators.PASSWORD_INPUT)
            password_input.click()
            password_input.send_keys(self.__password)

            loggin_button = self.__driver.find_element(*Locators.LOGIN_BUTTON)
            loggin_button.click()

            if not self.__await_element_load(Locators.ONE_TOUCH_LOGIN_SCREEN):
                self.__logger.log(
                    f"Invalid username or password.",
                    "ERROR",
                )

                self.invalid_credentials = True

                return False

            username = self.__driver.find_element(*Locators.USERNAME).text

            self.__logger.log(f"Logged in as {username}.", "EVENT")

            return True
        except (
            NoSuchElementException,
            ElementNotInteractableException,
        ):
            self.__logger.log(
                "Couldn't log in, please contact the developers!", "ERROR"
            )

            self.error = True

            return False
