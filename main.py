import os

from classes import Logger
from functions import get_config, create_config
from constants import VERSION


def main() -> None:
    os.system(f"title Facebook Bot v{VERSION}")

    config = get_config() or create_config()

    logger = Logger(config["lang"])

    logger.log("welcome")


if __name__ == "__main__":
    main()
