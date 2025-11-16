import os
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
OPENROUTER_API_KEY=os.environ["OPENROUTER_API_KEY"]
OPENROUTER_MODEL = os.environ.get("OPENROUTER_MODEL","openai/gpt-oss-20b:free") #, "openai/gpt-3.5-turbo")
OPENROUTER_URL = os.environ.get("OPENROUTER_URL")
HISTORY_LEN = int(os.environ.get("HISTORY_LEN", "3"))
LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO")  # Доступные уровни: DEBUG, INFO, WARNING, ERROR, CRITICAL
LOG_FILE = os.environ.get("LOG_FILE", "bot.log")
