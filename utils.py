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

        return False
    except ValueError:
        return False


def get_group_id(group: str) -> str:
    segments = group.split("/")

    return segments[-1] if segments[-1] else segments[-2]
