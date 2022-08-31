import os

from classes import Logger
from functions import get_config, create_config, initialize_driver
from constants import VERSION


def main() -> None:
    os.system(f"title Facebook Bot v{VERSION} by ShadeDev7")

    config = get_config() or create_config()

    logger = Logger()
    logger.log(f"Welcome, {config['username']}!", "DEBUG")

    driver = initialize_driver(config["visuals"])
    driver.get("https://mbasic.facebook.com")

    os.system("pause")


if __name__ == "__main__":
    main()
