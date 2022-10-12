import os
import requests
from bs4 import BeautifulSoup

from constants import BRAVE_PATH


def get_input(prompt: str, options: list = []) -> str:
    while True:
        try:
            os.system("cls")

            print(prompt)

            if not options:
                response = input(">>> ")

                if response:
                    return response

                continue

            for i, option in enumerate(options):
                print(f"{i + 1}. {option['display']}")

            option_index = int(input(">>> ")) - 1

            if option_index >= 0 and option_index < len(options):
                return options[option_index]["value"]

        except ValueError:
            continue


def get_chromedriver_versions() -> list[str] | list | None:
    html = BeautifulSoup(
        requests.get("https://chromedriver.chromium.org/downloads").content,
        "html.parser",
    )

    versions = []
    for v in html.find_all("strong")[1:]:
        text = v.text

        if "ChromeDriver" in text:
            versions.append(text.split(" ")[-1])

    return versions


def get_brave_version() -> str | None:
    for f in os.listdir(BRAVE_PATH):
        if os.path.isdir(BRAVE_PATH + f"\\{f}") and len(f.split(".")) == 4:
            return f


def is_valid_group_url(group_url: str) -> bool:
    try:
        url_segments = group_url.split("/")

        if len(url_segments) != 5:
            return False

        scheme, _, domain, subdirectory, group_id = url_segments

        if (
            scheme.replace(":", "") in ["http", "https"]
            and domain == "mbasic.facebook.com"
            and subdirectory == "groups"
            and group_id
        ):
            return True
    except ValueError:
        pass

    return False


def get_group_id(group: str) -> str:
    segments = group.split("/")

    return segments[-1] if segments[-1] else segments[-2]
