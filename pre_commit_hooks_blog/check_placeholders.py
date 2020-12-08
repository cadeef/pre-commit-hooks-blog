from pathlib import Path
from re import IGNORECASE, compile
from typing import List, Optional, Pattern, Tuple

import click

from pre_commit_hooks_blog.util import Hook, Post, Result

"""
This script could be replaced with pygrep easily, but it is more approachable-- I think.
"""


@click.command()
@click.argument(
    "files",
    required=True,
    nargs=-1,
    type=click.Path(exists=True),
    metavar="</path/to/file>",
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
@click.option(
    "--verbose",
    "-v",
    is_flag=True,
    default=False,
    help="Verbose output, output is typically minimized.",
)
def main(
    files: Tuple[Path, ...],
    slug: Optional[Tuple[str, ...]] = None,
    regex: Optional[Tuple[Pattern, ...]] = None,
    ansi: bool = True,
    verbose: bool = False,
) -> None:
    """
    Search for placeholders that haven't been replaced during document authoring.

    Expects a path to a file that exists.

    `--slug` and `--regex` may be specified multiple times.

    Example:

    \b
    check-placeholders -s 'placeholder-link' -s 'placeholder-code' -r '\\bdummy\\-\\w+\\b' my_really_cool.md
    """

    # TODO: Generate regex based on options

    pattern = r"placeholder\-[\w\-]+"
    compiled = compile(pattern, IGNORECASE)

    hook = Hook(name=__name__, function=run_step, ansi=ansi, verbose=verbose)
    try:
        hook.run(files, pattern=compiled)
    except Exception as e:
        raise e


def run_step(file: Path, pattern: Pattern) -> List[Result]:
    post = Post.load(file)

    results = []
    for i, l in enumerate(post.body(return_type="list")):
        match = pattern.findall(l)
        if match:
            # TODO: Colorize match in line
            results.append(Result(post.body_to_post_line(i), l))
    return results


if __name__ == "__main__":
    main()
