from pathlib import Path
from subprocess import CalledProcessError, run
from typing import Tuple

import click

from pre_commit_hooks_blog.util import Hook, HookException, Result


@click.command()
@click.argument(
    "files",
    required=True,
    nargs=-1,
    type=click.Path(exists=True),
    metavar="</path/to/file>",
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
    files: Tuple[Path, ...], ansi: bool = True, verbose: bool = False, **kwargs
) -> None:
    """
    Wrapper to run markdown-link-check

    Primarily a means to unify interface and options.

    Expects a path(s) to a file that exists.
    """

    hook = Hook(name=__name__, function=run_step, ansi=ansi, verbose=verbose)
    try:
        hook.run(files)
    except HookException as e:
        hook.error(str(e))


def run_step(file: Path) -> Result:
    cmd = ("markdown-link-check", str(file))
    try:
        # FIXME: Currently run in a shell so we have PATH and don't have to find MLC
        result = run(cmd, capture_output=True, check=True, shell=True)
    except CalledProcessError as e:
        raise HookException(e)

    output = result.stdout.decode("utf-8")

    # Markdown link check returns full, per-file output, return 0 for line
    # TODO: Consider a custom type for this return that better describes return
    return Result(0, output)


if __name__ == "__main__":
    main()
