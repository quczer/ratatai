from pathlib import Path

import click

from ratatai import config
from ratatai.create import create_cooking_assistant


@click.command()
@click.argument(
    "recipe_path",
    type=click.Path(exists=True, dir_okay=False),
    default=config.Files.DEFAULT_RECIPE,
)
def run(recipe_path: Path) -> None:
    assistant = create_cooking_assistant()

    with open(recipe_path) as file:
        recipe = file.read().strip()

    click.echo(f"Using recipe from {recipe_path}:")
    click.echo(recipe)

    assistant.run()
