import os
from dotenv import load_dotenv

# Try project root .env first
ROOT_ENV = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env")
BACKEND_ENV = os.path.join(os.path.dirname(__file__), ".env")

# Load root .env if present, otherwise backend .env
if os.path.exists(ROOT_ENV):
    load_dotenv(ROOT_ENV)
else:
    load_dotenv(BACKEND_ENV)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN", "")

if not OPENAI_API_KEY:
    raise RuntimeError("OPENAI_API_KEY missing in project/.env or backend/.env")
