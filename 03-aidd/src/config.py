import os
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
OPENROUTER_API_KEY=os.environ["OPENROUTER_API_KEY"]
OPENROUTER_MODEL = os.environ.get("OPENROUTER_MODEL","openai/gpt-oss-20b:free") #, "openai/gpt-3.5-turbo")
OPENROUTER_URL = os.environ.get("OPENROUTER_URL")
