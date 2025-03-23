import os

from dotenv import load_dotenv
from pathlib import Path


BASE_DIR = Path(__file__).parent.parent
PATH_TO_ENV = BASE_DIR / ".env"
PATH_TO_RESOURCES = BASE_DIR / "app" / "resources"
PATH_TO_MESSAGES = PATH_TO_RESOURCES / "messages"

load_dotenv(PATH_TO_ENV)

OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]
TG_BOT_API_KEY = os.environ["TG_BOT_API_KEY"]