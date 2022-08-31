import json


def read_file(file: str) -> any:
    try:
        with open(file, "r+", encoding="utf-8") as f:
            extension = file.split(".")[-1].lower()

            if extension == "json":
                return json.load(f)

            if extension == "txt":
                return f.readlines()

    except (FileNotFoundError, json.decoder.JSONDecodeError):
        return


def get_input(prompt: str, options: list = []) -> str:
    while True:
        try:
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


def create_json_file(filename: str, content) -> None:
    with open(f"{filename}.json", "a+", encoding="utf-8") as f:
        f.truncate(0)
        f.seek(0)
        json.dump(content, f, indent=4)
