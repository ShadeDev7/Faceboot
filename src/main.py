import os
from selenium.common.exceptions import NoSuchWindowException
from urllib3.exceptions import ProtocolError

from classes import Bot
from functions import create_config
from constants import VERSION


def main() -> None:
    os.system(f"title Faceboot v{VERSION} by ShadeDev7")

    bot = None

    try:
        bot = Bot(create_config())

        while True:
            if bot.error or bot.invalid_credentials:
                break

            if not bot.logged:
                bot.login()

                continue

            bot.start_posting()
    except (
        KeyboardInterrupt,
        NoSuchWindowException,
        ProtocolError
    ):
        pass

    if bot:
        bot.close()


if __name__ == "__main__":
    main()
