import os
import time
import psutil
import subprocess
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import (
    SessionNotCreatedException,
    TimeoutException,
    NoSuchElementException,
    ElementNotInteractableException,
)

from .Logger import Logger
from locators import Locators
from attempts import Attempts
from cooldowns import Cooldowns
from functions import download_chromedriver, get_groups, get_images, get_message
from utils import get_group_id
from constants import (
    VERSION,
    DRIVER_ARGUMENTS,
    BROWSER_URL,
    LOADING_TIMEOUT,
    MAX_IMAGES,
)
from exceptions import CouldNotSendPostException


class Bot:
    # Private values
    __logger: Logger
    __username: str
    __password: str
    __headless: bool
    __mode: str
    __groups: list[str]
    __message: list[str]
    __images: list[str]

    # Public values
    error: bool
    logged: bool
    invalid_credentials: bool

    def __init__(self, config: dict) -> None:
        self.__logger = Logger()
        self.error = False
        self.logged = False
        self.invalid_credentials = False

        self.__logger.log(f"Starting Faceboot v{VERSION}...", "DEBUG")
        time.sleep(3)

        if "chromedriver.exe" not in os.listdir("."):
            self.__logger.log("Chrome driver not found! Downloading it...", "DEBUG")

            if not download_chromedriver():
                self.__logger.log("Couldn't download the chrome driver!", "ERROR")
                self.error = True

                return

        self.__logger.log("Fetching configuration...", "DEBUG")
        time.sleep(3)

        self.__username = config["username"]
        self.__password = config["password"]
        self.__headless = not config["visuals"]
        self.__mode = config["mode"]
        self.__groups = get_groups()
        self.__message = get_message()
        self.__images = get_images()

        if not self.__groups or not self.__message:
            self.__logger.log(
                "Either the groups file or the message file doesn't exist or is empty!",
                "ERROR",
            )
            self.error = True

            return

        self.__logger.log("All good. Initializing...", "DEBUG")

        self.__sleep_time = (
            config["ST"] if self.__mode == "ST" else config["CT"] // len(self.__groups)
        )
        self.__driver = self.__initialize_driver()

    def __initialize_driver(self) -> Chrome:
        arguments = (
            DRIVER_ARGUMENTS + ["--headless"] if self.__headless else DRIVER_ARGUMENTS
        )

        options = ChromeOptions()
        options.binary_location = BROWSER_URL
        options.add_experimental_option("excludeSwitches", ["enable-logging"])

        for argument in arguments:
            options.add_argument(argument)

        try:
            return Chrome(
                service=Service(executable_path="./chromedriver.exe"), options=options
            )
        except SessionNotCreatedException:
            os.remove("chromedriver.exe")
            self.__logger.log(
                "Invalid chrome driver version! Downloading the correct one...", "ERROR"
            )

            if not download_chromedriver():
                self.__logger.log("Couldn't download the chrome driver!", "ERROR")
                self.error = True

                return

            return self.__initialize_driver()

    def __await_element_load(self, locator: tuple) -> bool:
        try:
            WebDriverWait(self.__driver, LOADING_TIMEOUT).until(
                EC.presence_of_element_located(locator)
            )

            return True
        except TimeoutException:
            return False

    def __await_redirect(self) -> bool:
        start_time = time.time()

        while True:
            if "_rdr" in self.__driver.current_url:
                return True

            if time.time() - start_time >= (LOADING_TIMEOUT * 1000):
                return False

            time.sleep(0.5)

    def login(self) -> None:
        self.__logger.log("Trying to log in...", "DEBUG")
        attempt = 0

        while attempt <= Attempts.LOGIN:
            self.__driver.get("https://mbasic.facebook.com")

            if not self.__await_element_load(Locators.LOGIN_FORM):
                self.__logger.log(
                    f"Couldn't load the login page! Trying again in {Cooldowns.LOGIN} seconds... ({attempt+1}/{Attempts.LOGIN})",
                    "ERROR",
                )
                time.sleep(Cooldowns.LOGIN)
                attempt += 1

                continue
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
                    if "checkpoint" in self.__driver.current_url:
                        self.__logger.log(
                            "Human verification required (Visuals ON)",
                            "ERROR",
                        )
                        input(
                            "\nAfter the verification process, press [ENTER] and re-open Faceboot...\n"
                        )
                        self.error = True

                        return

                    self.__logger.log(
                        f"Invalid username or password.",
                        "ERROR",
                    )
                    self.invalid_credentials = True

                    return

                username = self.__driver.find_element(*Locators.USERNAME).text

                self.__logger.log(f"Logged in as {username}.", "EVENT")
                self.logged = True

                return
            except (
                NoSuchElementException,
                ElementNotInteractableException,
            ):
                break

        self.__logger.log("Couldn't log in, please contact the developers!", "ERROR")
        self.error = True

    def start_posting(self) -> None:
        for group in self.__groups:
            try:
                self.__driver.get(group)

                if not self.__await_element_load(Locators.GROUP_HEADER):
                    raise CouldNotSendPostException

                group_name = self.__driver.find_element(*Locators.GROUP_NAME).text
                self.__logger.log(f"Posting on {group_name}...", "DEBUG")

                message_input = self.__driver.find_element(*Locators.MESSAGE_INPUT)
                for line in self.__message:
                    message_input.send_keys(line + "\n")

                if self.__images:
                    self.__driver.find_element(*Locators.CAMERA_BUTTON).click()

                    if not self.__await_element_load(Locators.IMAGES_FORM):
                        raise CouldNotSendPostException

                    for i in range(min(len(self.__images), MAX_IMAGES)):
                        self.__driver.find_element(By.NAME, f"file{i+1}").send_keys(
                            self.__images[i]
                        )

                    self.__driver.find_element(*Locators.ADD_IMAGES_BUTTON).click()

                    if not self.__await_element_load(Locators.POST_BUTTON):
                        raise CouldNotSendPostException

                self.__driver.find_element(*Locators.POST_BUTTON).click()

                if not self.__await_redirect():
                    raise CouldNotSendPostException

                self.__logger.log("Post sent successfully.", "EVENT")
                self.__logger.log(
                    f"Waiting {self.__sleep_time // 60} minutes...", "DEBUG"
                )

                time.sleep(self.__sleep_time)
            except (
                NoSuchElementException,
                ElementNotInteractableException,
                CouldNotSendPostException,
            ):
                self.__logger.log(
                    f"Couldn't post on group with id {get_group_id(group)}!",
                    "ERROR",
                )

                continue

    def close(self) -> None:
        self.__logger.log("Closing... Please wait!\n", "CLOSE")
        # As the driver.quit() method doesn't end brave browser processes,
        # the only way I found to do it was killing them manually.
        try:
            for process in psutil.process_iter():
                if (
                    process.name() == "brave.exe"
                    and "--test-type=webdriver" in process.cmdline()
                ):
                    subprocess.call(
                        f"taskkill /pid {process.pid} /f",
                        stderr=subprocess.DEVNULL,
                        stdout=subprocess.DEVNULL,
                    )
        except (ProcessLookupError, psutil.NoSuchProcess):
            pass

        os.system("pause")
