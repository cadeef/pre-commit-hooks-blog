#!/usr/bin/env python3
from pathlib import Path
from subprocess import CalledProcessError, run
from typing import List, Optional, Tuple

import click

from pre_commit_hooks_blog.util import Hook, HookException, Result


@click.command()
@click.argument(
    "files",
    required=True,
    nargs=-1,
    type=click.Path(exists=True),
    metavar="</path/to/file(s)>",
)
@click.option("--config", "-c", type=click.Path(exists=True), help="Config file")
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
    config: Optional[str] = None,
    ansi: bool = True,
    verbose: bool = False,
) -> None:
    """
    Wrapper to run markdownlint

    Primarily a means to unify interface and options.

    Expects path(s) to a file(s) that exists.
    """

    hook = Hook(name=__name__, function=run_step, ansi=ansi, verbose=verbose)
    try:
        hook.run(files, config=config)
    except HookException as e:
        hook.error(str(e))


def run_step(file: Path, config: Optional[str] = None) -> List[Result]:
    cmd = ["markdownlint"]

    if config:
        for i in ("--config", config):
            # FIXME append is probably wrong here
            cmd.append(i)

    # Add file
    cmd.append(str(file))

    # shell=true doesn't like cmd as a list
    cmd_str = " ".join(cmd)

    try:
        # FIXME: Currently run in a shell so we have PATH and don't have to find markdownlint
        result = run(cmd_str, capture_output=True, check=True, shell=True).stdout
    except CalledProcessError as e:
        if e.returncode == 1:
            result = e.stderr
        else:
            raise HookException(e)

    output = result.decode("utf-8")

    # Markdownlint returns full, per-file output, return 0 for line
    return [Result(0, output)]


if __name__ == "__main__":
    main()
