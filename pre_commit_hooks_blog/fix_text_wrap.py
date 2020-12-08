from pathlib import Path
from typing import List, Tuple

import click

from pre_commit_hooks_blog.util import Hook, HookException, Post, Result

# from textwrap import wrap


@click.command()
@click.argument(
    "files",
    required=True,
    nargs=-1,
    type=click.Path(exists=True),
    metavar="</path/to/file>",
)
@click.option(
    "--width",
    "-w",
    type=int,
    help="Width in characters to wrap. Default: 80",
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
    width: int = 80,
    ansi: bool = True,
    verbose: bool = False,
) -> None:
    hook = Hook(name=__name__, function=run_step, ansi=ansi, verbose=verbose)
    try:
        hook.run(files)
    except HookException as e:
        raise e


def run_step(file: Path) -> List[Result]:
    post = Post.load(file)
    if post:
        pass
    # TODO: Implement text wrapping
    return [Result(0, "File modified, text wrapped")]


if __name__ == "__main__":
    main()
