from dotenv import load_dotenv
import os

load_dotenv()  # Load .env into environment

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
SCHOLAR_BASE_URL = os.getenv("SCHOLAR_BASE_URL")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4-turbo")
