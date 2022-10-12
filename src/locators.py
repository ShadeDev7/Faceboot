from selenium.webdriver.common.by import By


class Locators:
    LOGIN_FORM = (By.ID, "login_form")
    USERNAME_INPUT = (By.NAME, "email")
    PASSWORD_INPUT = (By.NAME, "pass")
    LOGIN_BUTTON = (By.NAME, "login")
    ONE_TOUCH_LOGIN_SCREEN = (
        By.XPATH,
        '//table[@role="presentation"]/tbody/tr/td/div/img',
    )
    USERNAME = (
        By.XPATH,
        '//*[@id="root"]/table/tbody/tr/td/div/div[2]/div/div/div[2]/table/tbody/tr/td[2]/div',
    )
    GROUP_HEADER = (By.TAG_NAME, "header")
    GROUP_NAME = (
        By.XPATH,
        '//a[@href="#groupMenuBottom"]/table/tbody/tr/td[2]/h1/div',
    )
    MESSAGE_INPUT = (By.NAME, "xc_message")
    CAMERA_BUTTON = (By.NAME, "view_photo")
    IMAGES_FORM = (By.XPATH, '//form[@enctype="multipart/form-data"]')
    ADD_IMAGES_BUTTON = (By.NAME, "add_photo_done")
    POST_BUTTON = (By.NAME, "view_post")
