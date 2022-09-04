import os


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

            optionIndex = int(input(">>> ")) - 1

            if optionIndex >= 0 and optionIndex < len(options):
                return options[optionIndex]["value"]

        except ValueError:
            continue
