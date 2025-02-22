from pathlib import Path


class Files:
    REPO_DIR = Path(__file__).parent.parent.parent
    FILES_DIR = REPO_DIR / "files"
    RECIPES_DIR = FILES_DIR / "recipes"

    DEFAULT_RECIPE = RECIPES_DIR / "example.txt"
    MOCK_RESPONSE_PATH = FILES_DIR / "id_eat_you_bby.wav"
    DOTENV_FILE = REPO_DIR / ".env"


class Whisper:
    """Config for OpenAI's Whisper model.

    Notes
    -----
    Available models:
    ```
    docker-user@quczer-seagle:/mnt/ratatai$ python -c 'import whisper; print(whisper.available_models())'
    ['tiny.en', 'tiny', 'base.en', 'base', 'small.en', 'small', 'medium.en', 'medium', 'large-v1', \
    'large-v2', 'large-v3', 'large', 'large-v3-turbo', 'turbo']
    ```
    """

    MODEL_SIZE = "small.en"
