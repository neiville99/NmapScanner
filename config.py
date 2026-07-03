import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent
ENV_PATH = BASE_DIR / ".env"

load_dotenv(dotenv_path=ENV_PATH)

SCAN_TARGET = os.getenv("SCAN_TARGET", "127.0.0.1")


# Basic validation
if not SCAN_TARGET.strip():
    raise ValueError("Scan interval cant be empty")


if __name__ == "__main__":
    print("Configuration succesful")
    print(f"Env file: {ENV_PATH}")
    print(f"Environment file exists: {ENV_PATH.exists()}")
    print(f"Scan Target: {SCAN_TARGET}")
