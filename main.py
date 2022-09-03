import os

from classes import Bot
from functions import get_config, create_config
from constants import VERSION


def main() -> None:
    os.system(f"title Facebook Bot v{VERSION} by ShadeDev7")

    config = get_config() or create_config()

    bot = Bot(config)
    bot.login()

    os.system("pause")


if __name__ == "__main__":
    main()
