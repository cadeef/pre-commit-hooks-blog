from pathlib import Path
from typing import Tuple

import click

import pre_commit_hooks_blog.util as pcu


@click.command()
@click.argument(
    "files", nargs=-1, type=click.Path(exists=True), metavar="</path/to/file>"
)
@click.option(
    "--ansi/--no-ansi", default=True, help="Toggle color output, on by default"
)
def main(files: Tuple[Path, ...], ansi: bool = True):
    pcu.output(str(files), ansi=ansi)


if __name__ == "__main__":
    main()
