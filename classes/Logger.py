import os
import time

from constants import VERSION, MESSAGES

COLORS = {
    "DEBUG": "\033[32m",
    "EVENT": "\033[34m",
    "ERROR": "\033[31m",
    "RESET": "\033[0m",
}


class Logger:
    def __init__(self, lang: str) -> None:
        self.__lang = lang

        os.makedirs("./logs", exist_ok=True)

    def log(self, message_id: str) -> None:
        message_data = MESSAGES[message_id]
        message_type = message_data["messageType"]

        message = f">> [v{VERSION} | {time.strftime('%H:%M:%S')}] ¦ [{message_type}] ¦ {message_data['variants'][self.__lang]}"

        print(COLORS[message_type] + message + COLORS["RESET"])

        with open(
            f"./logs/{time.strftime('%d-%m-%Y')}.txt", "a+", encoding="utf-8"
        ) as f:
            f.write(message + "\n")
