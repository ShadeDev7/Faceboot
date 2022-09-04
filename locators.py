from selenium.webdriver.common.by import By


class Locators:
    LOGIN_FORM = (By.ID, "login_form")
    USERNAME_INPUT = (By.NAME, "email")
    PASSWORD_INPUT = (By.NAME, "pass")
    LOGIN_BUTTON = (By.NAME, "login")
    ONE_TOUCH_LOGIN_SCREEN = (
        By.XPATH,
        '//form[@action="/login/device-based/update-nonce/"]',
    )
    USERNAME = (
        By.XPATH,
        '//*[@id="root"]/table/tbody/tr/td/div/div[2]/div/div/div[2]/table/tbody/tr/td[2]/div',
    )
