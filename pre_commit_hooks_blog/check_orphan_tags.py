from pathlib import Path
from typing import Tuple

import click

import pre_commit_hooks_blog.util as pcu


@click.command()
@click.argument(
    "files", nargs=-1, type=click.Path(exists=True), metavar="</path/to/file>"
)
@click.option(
    "--remove/--no-remove",
    default=False,
    help="Remove tags represented in metadata from body, off by default",
)
@click.option(
    "--ansi/--no-ansi", default=True, help="Toggle color output, on by default"
)
@click.option(
    "--verbose",
    "-v",
    is_flag=True,
    default=False,
    help="Verbose output, output is typically minimized.",
)
def main(files: Tuple[Path, ...], remove: bool = False, ansi: bool = True) -> None:
    pcu.output(str(files), ansi=ansi)


if __name__ == "__main__":
    main()
