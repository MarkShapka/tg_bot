from config import PATH_TO_MESSAGES, PATH_TO_IMAGES


def load_messages(name: str) -> str:
    with open(PATH_TO_MESSAGES / f"{name}.txt", "r") as src:
        return src.read()

def load_images(image_file: str):
    with open(PATH_TO_IMAGES / f"{image_file}", "rb") as src:
        return src.read()



if __name__ == "__main__":
    print(load_messages("menu"))
