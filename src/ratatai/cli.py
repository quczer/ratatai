from pathlib import Path

import click

from ratatai import config


@click.command()
@click.argument(
    "recipe_path",
    type=click.Path(exists=True, dir_okay=False),
    default=config.Files.DEFAULT_RECIPE,
)
def run(recipe_path: Path) -> None:
    with open(recipe_path) as file:
        recipe = file.read().strip()

    click.echo(f"{recipe=}")
