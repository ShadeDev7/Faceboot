from selenium.webdriver.common.by import By


class Locators:
    LOGIN_FORM = (By.ID, "login_form")
    USERNAME_INPUT = (By.NAME, "email")
    PASSWORD_INPUT = (By.NAME, "pass")
    LOGIN_BUTTON = (By.NAME, "login")
