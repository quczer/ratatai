from pathlib import Path


class Files:
    REPO_DIR = Path(__file__).parent.parent.parent
    RECIPES_DIR = REPO_DIR / "db" / "recipes"

    DEFAULT_RECIPE = RECIPES_DIR / "example.txt"
