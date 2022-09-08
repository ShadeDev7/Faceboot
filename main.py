import os

from classes import Bot
from functions import create_config
from constants import VERSION


def main() -> None:
    os.system(f"title Faceboot v{VERSION} by ShadeDev7")

    bot = Bot(create_config())

    while True:
        if bot.invalid_credentials or bot.error:
            break

        logged = bot.login()

        if not logged:
            continue

        bot.start_posting()

        # Only for testing purposes.
        os.system("pause")
        break


if __name__ == "__main__":
    main()
