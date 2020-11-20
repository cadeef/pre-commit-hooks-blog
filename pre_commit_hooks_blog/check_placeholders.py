from pathlib import Path
from typing import Optional, Pattern, Tuple

import click

from pre_commit_hooks_blog.util import output

"""
This script could be replaced with pygrep easily, but it is more approachable-- I think.
"""


@click.command()
@click.argument(
    "files", nargs=-1, type=click.Path(exists=True), metavar="</path/to/file>"
)
@click.option(
    "-s",
    "--slug",
    type=str,
    multiple=True,
    required=False,
    help="placeholder token, may be specified multiple times, i.e. 'placeholder-link'",
)
@click.option(
    "-r",
    "--regex",
    multiple=True,
    required=False,
    help="python regular expression, may be specified multiple times, i.e 'placeholder\\-\\w+'",
    metavar="PATTERN",
)
@click.option(
    "--ansi/--no-ansi", default=True, help="Toggle color output, on by default"
)
def main(
    files: Tuple[Path, ...],
    slug: Optional[Tuple[str, ...]] = None,
    regex: Optional[Tuple[Pattern, ...]] = None,
    ansi: bool = True,
) -> None:
    """
    Search for placeholders that haven't been replaced during document authoring.

    Expects a path to a file that exists.

    `--slug` and `--regex` may be specified multiple times.

    Example:

    \b
    check-placeholders -s 'placeholder-link' -s 'placeholder-code' -r '\\bdummy\\-\\w+\\b' my_really_cool.md
    """

    output("{} {} {} {}".format(files, slug, regex, ansi))


if __name__ == "__main__":
    main()
