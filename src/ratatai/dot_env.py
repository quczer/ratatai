import os
from typing import Literal

import dotenv

from ratatai import config


def get_api_key(key: Literal["openai", "elevenlabs"]) -> str:
    dotenv.load_dotenv(config.Files.DOTENV_FILE)
    match key:
        case "openai":
            dotenv_key = "OPENAI_API_KEY"
        case "elevenlabs":
            dotenv_key = "ELEVENLABS_API_KEY"
        case _:
            raise ValueError(f"Unknown API key: {key}")

    return os.environ[dotenv_key]
