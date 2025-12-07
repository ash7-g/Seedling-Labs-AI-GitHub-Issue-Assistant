import os
from dotenv import load_dotenv

# Find the real folder the code is running from
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
ENV_PATH = os.path.join(CURRENT_DIR, ".env")

print("DEBUG: Looking for .env at:", ENV_PATH)
print("DEBUG: File exists? ->", os.path.exists(ENV_PATH))

# Force-load .env
load_dotenv(ENV_PATH)

print("DEBUG: Loaded OPENAI_API_KEY =", os.getenv("OPENAI_API_KEY"))

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

if not OPENAI_API_KEY:
    raise RuntimeError("❌ ERROR: OPENAI_API_KEY is missing. Check backend/.env")
