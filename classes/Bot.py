import os
import time

from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
from selenium.common.exceptions import (
    TimeoutException,
    NoSuchElementException,
    ElementNotInteractableException,
)

from .Logger import Logger
from locators import Locators
from cooldowns import Cooldowns
from constants import (
    DRIVER_ARGUMENTS,
    BROWSER_URL,
    LOADING_TIMEOUT,
    IMAGE_EXTENSIONS,
    MAX_IMAGE_SIZE,
    MAX_IMAGES,
)
from utils import is_valid_group_url, get_group_id
from exceptions import EmptyFileException, CouldNotSendPostException


class Bot:
    def __init__(self, config: dict) -> None:
        self.__username = config["username"]
        self.__password = config["password"]
        self.__headless = not config["visuals"]
        self.__mode = config["mode"]
        self.__groups = self.__get_groups()
        self.__message = self.__get_message()
        self.__images = self.__get_images()
        self.__sleep_time = (
            config["ST"] if self.__mode == "ST" else config["CT"] // len(self.__groups)
        )
        self.__logger = Logger()
        self.__driver = self.__initialize_driver()

        self.invalid_credentials = None
        self.error = False

        os.system("cls")
        self.__logger.log(f"Welcome to Faceboot!", "DEBUG")
        self.__driver.get("https://mbasic.facebook.com")

    def __get_groups(self) -> list[str]:
        while True:
            try:
                with open("groups.txt", "r", encoding="utf-8") as f:
                    groups = []

                    for line in f.readlines():
                        group_url = line.replace("\n", "").strip().lower()

                        if is_valid_group_url(group_url):
                            groups.append(group_url)

                    if not groups:
                        raise EmptyFileException

                    return groups
            except FileNotFoundError:
                self.__logger.log(
                    f"Groups.txt file not found or is invalid... Trying again in {Cooldowns.GET_FILE} seconds!",
                    "ERROR",
                )

                time.sleep(Cooldowns.GROUPS_FILE)

    def __get_message(self) -> list[str]:
        while True:
            try:
                with open("message.txt", "r", encoding="utf-8") as f:
                    messages = [line.strip() for line in f.readlines()]

                    if not messages or not "".join(messages):
                        raise EmptyFileException

                    return messages
            except (FileNotFoundError, EmptyFileException):
                self.__logger.log(
                    f"Message.txt file not found or is invalid... Trying again in {Cooldowns.GET_FILE} seconds!",
                    "ERROR",
                )

                time.sleep(Cooldowns.GET_FILE)

    def __get_images(self) -> list:
        abs_path = os.path.abspath(os.getcwd())
        images = []

        for f in os.listdir("."):
            is_image = f.split(".")[-1].lower() in IMAGE_EXTENSIONS
            stat = os.stat(f)

            if not is_image or stat.st_size // 1024 > MAX_IMAGE_SIZE:
                continue

            images.append({"path": f"{abs_path}\\{f}", "creation_time": stat.st_ctime})

        return [
            image["path"]
            for image in sorted(
                images, key=lambda image: image["creation_time"], reverse=True
            )
        ]

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

    def __await_redirect(self) -> bool:
        start_time = time.time()

        while True:
            if "_rdr" in self.__driver.current_url:
                return True

            if time.time() - start_time >= (LOADING_TIMEOUT * 1000):
                return False

            time.sleep(0.5)

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

    def start_posting(self) -> None:
        for group in self.__groups:
            try:
                self.__driver.get(group)

                if not self.__await_element_load(Locators.GROUP_HEADER):
                    raise CouldNotSendPostException

                group_name = self.__driver.find_element(*Locators.GROUP_NAME).text

                self.__logger.log(f"Sending post to {group_name}...", "DEBUG")

                message_input = self.__driver.find_element(*Locators.MESSAGE_INPUT)

                for line in self.__message:
                    message_input.send_keys(line)

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

                self.__logger.log(
                    f"Post sent successfully. Now sleeping for {self.__sleep_time // 60} minutes!",
                    "EVENT",
                )

                time.sleep(self.__sleep_time)
            except (
                NoSuchElementException,
                ElementNotInteractableException,
                CouldNotSendPostException,
            ):
                self.__logger.log(
                    f"Couldn't send post to group with id {get_group_id(group)}!",
                    "ERROR",
                )

                continue
