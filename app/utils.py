from config import PATH_TO_MESSAGES


def load_messages(name: str) -> str:
    with open(PATH_TO_MESSAGES / f"{name}.txt", "r") as src:
        return src.read()


if __name__ == "__main__":
    print(load_messages("menu"))