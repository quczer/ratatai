from pathlib import Path

import click

from ratatai import config, logger
from ratatai.create import create_cooking_assistant


@click.command()
@click.argument(
    "recipe_path",
    type=click.Path(exists=True, dir_okay=False),
    default=config.Files.DEFAULT_RECIPE,
)
def run(recipe_path: Path) -> None:
    logger.info("Reading recipe...")
    with open(recipe_path) as file:
        recipe_steps = file.read()

    logger.debug("Creating cooking assistant...")
    assistant = create_cooking_assistant(recipe_steps=recipe_steps)
    logger.debug("Cooking assistant created!")

    assistant.run()
