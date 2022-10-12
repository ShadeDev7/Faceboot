import os
import time
from urllib import request
from zipfile import ZipFile

from utils import (
    get_input,
    get_chromedriver_versions,
    get_brave_version,
    is_valid_group_url,
)
from constants import (
    CALCULATED_TIME_OPTIONS,
    MODE_OPTIONS,
    STATIC_TIME_OPTIONS,
    VISUALS_OPTIONS,
    IMAGE_EXTENSIONS,
    MAX_IMAGE_SIZE,
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

    os.system("cls")

    return {
        "username": username,
        "password": password,
        "visuals": visuals,
        "mode": mode,
        "ST" if st else "CT": st if st else ct,
    }


def download_chromedriver() -> bool:
    chromedriver_versions = get_chromedriver_versions()
    brave_version = get_brave_version()

    if not chromedriver_versions or not brave_version:
        return False

    version = brave_version.split(".")[0]

    for v in chromedriver_versions:
        if version in v:
            version = v
            break

    url = (
        f"https://chromedriver.storage.googleapis.com/{version}/chromedriver_win32.zip"
    )
    filename = "temp-" + str(int(time.time())) + ".zip"
    request.urlretrieve(url, filename)
    ZipFile(filename, "r").extractall()
    os.remove(filename)

    return True


def get_groups() -> list[str] | None:
    while True:
        try:
            with open("groups.txt", "r", encoding="utf-8") as f:
                groups = []

                for line in f.readlines():
                    group_url = line.replace("\n", "").strip().lower()

                    if is_valid_group_url(group_url):
                        groups.append(group_url)

                return groups
        except FileNotFoundError:
            return


def get_message() -> list[str] | None:
    while True:
        try:
            with open("message.txt", "r", encoding="utf-8") as f:
                messages = [line.strip() for line in f.readlines()]

                if not messages or not "".join(messages):
                    return

                return messages
        except FileNotFoundError:
            return


def get_images() -> list[str]:
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
